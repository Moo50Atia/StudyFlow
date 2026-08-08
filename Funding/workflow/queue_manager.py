"""
queue_manager.py
Queue Manager for selecting, locking, resuming, and tracking entity enrichment jobs in SQLite.
Renamed to avoid shadowing Python's standard library 'queue' module.
"""

import sqlite3
import logging
from typing import Optional, Tuple
from models import FundingEntityItem
from config import AppConfig

class QueueManager:
    def __init__(self, config: AppConfig, logger: logging.Logger):
        self.config = config
        self.db_path = config.paths.db_path
        self.logger = logger

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def reset_crashed_jobs(self):
        """Reset entities stuck in 'Running' state back to 'Pending' on startup."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE entity_research_status
                SET status = 'Pending', last_error = 'Reset after unexpected application shutdown'
                WHERE status = 'Running'
            """)
            count = cursor.rowcount
            conn.commit()
            if count > 0:
                self.logger.info(f"Reset {count} crashed or orphaned 'Running' jobs back to 'Pending'.")
        except Exception as e:
            self.logger.error(f"Error resetting crashed jobs: {e}")
        finally:
            conn.close()

    def get_next_entity(self) -> Optional[FundingEntityItem]:
        """Fetch the next pending or retriable failed entity and mark it as 'Running'."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            max_retries = self.config.queue.max_retries
            cursor.execute("""
                SELECT e.id, e.funding_category_id, c.name as category_name, e.name, e.priority, 
                       co.name as country_name, ci.name as city_name, e.official_website, 
                       e.official_email, e.linkedin, e.phone, e.description, c.entity_type
                FROM funding_entities e
                JOIN categories c ON e.funding_category_id = c.id
                LEFT JOIN countries co ON e.country_id = co.id
                LEFT JOIN cities ci ON e.city_id = ci.id
                JOIN entity_research_status s ON e.id = s.funding_entity_id
                WHERE (s.status = 'Pending' OR (s.status = 'Failed' AND s.retry_count < ?))
                ORDER BY 
                    CASE e.priority 
                        WHEN 'Critical' THEN 1 
                        WHEN 'High' THEN 2 
                        WHEN 'Medium' THEN 3 
                        ELSE 4 
                    END, e.id ASC
                LIMIT 1
            """, (max_retries,))
            row = cursor.fetchone()
            if not row:
                return None

            entity = FundingEntityItem(
                id=row[0],
                category_id=row[1],
                category_name=row[2],
                name=row[3],
                priority=row[4],
                country=row[5],
                city=row[6],
                official_website=row[7],
                official_email=row[8],
                linkedin=row[9],
                phone=row[10],
                description=row[11],
                entity_type=row[12]
            )

            # Mark state as Running
            cursor.execute("""
                UPDATE entity_research_status
                SET status = 'Running', last_attempt = CURRENT_TIMESTAMP
                WHERE funding_entity_id = ?
            """, (entity.id,))
            conn.commit()
            
            self.logger.info(f"Locked entity #{entity.id} [{entity.name}] for enrichment processing.")
            return entity
        except Exception as e:
            self.logger.error(f"Error fetching next entity from queue: {e}")
            return None
        finally:
            conn.close()

    def mark_failed(self, entity_id: int, error_msg: str):
        """Mark an entity research job as Failed and increment retry count."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE entity_research_status
                SET status = 'Failed', 
                    retry_count = retry_count + 1, 
                    last_error = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE funding_entity_id = ?
            """, (error_msg, entity_id))
            conn.commit()
            self.logger.warning(f"Entity #{entity_id} research marked as Failed. Error: {error_msg}")
        except Exception as e:
            self.logger.error(f"Error marking entity #{entity_id} as failed: {e}")
        finally:
            conn.close()

    def mark_completed(self, entity_id: int, status: str = 'Completed'):
        """Mark an entity research job as Completed or Needs Human Review."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE entity_research_status
                SET status = ?, 
                    last_error = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE funding_entity_id = ?
            """, (status, entity_id))
            conn.commit()
            self.logger.info(f"Entity #{entity_id} status updated to '{status}'.")
        except Exception as e:
            self.logger.error(f"Error completing entity #{entity_id}: {e}")
        finally:
            conn.close()
