# Design and Implementation Strategy for `verify_funding_db.py`

This document details the architecture, schemas, and verification rules for the E2E verification track of the Funding Intelligence Database project.

---

## 1. Background & Scope
The goal of the E2E testing track is to build `verify_funding_db.py` as a strict, automated gatekeeper for the expanded Funding Database (`Funding/ContentForFunding_Expanded.json`). The database is populated by browser scrapers and API integrations. The script verifies database structure, schema conformity, content integrity, uniqueness, and completeness.

---

## 2. Category-Specific Schema Models

The database contains two distinct schemas depending on the category:

### A. Government Category Schema
Entities categorized under **Government** must have exactly the following keys:
* **Name** (string): Non-empty name of the agency or program.
* **Official_Website** (string): Valid URL of the official agency site.
* **Funding_Programs** (list of strings): List of specific grant or funding program names.
* **Last_Project_Link** (string): Valid URL pointing to the last funded project list or program output page.
* **Eligibility** (list of strings): Specific eligibility criteria.
* **Required_Documents** (list of strings): List of documents required for application.
* **Funding_Amount** (string): Described or exact funding bounds (e.g., "Up to 500k EGP").
* **Application_Process** (list of strings): High-level checklist/steps to submit.
* **Success_Stories** (list of strings): Case studies or successful beneficiaries.
* **Acceptance_Rate** (string): Estimated or exact acceptance rate.
* **Expected_Duration** (string): How long the review/funding cycle takes.
* **Notes** (string): Additional contextual info.
* **Steps_For_Any_Project_To_Get_Funded** (list of strings): General requirements steps.
* **Steps_For_This_Project_To_Get_Funded** (list of strings): Actionable checklist customized for our project.

### B. Standard Schema (All Other Categories)
Entities under all other categories (e.g. Universities, Incubators, VCs) must have exactly the following keys:
* **Name** (string): Non-empty entity name.
* **Category** (string): Non-empty category name (must match the key of the parent category it is located within).
* **Category_For_Company** (list of strings): List of matching company tags (e.g. "Startup", "AI Startup").
* **Priority** (string): String value corresponding to the category priority (e.g., "Critical", "High", "Medium").
* **Country** (string): Country of operation.
* **City** (string): City of operation.
* **Official_Website** (string): Valid URL.
* **Official_Email** (string): Valid email address.
* **LinkedIn** (string, optional): Valid LinkedIn URL or empty string.
* **Phone** (string, optional): Valid phone format or empty string.
* **Description** (string): Detailed description of why it fits and what it offers (maps to original "Why").

---

## 3. Data Integrity & Validation Rules

The validation script `verify_funding_db.py` will enforce the following integrity rules:

### A. Strict Schema Adherence
* No extra keys allowed in either schema (strict validation).
* No missing keys allowed.
* Strict type checks (e.g. list fields must contain only strings; string fields must contain only strings).

### B. Contact and URL Verification (Regex)
* **URL fields** (`Official_Website`, `Last_Project_Link`, `LinkedIn`): Must match:
  `^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$`
* **Email fields** (`Official_Email`): Must match:
  `^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`
* **Phone fields** (`Phone`): If non-empty, must match:
  `^\+?[0-9\s.-]{7,20}$`

### C. Placeholder Prevention
* The script maintains a set of forbidden case-insensitive placeholders:
  `{"tbd", "placeholder", "fake@email.com", "example.com", "fake", "dummy", "n/a", "na", "none", "not available", "todo", "to be determined", "null", "empty", "temp"}`
* Any field containing these exact values (or domains like `example.com`, `fake.com` in email/websites) will be flagged.
* Short text fields cannot be empty. Text fields like `Description` and `Notes` must be at least 10 characters long to avoid lazy "TBD" equivalents.

