# Technical Analysis and Design: E2E Verification Track (Explorer 3)

This document presents a synthesized design and implementation strategy for `verify_funding_db.py` and its test runner. It reconciles previous proposals from Explorers 1 and 2, defines the precise validation schemas, and provides complete, robust implementation patterns.

---

## 1. Synthesis & Reconciliation of Previous Designs

We have reviewed the analyses of Explorer 1 and Explorer 2. While both agree on the core validation requirements, they present distinct approaches in a few areas. We reconcile these differences as follows:

### A. Target File Structure & Hierarchy (Object vs. List)
* **Conflict**: Explorer 2 assumes the categories in `ContentForFunding_Expanded.json` map directly to lists of entities. Explorer 1 proposes a nested structure where each category remains an object preserving its source metadata (`Why`, `Priority`, etc.) with a nested `"Entities"` key containing the list of entity records.
* **Reconciliation**: **Adopt Explorer 1's Nested Object approach.** The project specification (`PROJECT.md`) states that the target database must have the *"same categories and hierarchy"* as the source config. If a category maps directly to a list, the original category-level metadata is lost. Keeping the metadata objects intact and introducing the `"Entities"` key is the only way to satisfy this contract and ensure category rules can be validated for preservation.
* **Expanded Database Structure**:
  ```json
  {
    "ContentForFunding": {
      "Universities": {
        "Why": "Research partnerships...",
        "Priority": "Critical",
        "Category_For_Company": ["Research Project"],
        "Entities": [ ... ]
      },
      "Government": {
        "Why": "Official grants...",
        "Priority": "Critical",
        "Structure": { ... },
        "Entities": [ ... ]
      }
    }
  }
  ```

### B. Uniqueness and Normalization Rules
* **Conflict**: Explorer 1 uses basic lowercase name checks. Explorer 2 implements a more robust normalizer that strips common corporate suffixes (Inc., Co., Ltd., LLC) and collapses non-alphanumeric characters.
* **Reconciliation**: **Adopt Explorer 2's robust normalizer.** Scraped and compiled lists often have minor variations in entity naming (e.g. "Flat6Labs", "Flat6Labs LLC", "Flat6Labs Co."). Without stripping these corporate suffixes and removing formatting characters, duplicates will slip through.
* **Website normalization**: Website URLs should have protocols (`http://`, `https://`), `www.`, and trailing slashes stripped to prevent duplicate domains (e.g., `http://example.com/` and `https://www.example.com` will both normalize to `example.com`).

### C. Placeholder Value Blacklist
* **Reconciliation**: Merge both lists into a highly comprehensive blacklist. We check for:
  - Exact match (case-insensitive): `tbd`, `todo`, `n/a`, `na`, `none`, `null`, `nil`, `-`, `--`, `undefined`, `temp`, `placeholder`.
  - Substring matches: `dummy`, `fake`, `placeholder`, `test@`.
  - Email/URL dummy domains: `example.com`, `test.com`, `email.com`, `domain.com`, `fake.com`.
  - Fake patterns in phone numbers: repeated digits like `0000000`, `1111111`, etc.

### D. Test Harness Framework
* **Reconciliation**: Propose a `pytest`-based test runner. The project already contains pytest configurations. Using a native pytest runner with `tmp_path` fixtures is clean, standard, and avoids committing mock files to the main database directories.

---

## 2. Schema Models

### A. Government Schema
Applied strictly to entities under the `"Government"` category.

| Field | Type | Required | Constraints / Validation |
|---|---|---|---|
| `Name` | `str` | Yes | Non-empty, unique |
| `Official_Website` | `str` | Yes | Valid URL format, unique |
| `Funding_Programs` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Last_Project_Link` | `str` | Yes | Valid URL format |
| `Eligibility` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Required_Documents` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Funding_Amount` | `str` | Yes | Non-empty text |
| `Application_Process` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Success_Stories` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Acceptance_Rate` | `str` | Yes | Non-empty text |
| `Expected_Duration` | `str` | Yes | Non-empty text |
| `Notes` | `str` | Yes | Non-empty text |
| `Steps_For_Any_Project_To_Get_Funded` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Steps_For_This_Project_To_Get_Funded` | `list[str]` | Yes | Non-empty list of non-placeholder strings |

