#!/usr/bin/env python3
"""
verify_funding_db.py
Automated End-to-End Verification script for the Funding Intelligence Database.
"""

import os
import sys
import json
import argparse
import re
from typing import List, Dict, Any, Tuple
from urllib.parse import urlparse

# Validation Regexes
URL_REGEX = re.compile(
    r'^https?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^\+?[0-9\s\-()]{7,25}$')
TBD_REGEX = re.compile(r'\b(tbd|todo|n/a)\b', re.IGNORECASE)

# Placeholder Detection
EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake', 'test@']
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com', 'fake.com']

# Schemas
GOVERNMENT_SCHEMA = {
    "Name": {"type": str, "required": True},
    "Official_Website": {"type": str, "required": True, "format": "url"},
    "Funding_Programs": {"type": list, "item_type": str, "required": True},
    "Last_Project_Link": {"type": str, "required": True, "format": "url"},
    "Eligibility": {"type": list, "item_type": str, "required": True},
    "Required_Documents": {"type": list, "item_type": str, "required": True},
    "Funding_Amount": {"type": str, "required": True},
    "Application_Process": {"type": list, "item_type": str, "required": True},
    "Success_Stories": {"type": list, "item_type": str, "required": True},
    "Acceptance_Rate": {"type": str, "required": True},
    "Expected_Duration": {"type": str, "required": True},
    "Notes": {"type": str, "required": True},
    "Steps_For_Any_Project_To_Get_Funded": {"type": list, "item_type": str, "required": True},
    "Steps_For_This_Project_To_Get_Funded": {"type": list, "item_type": str, "required": True}
}

STANDARD_SCHEMA = {
    "Name": {"type": str, "required": True},
    "Category": {"type": str, "required": True},
    "Category_For_Company": {"type": list, "item_type": str, "required": True},
    "Priority": {"type": str, "required": True},
    "Country": {"type": str, "required": True},
    "City": {"type": str, "required": True},
    "Official_Website": {"type": str, "required": True, "format": "url"},
    "Official_Email": {"type": str, "required": True, "format": "email"},
    "LinkedIn": {"type": str, "required": False, "format": "linkedin"},
    "Phone": {"type": str, "required": False, "format": "phone"},
    "Description": {"type": str, "required": True}
}