### D. Global Uniqueness
* **De-duplication of Names**: All names are normalized (whitespace collapsed, case-folded). No duplicates allowed across the entire file.
* **De-duplication of Websites**: All website URLs are normalized (scheme removed, trailing slash removed, `www.` removed). No duplicate official websites allowed across the entire file.

### E. Database Constraints
* **Hierarchy Check**: Category keys in the expanded database must exactly match `Funding/ContentForFunding.json`.
* **Volume Check**: Total entities across all categories must be $\ge 150$.

---

## 4. Verification Script Blueprint (`verify_funding_db.py`)

Below is the proposed design of the verification script:

```python
#!/usr/bin/env python3
"""
verify_funding_db.py
E2E Testing Track automated verification script.
"""

import os
import sys
import re
import json
import argparse
from typing import List, Dict, Any, Set

class FundingDatabaseVerifier:
    def __init__(self, target_path: str, source_path: str):
        self.target_path = target_path
        self.source_path = source_path
        self.errors: List[str] = []
        
        # Regex compilation
        self.url_regex = re.compile(r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$")
        self.email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        self.phone_regex = re.compile(r"^\+?[0-9\s.-]{7,20}$")
        
        # Placeholder terms
        self.forbidden_exact = {
            "tbd", "placeholder", "fake", "dummy", "n/a", "na", 
            "none", "not available", "todo", "to be determined", "null", "empty"
        }
        self.forbidden_substrings = [
            "example.com", "fake@email.com", "test@email.com", 
            "dummy.com", "temp@email.com", "user@example.com"
        ]

    def log_error(self, message: str):
        self.errors.append(message)

    def normalize_url(self, url: str) -> str:
        if not url:
            return ""
        # Remove scheme, trailing slash, and www prefix
        normalized = url.lower().strip()
        normalized = re.sub(r"^https?://", "", normalized)
        normalized = re.sub(r"^www\.", "", normalized)
        normalized = normalized.rstrip("/")
        return normalized

    def normalize_name(self, name: str) -> str:
        return " ".join(name.lower().split())

    def check_placeholder(self, value: Any, context: str) -> bool:
        if isinstance(value, str):
            val_clean = value.strip().lower()
            if val_clean in self.forbidden_exact:
                self.log_error(f"Placeholder detected in {context}: '{value}'")
                return True
            for sub in self.forbidden_substrings:
                if sub in val_clean:
                    self.log_error(f"Placeholder domain/email pattern in {context}: '{value}'")
                    return True
        elif isinstance(value, list):
            for i, item in enumerate(value):
                self.check_placeholder(item, f"{context}[{i}]")
        return False

    def validate_url(self, url: str, context: str, optional: bool = False) -> bool:
        if not url:
            if optional:
                return True
            self.log_error(f"Missing required URL in {context}")
            return False
        if not self.url_regex.match(url):
            self.log_error(f"Invalid URL format in {context}: '{url}'")
            return False
        self.check_placeholder(url, context)
        return True

    def validate_email(self, email: str, context: str) -> bool:
        if not email:
            self.log_error(f"Missing required Email in {context}")
            return False
        if not self.email_regex.match(email):
            self.log_error(f"Invalid Email format in {context}: '{email}'")
            return False
        self.check_placeholder(email, context)
        return True

    def validate_phone(self, phone: str, context: str) -> bool:
        if not phone:
            return True # Phone is optional
        if not self.phone_regex.match(phone):
            self.log_error(f"Invalid Phone format in {context}: '{phone}'")
            return False
        self.check_placeholder(phone, context)
        return True

    def verify(self) -> bool:
        # 1. Check existence and parse source
        if not os.path.exists(self.source_path):
            self.log_error(f"Source config file not found: {self.source_path}")
            return False
        try:
            with open(self.source_path, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
        except Exception as e:
            self.log_error(f"Failed to parse source config: {e}")
            return False

        # 2. Check existence and parse target
        if not os.path.exists(self.target_path):
            self.log_error(f"Target Expanded JSON file not found: {self.target_path}")
            return False
        try:
            with open(self.target_path, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"JSON syntax error in target file: {e}")
            return False
        except Exception as e:
            self.log_error(f"Failed to read target file: {e}")
            return False

        # 3. Validate root structure
        if "ContentForFunding" not in target_data:
            self.log_error("Target JSON root must contain 'ContentForFunding' key.")
            return False

        source_categories = source_data.get("ContentForFunding", {})
        target_categories = target_data.get("ContentForFunding", {})

        # 4. Category matching check
        source_keys = set(source_categories.keys())
        target_keys = set(target_categories.keys())
        if source_keys != target_keys:
            self.log_error(f"Category keys do not match.\nMissing in Target: {source_keys - target_keys}\nExtra in Target: {target_keys - source_keys}")

        # Unique indices for duplicate checks
        seen_names: Set[str] = set()
        seen_urls: Set[str] = set()
        total_entity_count = 0

        # 5. Detailed Category and Schema checks
        for cat_name, source_meta in source_categories.items():
            if cat_name not in target_categories:
                continue
            
            target_cat = target_categories[cat_name]
            
            # Check metadata preservation
            for meta_key, meta_val in source_meta.items():
                if meta_key == "Structure" or meta_key == "Entities":
                    continue
                if target_cat.get(meta_key) != meta_val:
                    self.log_error(f"Category '{cat_name}' metadata mismatch for key '{meta_key}'. Expected '{meta_val}', found '{target_cat.get(meta_key)}'")

            # Check presence and type of Entities list
            if "Entities" not in target_cat:
                self.log_error(f"Category '{cat_name}' is missing 'Entities' list.")
                continue
            entities = target_cat["Entities"]
            if not isinstance(entities, list):
                self.log_error(f"Category '{cat_name}' key 'Entities' must be a list. Found {type(entities).__name__}")
                continue

            for idx, entity in enumerate(entities):
                total_entity_count += 1
                ctx = f"Category '{cat_name}', entity index {idx}"
                if not isinstance(entity, dict):
                    self.log_error(f"{ctx}: Entity must be a dictionary. Found {type(entity).__name__}")
                    continue

                entity_name = entity.get("Name", f"Unnamed_Entity_{idx}")
                ctx_named = f"Category '{cat_name}', entity '{entity_name}'"

                # Check Name presence
                if not entity.get("Name") or not isinstance(entity["Name"], str):
                    self.log_error(f"{ctx}: Missing or invalid 'Name'")
                else:
                    norm_name = self.normalize_name(entity["Name"])
                    if norm_name in seen_names:
                        self.log_error(f"Duplicate entity name detected: '{entity['Name']}'")
                    seen_names.add(norm_name)
                    self.check_placeholder(entity["Name"], f"{ctx_named}.Name")

                # Schema checks
                if cat_name == "Government":
                    self.validate_government(entity, ctx_named)
                else:
                    self.validate_standard(entity, ctx_named, cat_name)

                # Check unique website
                web_key = "Official_Website"
                if web_key in entity:
                    url = entity[web_key]
                    if url:
                        norm_url = self.normalize_url(url)
                        if norm_url:
                            if norm_url in seen_urls:
                                self.log_error(f"Duplicate website URL detected: '{url}' (normalized: '{norm_url}')")
                            seen_urls.add(norm_url)

        # 6. Entity Volume Constraint Check
        if total_entity_count < 150:
            self.log_error(f"Total entity count check failed. Expected >= 150, found {total_entity_count}")

        return len(self.errors) == 0

    def validate_government(self, entity: Dict[str, Any], ctx: str):
        govt_schema = {
            "Name": str,
            "Official_Website": str,
            "Funding_Programs": list,
            "Last_Project_Link": str,
            "Eligibility": list,
            "Required_Documents": list,
            "Funding_Amount": str,
            "Application_Process": list,
            "Success_Stories": list,
            "Acceptance_Rate": str,
            "Expected_Duration": str,
            "Notes": str,
            "Steps_For_Any_Project_To_Get_Funded": list,
            "Steps_For_This_Project_To_Get_Funded": list
        }

        # Check exact key matching
        entity_keys = set(entity.keys())
        expected_keys = set(govt_schema.keys())
        if entity_keys != expected_keys:
            self.log_error(f"{ctx}: Schema mismatch for Government entity.\nMissing: {expected_keys - entity_keys}\nExtra: {entity_keys - expected_keys}")

        for key, exp_type in govt_schema.items():
            if key not in entity:
                continue
            val = entity[key]
            if not isinstance(val, exp_type):
                self.log_error(f"{ctx}: Field '{key}' must be type '{exp_type.__name__}', got '{type(val).__name__}'")
                continue
            
            # String validation
            if exp_type is str:
                if key in ["Official_Website", "Last_Project_Link"]:
                    self.validate_url(val, f"{ctx}.{key}")
                else:
                    if not val.strip() and key not in ["Notes"]:
                        self.log_error(f"{ctx}: Field '{key}' cannot be empty")
                    self.check_placeholder(val, f"{ctx}.{key}")
            
            # List validation
            elif exp_type is list:
                for idx, item in enumerate(val):
                    if not isinstance(item, str):
                        self.log_error(f"{ctx}: List field '{key}' item at index {idx} must be a string, got '{type(item).__name__}'")
                    else:
                        if not item.strip():
                            self.log_error(f"{ctx}: List field '{key}' item at index {idx} cannot be empty")
                        self.check_placeholder(item, f"{ctx}.{key}[{idx}]")

    def validate_standard(self, entity: Dict[str, Any], ctx: str, expected_cat: str):
        standard_schema = {
            "Name": str,
            "Category": str,
            "Category_For_Company": list,
            "Priority": str,
            "Country": str,
            "City": str,
            "Official_Website": str,
            "Official_Email": str,
            "LinkedIn": str,
            "Phone": str,
            "Description": str
        }

        entity_keys = set(entity.keys())
        expected_keys = set(standard_schema.keys())
        if entity_keys != expected_keys:
            self.log_error(f"{ctx}: Schema mismatch for Standard entity.\nMissing: {expected_keys - entity_keys}\nExtra: {entity_keys - expected_keys}")

        for key, exp_type in standard_schema.items():
            if key not in entity:
                continue
            val = entity[key]
            if not isinstance(val, exp_type):
                self.log_error(f"{ctx}: Field '{key}' must be type '{exp_type.__name__}', got '{type(val).__name__}'")
                continue
            
            # String validation
            if exp_type is str:
                if key == "Official_Website":
                    self.validate_url(val, f"{ctx}.{key}")
                elif key == "Official_Email":
                    self.validate_email(val, f"{ctx}.{key}")
                elif key == "LinkedIn":
                    self.validate_url(val, f"{ctx}.{key}", optional=True)
                elif key == "Phone":
                    self.validate_phone(val, f"{ctx}.{key}")
                else:
                    if not val.strip():
                        self.log_error(f"{ctx}: Field '{key}' cannot be empty")
                    if key == "Category" and val != expected_cat:
                        self.log_error(f"{ctx}: Field 'Category' value '{val}' must match actual parent category '{expected_cat}'")
                    self.check_placeholder(val, f"{ctx}.{key}")
                    if key == "Description" and len(val.strip()) < 10:
                        self.log_error(f"{ctx}: Description field is too short (must be at least 10 characters)")

            # List validation
            elif exp_type is list:
                for idx, item in enumerate(val):
                    if not isinstance(item, str):
                        self.log_error(f"{ctx}: List field '{key}' item at index {idx} must be a string, got '{type(item).__name__}'")
                    else:
                        if not item.strip():
                            self.log_error(f"{ctx}: List field '{key}' item at index {idx} cannot be empty")
                        self.check_placeholder(item, f"{ctx}.{key}[{idx}]")

def main():
    parser = argparse.ArgumentParser(description="Verify Funding Database Expanded JSON file structure, schema correctness, and de-duplication rules.")
    parser.add_argument("target_path", nargs="?", default="Funding/ContentForFunding_Expanded.json",
                        help="Path to the expanded target JSON file (default: Funding/ContentForFunding_Expanded.json)")
    parser.add_argument("--source_path", default="Funding/ContentForFunding.json",
                        help="Path to the source config schema JSON file (default: Funding/ContentForFunding.json)")
    args = parser.parse_ok_args() if hasattr(parser, 'parse_ok_args') else parser.parse_args()

    verifier = FundingDatabaseVerifier(args.target_path, args.source_path)
    success = verifier.verify()

    if success:
        print("SUCCESS: Funding expanded database verification passed successfully. No errors.")
        sys.exit(0)
    else:
        print(f"FAILURE: Verification found {len(verifier.errors)} errors in target file:")
        for err in verifier.errors:
            print(f" - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 5. Mock Dataset Strategy

To thoroughly test the verification script, we design both a valid and an invalid dummy dataset.

### A. Valid Dummy Dataset: `ContentForFunding_Expanded_Valid_Dummy.json`
* Contains all 18 categories matching `ContentForFunding.json` exactly.
* Restores original `Why`, `Priority`, and config structures for all categories.
* Distributes exactly 150 entities across the categories (e.g., ~8-9 entities per category, with `Government` having 10).
* All entities have complete, non-placeholder data.
* URLs are valid, unique, and formatted with `https://`.
* Emails are unique, non-placeholder.
* LinkedIn and Phone fields are either valid or correctly empty.