### B. Standard Schema
Applied to entities under all other 17 categories (e.g., `Universities`, `Incubators`, `Venture Capital`).

| Field | Type | Required | Constraints / Validation |
|---|---|---|---|
| `Name` | `str` | Yes | Non-empty, unique |
| `Category` | `str` | Yes | Must match the name of the parent category |
| `Category_For_Company` | `list[str]` | Yes | Non-empty list of non-placeholder strings |
| `Priority` | `str` | Yes | Must match the priority of the parent category |
| `Country` | `str` | Yes | Non-empty text |
| `City` | `str` | Yes | Non-empty text |
| `Official_Website` | `str` | Yes | Valid URL format, unique |
| `Official_Email` | `str` | Yes | Valid email format, non-placeholder |
| `LinkedIn` | `str` | No | If non-empty, must be a valid LinkedIn URL |
| `Phone` | `str` | No | If non-empty, must match international phone formats |
| `Description` | `str` | Yes | Minimum 10 characters, non-placeholder |

---

## 3. Recommended Code Design: `verify_funding_db.py`

This script is dependency-free, running on Python 3 standard library.

```python
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
from urllib.parse import urlparse
from typing import List, Dict, Any, Set, Tuple

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
        n = re.sub(r'[^\w]', '', n)
        return n

    def normalize_url(self, url: str) -> str:
        if not isinstance(url, str):
            return ""
        u = url.strip().lower()
        u = re.sub(r'^https?://', '', u)
        u = re.sub(r'^www\.', '', u)
        return u.rstrip('/')

    def check_placeholder(self, value: Any, context: str) -> bool:
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
            if context.endswith(".Phone") and any(seq in val_clean for seq in ['123456', '000000', '111111', '999999']):
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
            if not URL_REGEX.match(value) or 'linkedin.com' not in value.lower():
                self.log_error(f"[{context}] Invalid LinkedIn URL: '{value}'")
                return False
        elif fmt == "phone":
            if not PHONE_REGEX.match(value):
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
                        self.check_placeholder(item, f"{context}.{field}[{i}]")
            
            # String Validation
            elif expected_type is str:
                if rule["required"] and not val.strip():
                    self.log_error(f"[{context}] Field '{field}' cannot be empty")
                    continue
                
                # Check description length
                if field == "Description" and len(val.strip()) < 10:
                    self.log_error(f"[{context}] Description field must be at least 10 characters long")
                
                # Placeholder checks
                self.check_placeholder(val, f"{context}.{field}")
                
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

        ref_categories = ref_data.get("ContentForFunding", {})
        if not ref_categories:
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

        if missing_keys or extra_keys:
            return False

        seen_names: Dict[str, Tuple[str, str]] = {} # norm_name -> (original_name, category)
        seen_urls: Dict[str, Tuple[str, str, str]] = {}  # norm_url -> (original_url, original_name, category)
        total_entity_count = 0

        # Detailed checks per category
        for cat_name, ref_meta in ref_categories.items():
            target_cat_obj = target_categories[cat_name]
            
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
                    if norm_name in seen_names:
                        prev_name, prev_cat = seen_names[norm_name]
                        self.log_error(f"Duplicate entity name: '{name}' in category '{cat_name}' is a duplicate of '{prev_name}' in '{prev_cat}'")
                    else:
                        seen_names[norm_name] = (name, cat_name)

                website = entity.get("Official_Website")
                if isinstance(website, str) and website.strip():
                    norm_url = self.normalize_url(website)
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
```

---

## 4. Recommended Test Runner Design: `test_verify_funding_db.py`

To test `verify_funding_db.py` without permanently adding mock files, the test runner uses `pytest` and generates valid and invalid databases dynamically using Python's `tmp_path` fixture.

