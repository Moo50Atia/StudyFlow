"""
updater.py
SQLite Database Updater for persisting validated enrichment outputs, version snapshots, and data sources.
"""

import json
import sqlite3
import logging
from typing import Dict, Any
from models import ValidationResult, FundingEntityItem
from config import AppConfig

class DatabaseUpdater:
    def __init__(self, config: AppConfig, logger: logging.Logger):
        self.config = config
        self.db_path = config.paths.db_path
        self.logger = logger

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def persist_enrichment(self, entity: FundingEntityItem, val_res: ValidationResult) -> bool:
        """
        Persist validated enrichment results into SQLite.
        Includes entity field updates, sources provenance, version snapshot, contacts, and status update.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cleaned = val_res.cleaned_data

            # 1. Update funding_entities fields if present in cleaned data
            update_fields = []
            params = []
            
            for field in ['official_website', 'official_email', 'linkedin', 'phone']:
                if cleaned.get(field):
                    update_fields.append(f"{field} = ?")
                    params.append(cleaned[field])

            if update_fields:
                params.append(entity.id)
                sql = f"UPDATE funding_entities SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                cursor.execute(sql, params)

            # 2. Insert Provenance Records into entity_sources
            for src in val_res.sources:
                cursor.execute("""
                    INSERT INTO entity_sources 
                    (funding_entity_id, field_name, field_value, source_type, source_url, confidence_score, verification_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (entity.id, src.field_name, str(src.field_value), src.source_type, src.source_url, src.confidence_score, src.verification_status))

            # 3. Insert Public Contacts into entity_contacts
            for cnt in val_res.contacts:
                cursor.execute("""
                    INSERT INTO entity_contacts
                    (funding_entity_id, name, position, email, linkedin, phone, confidence_score, source_url, verified_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (entity.id, cnt.name, cnt.position, cnt.email, cnt.linkedin, cnt.phone, cnt.confidence_score, cnt.source_url))

            # 4. Insert Child Records (Programs, Eligibility, Documents, Steps, Success Stories)
            for prog in cleaned.get('funding_programs', []):
                cursor.execute("""
                    INSERT INTO funding_programs (funding_entity_id, program_name)
                    VALUES (?, ?)
                """, (entity.id, prog))

            for elig in cleaned.get('eligibility', []):
                cursor.execute("""
                    INSERT INTO eligibility_requirements (funding_entity_id, criterion)
                    VALUES (?, ?)
                """, (entity.id, elig))

            for doc in cleaned.get('required_documents', []):
                cursor.execute("""
                    INSERT INTO required_documents (funding_entity_id, document_name)
                    VALUES (?, ?)
                """, (entity.id, doc))

            for idx, step in enumerate(cleaned.get('application_process', []), start=1):
                cursor.execute("""
                    INSERT INTO application_steps (funding_entity_id, step_type, step_number, instruction)
                    VALUES (?, 'general_process', ?, ?)
                """, (entity.id, idx, step))

            for story in cleaned.get('success_stories', []):
                cursor.execute("""
                    INSERT INTO success_stories (funding_entity_id, story_description)
                    VALUES (?, ?)
                """, (entity.id, story))

            # 5. Create Version Snapshot in entity_versions
            cursor.execute("SELECT COUNT(*) FROM entity_versions WHERE funding_entity_id = ?", (entity.id,))
            ver_count = cursor.fetchone()[0] + 1
            
            snapshot = {
                "entity_id": entity.id,
                "name": entity.name,
                "cleaned_data": cleaned,
                "sources_added": len(val_res.sources),
                "contacts_added": len(val_res.contacts)
            }

            cursor.execute("""
                INSERT INTO entity_versions
                (funding_entity_id, version_number, change_reason, created_by, snapshot_json)
                VALUES (?, ?, 'Browser Agent Enrichment Update', 'browser_agent', ?)
            """, (entity.id, ver_count, json.dumps(snapshot)))

            # 6. Update entity_research_status
            status_val = 'Completed' if val_res.is_valid and not val_res.warnings else 'Needs Human Review'
            cursor.execute("""
                UPDATE entity_research_status
                SET status = ?, last_error = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE funding_entity_id = ?
            """, (status_val, entity.id))

            conn.commit()
            self.logger.info(f"Successfully persisted enrichment for entity #{entity.id} [{entity.name}]. Status: {status_val}")
            return True

        except Exception as e:
            conn.rollback()
            err_msg = f"Failed to persist enrichment for entity #{entity.id}: {str(e)}"
            self.logger.error(err_msg)
            raise RuntimeError(err_msg) from e
        finally:
            conn.close()