### B. Invalid Dummy Dataset: `ContentForFunding_Expanded_Invalid_Dummy.json`
To verify that the verification script correctly handles edge cases, this file contains intentional, tagged violations:
1. **Missing Category**: The `"NGOs"` category is omitted entirely to trigger the category matching error.
2. **Metadata Corruption**: In `"Universities"`, the metadata field `"Priority"` is changed from `"Critical"` to `"Low"`.
3. **Invalid Email Schema**: An entity in `"Incubators"` has an invalid email: `"not-an-email"`.
4. **Invalid URL Schema**: An entity in `"Venture Capital"` has website: `"website-without-http"`.
5. **Placeholder Value**: An entity in `"Research Centers"` has email `"fake@email.com"` and description `"TBD"`.
6. **Extra Field in Schema**: An entity in `"Government"` has an extra key `"unwanted_extra_field"`.
7. **Missing Field in Schema**: An entity in `"Government"` is missing the `"Expected_Duration"` field.
8. **Duplicate Entity Name**: Two distinct entities under `"Universities"` have the name `"Cairo University"`.
9. **Duplicate Official Website**: Two entities under different categories point to the exact same website `"https://flat6labs.com"`.
10. **Total Count Violation**: Setting up an invalid variant of this dataset where the total count is less than 150.

---

## 6. Test Runner Design (`run_tests.py`)

A test runner should automate the validation of `verify_funding_db.py` itself by running it against the valid and invalid mock datasets and checking the exit codes.

### Test Runner Logic
1. Run `verify_funding_db.py` with the path to the valid dummy dataset.
   * Expect **Exit Code 0** (success).
2. Run `verify_funding_db.py` with the path to the invalid dummy dataset.
   * Expect **Exit Code 1** (failure).
   * Verify that specific expected errors are in the output log (e.g., checking for strings like "Duplicate name", "Placeholder", "Schema mismatch").
3. Run `verify_funding_db.py` with a non-existent file path.
   * Expect **Exit Code 1**.
4. Run `verify_funding_db.py` with a corrupted JSON file (syntax error).
   * Expect **Exit Code 1**.