```python
import subprocess
import json
import pytest
import sys
import os

# Complete reference config mimicking ContentForFunding.json structure
MOCK_REFERENCE_CONTENT = {
    "ContentForFunding": {
        "Universities": {
            "Why": "Partnerships",
            "Priority": "Critical",
            "Category_For_Company": ["Research Project"]
        },
        "Government": {
            "Why": "Grants",
            "Priority": "Critical",
            "Structure": {}
        }
    }
}

VALID_UNIVERSITY = {
    "Name": "Cairo University",
    "Category": "Universities",
    "Category_For_Company": ["Research Project"],
    "Priority": "Critical",
    "Country": "Egypt",
    "City": "Giza",
    "Official_Website": "https://cu.edu.eg",
    "Official_Email": "info@cu.edu.eg",
    "LinkedIn": "https://linkedin.com/school/cairo-university",
    "Phone": "+20235676105",
    "Description": "Cairo University description detailing research partnership options."
}

VALID_GOVERNMENT = {
    "Name": "Science & Technology Development Fund",
    "Official_Website": "https://stdf.eg",
    "Funding_Programs": ["Research Grant Program"],
    "Last_Project_Link": "https://stdf.eg/awards",
    "Eligibility": ["Egyptian researchers"],
    "Required_Documents": ["Research proposal", "Budget plan"],
    "Funding_Amount": "1,000,000 EGP",
    "Application_Process": ["Submit online", "Technical evaluation"],
    "Success_Stories": ["Funded 500+ national energy projects"],
    "Acceptance_Rate": "20%",
    "Expected_Duration": "6 months",
    "Notes": "Non-dilutive government funding.",
    "Steps_For_Any_Project_To_Get_Funded": ["Create portal account"],
    "Steps_For_This_Project_To_Get_Funded": ["Target clean energy program track"]
}


@pytest.fixture
def ref_file(tmp_path):
    f = tmp_path / "ContentForFunding.json"
    f.write_text(json.dumps(MOCK_REFERENCE_CONTENT), encoding='utf-8')
    return f


def run_validator(db_file, ref_file, min_count=2):
    # Runs the verify_funding_db.py script
    return subprocess.run([
        sys.executable, "verify_funding_db.py", 
        str(db_file), 
        "--reference-path", str(ref_file),
        "--min-count", str(min_count)
    ], capture_output=True, text=True, encoding='utf-8')


def test_fully_valid_db(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "valid_db.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 0
    assert "SUCCESS" in result.stdout


def test_missing_root_key(tmp_path, ref_file):
    target_content = {
        "WrongRoot": {}
    }
    db_file = tmp_path / "missing_root.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Root key 'ContentForFunding' is missing" in result.stderr


def test_missing_category(tmp_path, ref_file):
    # Omit Government category
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            }
        }
    }
    db_file = tmp_path / "missing_category.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Missing category in target file: 'Government'" in result.stderr


def test_metadata_mismatch(tmp_path, ref_file):
    # Alter the priority metadata of Universities from 'Critical' to 'Low'
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Low",  # MISMATCH
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "mismatch.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "metadata mismatch. Field 'Priority' expected 'Critical'" in result.stderr


def test_missing_required_field(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    del bad_univ["Country"]  # Country is required
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [bad_univ]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "missing_field.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "Missing required field: 'Country'" in result.stderr


def test_invalid_type(tmp_path, ref_file):
    bad_gov = VALID_GOVERNMENT.copy()
    bad_gov["Funding_Programs"] = "Should be list, but string"
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [bad_gov]
            }
        }
    }
    db_file = tmp_path / "bad_type.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "must be a list, got str" in result.stderr


def test_placeholder_validation(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    bad_univ["Official_Email"] = "fake@email.com"  # Placeholder email
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [bad_univ]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "placeholder.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=1)
    assert result.returncode == 1
    assert "Placeholder pattern detected: 'fake@email.com'" in result.stderr


def test_duplicate_name(tmp_path, ref_file):
    # Two entities under different categories but with identical normalized names
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Name"] = "Cairo University LLC"  # Normalizes to 'cairouniversity' same as VALID_UNIVERSITY
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [dup_gov]
            }
        }
    }
    db_file = tmp_path / "dup_name.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate entity name: 'Cairo University LLC'" in result.stderr


def test_duplicate_website(tmp_path, ref_file):
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Official_Website"] = "http://www.cu.edu.eg/"  # Normalizes to 'cu.edu.eg' same as VALID_UNIVERSITY
    
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [dup_gov]
            }
        }
    }
    db_file = tmp_path / "dup_website.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate website:" in result.stderr


def test_insufficient_entity_count(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": {
                "Why": "Partnerships",
                "Priority": "Critical",
                "Category_For_Company": ["Research Project"],
                "Entities": [VALID_UNIVERSITY]
            },
            "Government": {
                "Why": "Grants",
                "Priority": "Critical",
                "Structure": {},
                "Entities": [VALID_GOVERNMENT]
            }
        }
    }
    db_file = tmp_path / "insufficient_count.json"
    db_file.write_text(json.dumps(target_content), encoding='utf-8')
    
    # Require 5, but we only have 2
    result = run_validator(db_file, ref_file, min_count=5)
    assert result.returncode == 1
    assert "Total entity count 2 is less than required minimum 5" in result.stderr
```