class DatabaseVerifier:
    def __init__(self, target_path: str, reference_path: str, min_count: int):
        self.target_path = target_path
        self.reference_path = reference_path
        self.min_count = min_count
        self.errors: List[str] = []

    def log_error(self, message: str):
        self.errors.append(message)

    def normalize_name(self, name: str) -> str:
        if not isinstance(name, str):
            return ""
        n = name.strip().lower()
        suffixes = [
            r'\binc\.?\b', r'\bco\.?\b', r'\bltd\.?\b', r'\bllc\.?\b',
            r'\bcorp\.?\b', r'\bcorporation\b', r'\bincorporated\b', r'\bcompany\b'
        ]
        for suffix in suffixes:
            n = re.sub(suffix, '', n)
        n = re.sub(r'[^a-z0-9]', '', n)
        return n

    def normalize_url(self, url: str) -> str:
        if not isinstance(url, str):
            return ""
        u = url.strip()
        scheme_match = re.match(r'^(https?://)', u, re.IGNORECASE)
        if scheme_match:
            rest = u[len(scheme_match.group(1)):]
        else:
            rest = u

        # Split domain from the rest
        split_idx = len(rest)
        for char in ('/', '?', '#'):
            idx = rest.find(char)
            if idx != -1 and idx < split_idx:
                split_idx = idx

        domain_part = rest[:split_idx].lower()
        path_query_part = rest[split_idx:]

        if domain_part.startswith('www.'):
            domain_part = domain_part[4:]

        return (domain_part + path_query_part).rstrip('/')

    def check_placeholder(self, value: Any, context: str, field_name: str = None) -> bool:
        if isinstance(value, str):
            val_clean = value.strip().lower()
            if val_clean in EXACT_PLACEHOLDERS:
                self.log_error(f"[{context}] Placeholder detected: '{value}'")
                return True
            for kw in SUBSTRING_PLACEHOLDERS:
                if kw in val_clean:
                    self.log_error(f"[{context}] Placeholder pattern detected: '{value}'")
                    return True
            if TBD_REGEX.search(val_clean):
                self.log_error(f"[{context}] TBD/Todo pattern detected: '{value}'")
                return True
            if any(dom in val_clean for dom in DUMMY_DOMAINS):
                self.log_error(f"[{context}] Dummy domain placeholder detected: '{value}'")
                return True
            # Check for dummy phone numbers
            if field_name == "Phone" and any(seq in val_clean for seq in ['123456', '000000', '111111', '999999']):
                self.log_error(f"[{context}] Fake phone number detected: '{value}'")
                return True
        return False

    def validate_field_format(self, value: str, fmt: str, context: str) -> bool:
        if fmt == "url":
            if not URL_REGEX.match(value):
                self.log_error(f"[{context}] Invalid URL format: '{value}'")
                return False
        elif fmt == "email":
            if not EMAIL_REGEX.match(value):
                self.log_error(f"[{context}] Invalid Email format: '{value}'")
                return False
        elif fmt == "linkedin":
            is_valid_linkedin = False
            try:
                parsed = urlparse(value)
                hostname = parsed.hostname
                if hostname:
                    hostname = hostname.lower()
                    if hostname == 'linkedin.com' or hostname.endswith('.linkedin.com'):
                        is_valid_linkedin = True
            except Exception:
                pass

            if not is_valid_linkedin or not URL_REGEX.match(value):
                self.log_error(f"[{context}] Invalid LinkedIn URL: '{value}'")
                return False
        elif fmt == "phone":
            if not PHONE_REGEX.match(value) or sum(1 for c in value if c.isdigit()) < 5:
                self.log_error(f"[{context}] Invalid Phone format: '{value}'")
                return False
        return True

    def validate_entity(self, entity: Dict[str, Any], schema: Dict[str, Any], category: str, idx: int):
        entity_name = entity.get("Name", f"Entity_at_Index_{idx}")
        context = f"{category} -> '{entity_name}'"

        # Check for unexpected fields
        for field in entity:
            if field not in schema:
                self.log_error(f"[{context}] Unexpected field: '{field}'")

        # Verify fields defined in schema
        for field, rule in schema.items():
            if rule["required"] and field not in entity:
                self.log_error(f"[{context}] Missing required field: '{field}'")
                continue

            if field not in entity:
                continue

            val = entity[field]
            expected_type = rule["type"]

            if isinstance(val, str):
                val_stripped = val.strip()
                if val_stripped == "":
                    if not rule["required"]:
                        continue
                    else:
                        self.log_error(f"[{context}] Field '{field}' cannot be empty")
                        continue
                elif not rule["required"]:
                    val = val_stripped

            # Handle optional fields with None or empty string value
            if not rule["required"] and val in (None, ""):
                continue

            # Type Validation
            if not isinstance(val, expected_type):
                self.log_error(f"[{context}] Field '{field}' must be a {expected_type.__name__}, got {type(val).__name__}")
                continue

            # List Validation
            if expected_type is list:
                item_type = rule["item_type"]
                if len(val) == 0:
                    self.log_error(f"[{context}] List field '{field}' cannot be empty")
                for i, item in enumerate(val):
                    if not isinstance(item, item_type):
                        self.log_error(f"[{context}.{field}[{i}]] List item must be {item_type.__name__}, got {type(item).__name__}")
                    else:
                        if not item.strip():
                            self.log_error(f"[{context}.{field}[{i}]] List item cannot be empty string")
                        self.check_placeholder(item, f"{context}.{field}[{i}]", field)
            
            # String Validation
            elif expected_type is str:
                if rule["required"] and not val.strip():
                    self.log_error(f"[{context}] Field '{field}' cannot be empty")
                    continue
                
                # Check description length
                if field == "Description" and len(val.strip()) < 10:
                    self.log_error(f"[{context}] Description field must be at least 10 characters long")
                
                # Placeholder checks
                self.check_placeholder(val, f"{context}.{field}", field)
                
                # Format checks
                if val.strip() and "format" in rule:
                    self.validate_field_format(val, rule["format"], f"{context}.{field}")

    def verify(self) -> bool:
        # Load Reference Config
        if not os.path.exists(self.reference_path):
            self.log_error(f"Reference file not found: {self.reference_path}")
            return False

        try:
            with open(self.reference_path, "r", encoding="utf-8") as f:
                ref_data = json.load(f)
        except Exception as e:
            self.log_error(f"Failed to parse reference JSON: {e}")
            return False

        if ref_data is None or not isinstance(ref_data, dict):
            self.log_error("Failed to parse reference JSON: parsed object is not a dictionary")
            return False

        ref_categories = ref_data.get("ContentForFunding")
        if ref_categories is None or not isinstance(ref_categories, dict) or not ref_categories:
            self.log_error("Reference file is missing 'ContentForFunding' key or it is empty.")
            return False

        # Load Target File
        if not os.path.exists(self.target_path):
            self.log_error(f"Target file not found: {self.target_path}")
            return False

        try:
            with open(self.target_path, "r", encoding="utf-8") as f:
                target_data = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"Target file is invalid JSON: {e}")
            return False
        except Exception as e:
            self.log_error(f"Failed to read target file: {e}")
            return False

        target_categories = target_data.get("ContentForFunding")
        if target_categories is None or not isinstance(target_categories, dict):
            self.log_error("Root key 'ContentForFunding' is missing or not a JSON object in target file.")
            return False

        # Category Consistency Checks
        ref_keys = set(ref_categories.keys())
        target_keys = set(target_categories.keys())
        
        missing_keys = ref_keys - target_keys
        extra_keys = target_keys - ref_keys
        
        for k in missing_keys:
            self.log_error(f"Missing category in target file: '{k}'")
        for k in extra_keys:
            self.log_error(f"Unexpected category in target file: '{k}'")

        seen_names: Dict[str, Tuple[str, str]] = {}  # norm_name -> (original_name, category)
        seen_urls: Dict[str, Tuple[str, str, str]] = {}  # norm_url -> (original_url, original_name, category)
        total_entity_count = 0

        # Run validations on common categories
        common_keys = ref_keys & target_keys
        for cat_name in common_keys:
            ref_meta = ref_categories[cat_name]
            if not isinstance(ref_meta, dict):
                self.log_error(f"Category '{cat_name}' metadata in reference file is not an object")
                continue

            target_cat_obj = target_categories[cat_name]
            
            if not isinstance(target_cat_obj, dict):
                self.log_error(f"Category '{cat_name}' must be an object in target file")
                continue
            
            # 1. Validate category metadata is preserved
            for meta_key, meta_val in ref_meta.items():
                if meta_key in ("Structure", "Entities"):
                    continue
                if target_cat_obj.get(meta_key) != meta_val:
                    self.log_error(f"Category '{cat_name}' metadata mismatch. Field '{meta_key}' expected '{meta_val}', found '{target_cat_obj.get(meta_key)}'")

            # 2. Check for Entities array
            if "Entities" not in target_cat_obj:
                self.log_error(f"Category '{cat_name}' is missing nested 'Entities' key")
                continue

            entities = target_cat_obj["Entities"]
            if not isinstance(entities, list):
                self.log_error(f"Category '{cat_name}' key 'Entities' must be a list, got {type(entities).__name__}")
                continue

            # 3. Validate each entity
            schema = GOVERNMENT_SCHEMA if cat_name == "Government" else STANDARD_SCHEMA
            for idx, entity in enumerate(entities):
                total_entity_count += 1
                if not isinstance(entity, dict):
                    self.log_error(f"Category '{cat_name}' entity at index {idx} is not an object")
                    continue

                # Cross-reference validations
                name = entity.get("Name")
                if isinstance(name, str) and name.strip():
                    norm_name = self.normalize_name(name)
                    if norm_name:
                        if norm_name in seen_names:
                            prev_name, prev_cat = seen_names[norm_name]
                            self.log_error(f"Duplicate entity name: '{name}' in category '{cat_name}' is a duplicate of '{prev_name}' in '{prev_cat}'")
                        else:
                            seen_names[norm_name] = (name, cat_name)

                website = entity.get("Official_Website")
                if isinstance(website, str) and website.strip():
                    norm_url = self.normalize_url(website)
                    if norm_url:
                        if norm_url in seen_urls:
                            prev_url, prev_entity_name, prev_cat = seen_urls[norm_url]
                            self.log_error(f"Duplicate website: '{website}' for '{name}' in '{cat_name}' is a duplicate of '{prev_url}' for '{prev_entity_name}' in '{prev_cat}'")
                        else:
                            seen_urls[norm_url] = (website, name or "Unnamed", cat_name)

                # Schema checks
                self.validate_entity(entity, schema, cat_name, idx)

                # Verify standard category cross-reference fields
                if cat_name != "Government":
                    ent_cat = entity.get("Category")
                    ent_priority = entity.get("Priority")
                    ref_priority = ref_meta.get("Priority")
                    
                    if ent_cat != cat_name:
                        self.log_error(f"[{cat_name} -> '{name}'] Field 'Category' expected '{cat_name}', got '{ent_cat}'")
                    if ent_priority != ref_priority:
                        self.log_error(f"[{cat_name} -> '{name}'] Field 'Priority' expected '{ref_priority}', got '{ent_priority}'")

        # Volume verification
        if total_entity_count < self.min_count:
            self.log_error(f"Total entity count {total_entity_count} is less than required minimum {self.min_count}")

        # If there were missing or extra categories, count them as errors
        if missing_keys or extra_keys:
            return False

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Automated Funding Database Compliance Auditor")
    parser.add_argument("db_path", nargs="?", default="Funding/ContentForFunding_Expanded.json",
                        help="Path to the expanded target JSON file.")
    parser.add_argument("--reference-path", default="Funding/ContentForFunding.json",
                        help="Path to the source categories configuration file.")
    parser.add_argument("--min-count", type=int, default=150,
                        help="Minimum total entities count required (default: 150)")
    args = parser.parse_args()

    verifier = DatabaseVerifier(args.db_path, args.reference_path, args.min_count)
    success = verifier.verify()

    if success:
        print("SUCCESS: Funding expanded database verification passed successfully. No errors.")
        sys.exit(0)
    else:
        print(f"FAILURE: Verification found {len(verifier.errors)} compliance violations:", file=sys.stderr)
        for err in verifier.errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
