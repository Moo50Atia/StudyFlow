#!/usr/bin/env python3
"""
import_json.py
ETL Importer for the Funding Knowledge Database (Layer 1 Scope).
Converts ContentForFunding_Expanded.json into a 3NF normalized SQLite database (Funding/Funding.db).
"""

import os
import sys
import json
import sqlite3
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "ContentForFunding_Expanded.json")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
DB_PATH = os.path.join(BASE_DIR, "Funding.sqlite")

def slugify(text: str) -> str:
    """Generate a clean URL slug from string."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text

def clean_str(val: Any) -> Optional[str]:
    """Sanitize string values, removing empty/placeholder noise."""
    if not isinstance(val, str):
        return None
    v = val.strip()
    if not v or v.lower() in {'n/a', 'na', 'tbd', 'none', 'null', 'undefined', '-'}:
        return None
    return v

def clean_list(val: Any) -> List[str]:
    """Sanitize lists of strings."""
    if isinstance(val, str):
        c = clean_str(val)
        return [c] if c else []
    elif isinstance(val, list):
        res = []
        for item in val:
            c = clean_str(item)
            if c and c not in res:
                res.append(c)
        return res
    return []

class FundingImporter:
    def __init__(self, json_path: str, schema_path: str, db_path: str):
        self.json_path = json_path
        self.schema_path = schema_path
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def initialize_db(self):
        """Recreate database and execute DDL schema."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"[+] Removed existing database: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            ddl_script = f.read()
            self.conn.executescript(ddl_script)
        
        self.conn.commit()
        print(f"[+] Instantiated clean database schema from {self.schema_path}")

    def run_import(self):
        """Execute complete ETL import pipeline."""
        self.initialize_db()

        with open(self.json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        content_for_funding = raw_data.get('ContentForFunding', {})
        if not isinstance(content_for_funding, dict):
            raise ValueError("Invalid JSON format: 'ContentForFunding' key must be an object.")

        cursor = self.conn.cursor()

        # Cache lookups
        countries_cache: Dict[str, int] = {}
        cities_cache: Tuple[int, str] = {}  # (country_id, city_name) -> city_id
        company_types_cache: Dict[str, int] = {}

        def get_or_create_country(country_name: str) -> Optional[int]:
            c_clean = clean_str(country_name)
            if not c_clean:
                return None
            if c_clean in countries_cache:
                return countries_cache[c_clean]
            
            cursor.execute("SELECT id FROM countries WHERE LOWER(name) = LOWER(?)", (c_clean,))
            row = cursor.fetchone()
            if row:
                cid = row[0]
            else:
                cursor.execute("INSERT INTO countries (name) VALUES (?)", (c_clean,))
                cid = cursor.lastrowid
            countries_cache[c_clean] = cid
            return cid

        def get_or_create_city(country_id: Optional[int], city_name: str) -> Optional[int]:
            c_clean = clean_str(city_name)
            if not c_clean or not country_id:
                return None
            key = (country_id, c_clean.lower())
            if key in cities_cache:
                return cities_cache[key]

            cursor.execute("SELECT id FROM cities WHERE country_id = ? AND LOWER(name) = LOWER(?)", (country_id, c_clean))
            row = cursor.fetchone()
            if row:
                city_id = row[0]
            else:
                cursor.execute("INSERT INTO cities (country_id, name) VALUES (?, ?)", (country_id, c_clean))
                city_id = cursor.lastrowid
            cities_cache[key] = city_id
            return city_id

        def get_or_create_company_type(ct_name: str) -> Optional[int]:
            ct_clean = clean_str(ct_name)
            if not ct_clean:
                return None
            if ct_clean in company_types_cache:
                return company_types_cache[ct_clean]

            cursor.execute("SELECT id FROM company_types WHERE LOWER(name) = LOWER(?)", (ct_clean,))
            row = cursor.fetchone()
            if row:
                ct_id = row[0]
            else:
                s = slugify(ct_clean)
                cursor.execute("INSERT INTO company_types (name, slug) VALUES (?, ?)", (ct_clean, s))
                ct_id = cursor.lastrowid
            company_types_cache[ct_clean] = ct_id
            return ct_id

        total_entities_imported = 0

        for cat_name, cat_data in content_for_funding.items():
            if not isinstance(cat_data, dict):
                continue

            entity_type = 'government' if cat_name.lower() == 'government' else 'standard'
            priority = clean_str(cat_data.get('Priority')) or 'Medium'
            why = clean_str(cat_data.get('Why'))
            cat_slug = slugify(cat_name)

            cursor.execute("""
                INSERT INTO categories (name, slug, priority, why_reasoning, entity_type)
                VALUES (?, ?, ?, ?, ?)
            """, (cat_name, cat_slug, priority, why, entity_type))
            category_id = cursor.lastrowid

            # Process Category_For_Company at category level
            cat_company_types = clean_list(cat_data.get('Category_For_Company'))

            entities = cat_data.get('Entities', [])
            if not isinstance(entities, list):
                continue

            for ent in entities:
                if not isinstance(ent, dict):
                    continue

                ent_name = clean_str(ent.get('Name'))
                if not ent_name:
                    continue

                ent_priority = clean_str(ent.get('Priority')) or priority
                country_name = ent.get('Country')
                city_name = ent.get('City')
                
                country_id = get_or_create_country(country_name)
                city_id = get_or_create_city(country_id, city_name)

                website = clean_str(ent.get('Official_Website'))
                email = clean_str(ent.get('Official_Email'))
                linkedin = clean_str(ent.get('LinkedIn'))
                phone = clean_str(ent.get('Phone'))
                description = clean_str(ent.get('Description'))

                # Insert Entity
                cursor.execute("""
                    INSERT INTO funding_entities 
                    (funding_category_id, country_id, city_id, name, priority, official_website, official_email, linkedin, phone, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (category_id, country_id, city_id, ent_name, ent_priority, website, email, linkedin, phone, description))
                entity_id = cursor.lastrowid
                total_entities_imported += 1

                # Link Company Types (merge category-level and entity-level)
                ent_company_types = clean_list(ent.get('Category_For_Company'))
                all_ct_names = list(set(cat_company_types + ent_company_types))
                for ct_n in all_ct_names:
                    ct_id = get_or_create_company_type(ct_n)
                    if ct_id:
                        cursor.execute("""
                            INSERT OR IGNORE INTO entity_company_types (funding_entity_id, company_type_id)
                            VALUES (?, ?)
                        """, (entity_id, ct_id))

                # Handle Government Specifics
                if entity_type == 'government':
                    funding_amount = clean_str(ent.get('Funding_Amount'))
                    acceptance_rate = clean_str(ent.get('Acceptance_Rate'))
                    expected_duration = clean_str(ent.get('Expected_Duration'))
                    last_project_link = clean_str(ent.get('Last_Project_Link'))
                    notes = clean_str(ent.get('Notes'))

                    cursor.execute("""
                        INSERT INTO government_details
                        (funding_entity_id, funding_amount, acceptance_rate, expected_duration, last_project_link, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (entity_id, funding_amount, acceptance_rate, expected_duration, last_project_link, notes))

                # Handle Funding Programs
                programs = clean_list(ent.get('Funding_Programs'))
                for prog in programs:
                    cursor.execute("""
                        INSERT INTO funding_programs (funding_entity_id, program_name)
                        VALUES (?, ?)
                    """, (entity_id, prog))

                # Handle Eligibility
                eligibility_items = clean_list(ent.get('Eligibility'))
                for elig in eligibility_items:
                    cursor.execute("""
                        INSERT INTO eligibility_requirements (funding_entity_id, criterion)
                        VALUES (?, ?)
                    """, (entity_id, elig))

                # Handle Required Documents
                docs = clean_list(ent.get('Required_Documents'))
                for doc in docs:
                    cursor.execute("""
                        INSERT INTO required_documents (funding_entity_id, document_name)
                        VALUES (?, ?)
                    """, (entity_id, doc))

                # Handle Application Steps
                gen_steps = clean_list(ent.get('Application_Process'))
                for idx, step_text in enumerate(gen_steps, start=1):
                    cursor.execute("""
                        INSERT INTO application_steps (funding_entity_id, step_type, step_number, instruction)
                        VALUES (?, 'general_process', ?, ?)
                    """, (entity_id, idx, step_text))

                any_steps = clean_list(ent.get('Steps_For_Any_Project_To_Get_Funded'))
                for idx, step_text in enumerate(any_steps, start=1):
                    cursor.execute("""
                        INSERT INTO application_steps (funding_entity_id, step_type, step_number, instruction)
                        VALUES (?, 'any_project', ?, ?)
                    """, (entity_id, idx, step_text))

                this_steps = clean_list(ent.get('Steps_For_This_Project_To_Get_Funded'))
                for idx, step_text in enumerate(this_steps, start=1):
                    cursor.execute("""
                        INSERT INTO application_steps (funding_entity_id, step_type, step_number, instruction)
                        VALUES (?, 'this_project', ?, ?)
                    """, (entity_id, idx, step_text))

                # Handle Success Stories
                stories = clean_list(ent.get('Success_Stories'))
                for story in stories:
                    cursor.execute("""
                        INSERT INTO success_stories (funding_entity_id, story_description)
                        VALUES (?, ?)
                    """, (entity_id, story))

                # Log Source Provenance into entity_sources
                if website:
                    cursor.execute("""
                        INSERT INTO entity_sources 
                        (funding_entity_id, field_name, field_value, source_type, source_name, source_url, confidence_score, verification_status)
                        VALUES (?, 'official_website', ?, 'Official Website', ?, ?, 1.0, 'Verified')
                    """, (entity_id, website, ent_name, website))
                if email:
                    cursor.execute("""
                        INSERT INTO entity_sources 
                        (funding_entity_id, field_name, field_value, source_type, source_name, source_url, confidence_score, verification_status)
                        VALUES (?, 'official_email', ?, 'Official Website', ?, ?, 1.0, 'Verified')
                    """, (entity_id, email, ent_name, website or ''))

                # Initialize Research Status to Pending for Enrichment Workflow
                cursor.execute("""
                    INSERT INTO entity_research_status (funding_entity_id, status, last_attempt, retry_count)
                    VALUES (?, 'Pending', NULL, 0)
                """, (entity_id,))

        self.conn.commit()
        print(f"[+] Successfully imported {total_entities_imported} entities.")

    def validate(self):
        """Run validation integrity checks."""
        cursor = self.conn.cursor()

        # Check Foreign Keys
        fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
        if fk_violations:
            print(f"[!] ERROR: Foreign Key Violations Found: {len(fk_violations)}")
            for v in fk_violations:
                print("   ", v)
            raise RuntimeError("Foreign key integrity check failed!")
        else:
            print("[+] Foreign Key Integrity Check: PASSED (Zero violations).")

        # Table Row Counts Summary
        print("\n==================================================")
        print("DATABASE ROW COUNTS SUMMARY")
        print("==================================================")
        
        tables = [
            'categories', 'countries', 'cities', 'company_types', 'funding_entities',
            'government_details', 'funding_programs', 'eligibility_requirements',
            'required_documents', 'application_steps', 'success_stories',
            'entity_company_types', 'entity_contacts', 'entity_sources',
            'entity_versions', 'entity_research_status', 'entity_enrichment_jobs'
        ]

        for tbl in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
            count = cursor.fetchone()[0]
            print(f" - {tbl:30s}: {count:5d} records")

        print("==================================================")

    def close(self):
        if self.conn:
            self.conn.close()

def main():
    importer = FundingImporter(JSON_PATH, SCHEMA_PATH, DB_PATH)
    try:
        importer.run_import()
        importer.validate()
        print("\n[+] ETL Import Pipeline finished successfully!")
    finally:
        importer.close()

if __name__ == '__main__':
    main()