---

## 5. Dummy Datasets for Manual Validation Testing

The files below can be written to disk to verify the CLI execution behavior of `verify_funding_db.py`.

### A. Valid Mock Data Structure (`ContentForFunding_Expanded_Valid_Dummy.json`)
*Note: To run successfully with this mock file, either pass `--min-count 2` to the script or populate it with 150 entities.*

```json
{
  "ContentForFunding": {
    "Universities": {
      "Why": "Partnerships",
      "Priority": "Critical",
      "Category_For_Company": ["Research Project"],
      "Entities": [
        {
          "Name": "Stanford University",
          "Category": "Universities",
          "Category_For_Company": ["Research Project"],
          "Priority": "Critical",
          "Country": "USA",
          "City": "Stanford",
          "Official_Website": "https://stanford.edu",
          "Official_Email": "info@stanford.edu",
          "LinkedIn": "https://linkedin.com/school/stanford-university",
          "Phone": "+16507232300",
          "Description": "Stanford University is a private research university in Stanford, California."
        }
      ]
    },
    "Research Centers": {
      "Why": "Scientific collaboration, publications, funded research.",
      "Priority": "Critical",
      "Category_For_Company": [
        "Research Project",
        "AI Research",
        "Academic Project"
      ],
      "Entities": []
    },
    "Cultural Centers": {
      "Why": "Innovation programs, educational grants, startup support, hackathons.",
      "Priority": "High",
      "Category_For_Company": [
        "Education",
        "Social Impact",
        "Research",
        "Startup"
      ],
      "Entities": []
    },
    "Innovation Hubs": {
      "Why": "Incubation, acceleration, mentoring, networking.",
      "Priority": "Critical",
      "Category_For_Company": [
        "Startup",
        "AI Startup",
        "DeepTech"
      ],
      "Entities": []
    },
    "Incubators": {
      "Why": "Pre-seed support and startup validation.",
      "Priority": "Critical",
      "Category_For_Company": [
        "Startup",
        "AI Startup"
      ],
      "Entities": []
    },
    "Accelerators": {
      "Why": "Investment, scaling, investor access.",
      "Priority": "Critical",
      "Category_For_Company": [
        "Startup",
        "AI Startup",
        "Scale-up"
      ],
      "Entities": []
    },
    "Educational Organizations": {
      "Why": "Learning partnerships and educational deployment.",
      "Priority": "High",
      "Category_For_Company": [
        "EdTech",
        "Education Platform"
      ],
      "Entities": []
    },
    "Educational Centers": {
      "Why": "Deploy platform to students and instructors.",
      "Priority": "Medium",
      "Category_For_Company": [
        "EdTech"
      ],
      "Entities": []
    },
    "NGOs": {
      "Why": "Education, youth empowerment, AI literacy.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Social Impact",
        "Education"
      ],
      "Entities": []
    },
    "International Organizations": {
      "Why": "Large grants and international partnerships.",
      "Priority": "High",
      "Category_For_Company": [
        "Research",
        "Education",
        "Innovation"
      ],
      "Entities": []
    },
    "Competitions": {
      "Why": "Prize money and visibility.",
      "Priority": "High",
      "Category_For_Company": [
        "Startup",
        "Research",
        "AI"
      ],
      "Entities": []
    },
    "Hackathons": {
      "Why": "Networking and sponsorship.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Startup"
      ],
      "Entities": []
    },
    "Awards": {
      "Why": "Recognition and financial prizes.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Startup",
        "Research"
      ],
      "Entities": []
    },
    "Fellowships": {
      "Why": "Research funding and leadership programs.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Research",
        "Education"
      ],
      "Entities": []
    },
    "Investors": {
      "Why": "Seed and Pre-seed funding.",
      "Priority": "High",
      "Category_For_Company": [
        "Startup"
      ],
      "Entities": []
    },
    "Angel Networks": {
      "Why": "Early investment.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Startup"
      ],
      "Entities": []
    },
    "Venture Capital": {
      "Why": "Growth funding.",
      "Priority": "Medium",
      "Category_For_Company": [
        "Scale-up"
      ],
      "Entities": []
    },
    "Government": {
      "Why": "Official grants and national funding programs.",
      "Priority": "Critical",
      "Entities": [
        {
          "Name": "National Science Foundation",
          "Official_Website": "https://nsf.gov",
          "Funding_Programs": ["SBIR", "STTR"],
          "Last_Project_Link": "https://nsf.gov/awards",
          "Eligibility": ["US small businesses", "US citizens"],
          "Required_Documents": ["Proposal pitch deck", "Financial audit reports"],
          "Funding_Amount": "$256,000",
          "Application_Process": ["Submit portal application", "Double-blind peer review"],
          "Success_Stories": ["Google and Qualcomm received early NSF support"],
          "Acceptance_Rate": "15%",
          "Expected_Duration": "6-12 months",
          "Notes": "Great source of non-dilutive capital.",
          "Steps_For_Any_Project_To_Get_Funded": ["Verify SAM.gov registration"],
          "Steps_For_This_Project_To_Get_Funded": ["Identify EdTech solicitation track"]
        }
      ]
    }
  }
}
```

### B. Invalid Mock Data Structure (`ContentForFunding_Expanded_Invalid_Dummy.json`)

```json
{
  "ContentForFunding": {
    "Universities": {
      "Why": "Partnerships",
      "Priority": "Low", 
      "Category_For_Company": ["Research Project"],
      "Entities": [
        {
          "Name": "TBD", 
          "Category": "Incubators", 
          "Category_For_Company": ["Research Project"],
          "Priority": "Critical",
          "Country": "USA",
          "City": "Stanford",
          "Official_Website": "stanford.edu", 
          "Official_Email": "info@example.com", 
          "LinkedIn": "https://linkedin.com/in/stanford",
          "Phone": "0000000", 
          "Description": "Too short" 
        }
      ]
    },
    "Research Centers": {
      "Why": "Scientific collaboration, publications, funded research.",
      "Priority": "Critical",
      "Category_For_Company": ["Research Project"],
      "Entities": []
    },
    "Government": {
      "Why": "Official grants and national funding programs.",
      "Priority": "Critical",
      "Entities": [
        {
          "Name": "National Science Foundation",
          "Official_Website": "https://nsf.gov",
          "Funding_Programs": "This should be a list", 
          "Last_Project_Link": "https://nsf.gov/awards",
          "Eligibility": ["US small businesses"],
          "Required_Documents": ["Proposal pitch deck"],
          "Funding_Amount": "$256,000",
          "Application_Process": ["Submit application"],
          "Success_Stories": ["Google and Qualcomm"],
          "Acceptance_Rate": "15%",
          "Expected_Duration": "6-12 months",
          "Notes": "Notes",
          "Steps_For_Any_Project_To_Get_Funded": ["Verify SAM.gov"],
          "Steps_For_This_Project_To_Get_Funded": ["Identify EdTech track"]
        }
      ]
    }
  }
}
```
*Note: This file contains multiple categories missing, a metadata mismatch (`Priority` value `Low` instead of `Critical`), type schema error (`Funding_Programs` as `str` instead of `list`), placeholder values, categories cross-reference mismatch, missing http schema, dummy emails, fake phones, and short descriptions.*
