# Technical Analysis and Design: E2E Verification Track

This document details the schema models, proposed python script `verify_funding_db.py`, test runner `test_verify_funding_db.py`, and dummy dataset designs to satisfy the End-to-End Testing requirements.

---

## 1. Schema Models

The verification track governs two distinct entity schemas within the database:

### A. Government Schema
Applied only to entities classified under the `"Government"` category.

| Field | Type | Format / Constraints |
|---|---|---|
| `Name` | `str` | Non-empty, unique name |
| `Official_Website` | `str` | Valid HTTP/HTTPS URL, unique |
| `Funding_Programs` | `list[str]` | Non-empty list of non-placeholder strings |
| `Last_Project_Link` | `str` | Valid HTTP/HTTPS URL |
| `Eligibility` | `list[str]` | Non-empty list of non-placeholder strings |
| `Required_Documents` | `list[str]` | Non-empty list of non-placeholder strings |
| `Funding_Amount` | `str` | Non-empty text |
| `Application_Process` | `list[str]` | Non-empty list of non-placeholder strings |
| `Success_Stories` | `list[str]` | Non-empty list of non-placeholder strings |
| `Acceptance_Rate` | `str` | Non-empty text |
| `Expected_Duration` | `str` | Non-empty text |
| `Notes` | `str` | Non-empty text |
| `Steps_For_Any_Project_To_Get_Funded` | `list[str]` | Non-empty list of non-placeholder strings |
| `Steps_For_This_Project_To_Get_Funded` | `list[str]` | Non-empty list of non-placeholder strings |

### B. Standard Schema
Applied to all entities under categories *other than* `"Government"`.

| Field | Type | Format / Constraints |
|---|---|---|
| `Name` | `str` | Non-empty, unique name |
| `Category` | `str` | Must match the actual category key name |
| `Category_For_Company` | `list[str]` | Non-empty list of non-placeholder strings |
| `Priority` | `str` | Non-empty text (e.g. Critical, High, Medium, Low) |
| `Country` | `str` | Non-empty country name |
| `City` | `str` | Non-empty city name |
| `Official_Website` | `str` | Valid HTTP/HTTPS URL, unique |
| `Official_Email` | `str` | Valid email address |
| `LinkedIn` | `str` (Optional) | If present, must be empty or a valid LinkedIn URL |
| `Phone` | `str` (Optional) | If present, must be empty or a valid phone format |
| `Description` (or `Why`) | `str` | Non-empty description or justification |

---

## 2. Python Script: `verify_funding_db.py`

This script validates JSON file presence, category integrity against `ContentForFunding.json`, schema conformity, placeholder exclusion, global de-duplication, and total entity count.

```python
#!/usr/bin/env python3
"""
Automated Verification and Validation Script for Funding Database.
Validates file structure, schema conformity, duplicate records, and placeholder values.
"""

import os
import sys
import json
import argparse
import re
from urllib.parse import urlparse

# Global validation regexes
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

EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake']
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com']

# Schemas definition
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

def is_valid_url(url):
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    if not (parsed.scheme in ('http', 'https') and parsed.netloc):
        return False
    return bool(URL_REGEX.match(url))

def is_valid_email(email):
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email))

def is_valid_phone(phone):
    if not phone:
        return True
    if not isinstance(phone, str):
        return False
    return bool(PHONE_REGEX.match(phone))

def is_placeholder(val):
    if not isinstance(val, str):
        return False
    val_clean = val.strip().lower()
    if val_clean in EXACT_PLACEHOLDERS:
        return True
    for kw in SUBSTRING_PLACEHOLDERS:
        if kw in val_clean:
            return True
    if TBD_REGEX.search(val):
        return True
    if '@' in val_clean:
        parts = val_clean.split('@')
        if len(parts) == 2:
            username, domain = parts
            if domain in DUMMY_DOMAINS or 'fake' in username or 'dummy' in username:
                return True
    if any(d in val_clean for d in DUMMY_DOMAINS):
        return True
    if any(p in val_clean for p in ['123456', '000000', '111111', '999999']):
        return True
    return False

def normalize_name(name):
    if not isinstance(name, str):
        return ""
    n = name.strip().lower()
    suffixes = [
        r'\binc\.?\b', r'\bco\.?\b', r'\bltd\.?\b', r'\bllc\.?\b',
        r'\bcorp\.?\b', r'\bcorporation\b', r'\bincorporated\b', r'\bcompany\b'
    ]
    for suffix in suffixes:
        n = re.sub(suffix, '', n)
    # Strip non-alphanumeric characters and collapse spaces
    n = re.sub(r'[^\w]', '', n)
    return n

def normalize_url(url):
    if not isinstance(url, str):
        return ""
    u = url.strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    u = u.rstrip('/')
    return u

def validate_entity(entity, schema, category, entity_index, errors):
    entity_name = entity.get("Name", f"Index {entity_index}")
    
    # Check for unexpected fields
    for key in entity:
        if key not in schema and not (key == "Why" and "Description" in schema):
            errors.append(f"[{category}] Entity '{entity_name}': Unexpected field '{key}'")

    for field, rule in schema.items():
        # Support 'Why' as an alias for 'Description'
        current_field = field
        if field == "Description" and "Description" not in entity and "Why" in entity:
            current_field = "Why"
            
        if rule["required"] and current_field not in entity:
            errors.append(f"[{category}] Entity '{entity_name}': Missing required field '{field}'")
            continue
            
        if current_field not in entity:
            continue
            
        val = entity[current_field]
        
        # Check type
        expected_type = rule["type"]
        if expected_type == list:
            if not isinstance(val, list):
                errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' must be a list, got {type(val).__name__}")
                continue
            item_type = rule["item_type"]
            for idx, item in enumerate(val):
                if not isinstance(item, item_type):
                    errors.append(f"[{category}] Entity '{entity_name}': Element {idx} in field '{current_field}' must be a {item_type.__name__}, got {type(item).__name__}")
                elif is_placeholder(item):
                    errors.append(f"[{category}] Entity '{entity_name}': Element {idx} in field '{current_field}' has placeholder value '{item}'")
        else:
            # For optional fields, empty string or None can skip format checking if it's not required
            if not rule["required"] and (val is None or val == ""):
                continue
                
            if not isinstance(val, expected_type):
                errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' must be a {expected_type.__name__}, got {type(val).__name__}")
                continue
                
            if is_placeholder(val):
                errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has placeholder value '{val}'")
                
            # Format verification
            fmt = rule.get("format")
            if fmt == "url":
                if not is_valid_url(val):
                    errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has invalid URL format '{val}'")
            elif fmt == "email":
                if not is_valid_email(val):
                    errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has invalid email format '{val}'")
            elif fmt == "linkedin":
                if not is_valid_url(val) or 'linkedin.com' not in val.lower():
                    errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has invalid LinkedIn URL '{val}'")
            elif fmt == "phone":
                if not is_valid_phone(val):
                    errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has invalid phone format '{val}'")

        # Category field cross-reference check
        if current_field == "Category" and val != category:
            errors.append(f"[{category}] Entity '{entity_name}': 'Category' field '{val}' does not match the actual category key '{category}'")

def print_errors_and_exit(errors):
    if errors:
        print("\n--- Verification Failed ---", file=sys.stderr)
        print(f"Found {len(errors)} validation errors:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print("\n---------------------------", file=sys.stderr)
        sys.exit(1)
    else:
        print("Verification Succeeded! The database is clean and compliant.", file=sys.stdout)
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Verify Funding Database JSON file.")
    parser.add_argument("db_path", nargs="?", default="Funding/ContentForFunding_Expanded.json",
                        help="Path to the expanded funding JSON file to verify.")
    parser.add_argument("--reference-path", default="Funding/ContentForFunding.json",
                        help="Path to the reference content for funding JSON file.")
    parser.add_argument("--min-count", type=int, default=150,
                        help="Minimum number of total entities required (default: 150).")
    args = parser.parse_args()

    errors = []

    # 1. Verify Reference File
    if not os.path.exists(args.reference_path):
        print(f"Reference file not found: {args.reference_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.reference_path, "r", encoding="utf-8") as f:
            ref_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing reference JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    ref_categories_root = ref_data.get("ContentForFunding", {})
    if not ref_categories_root:
        print("Reference file has missing or empty 'ContentForFunding' root key.", file=sys.stderr)
        sys.exit(1)
    ref_categories = set(ref_categories_root.keys())

    # 2. Target File Integrity Checks
    if not os.path.exists(args.db_path):
        print(f"Target file not found: {args.db_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.db_path, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in target file: {e}", file=sys.stderr)
        sys.exit(1)

    target_categories_root = target_data.get("ContentForFunding")
    if target_categories_root is None:
        errors.append("Root key 'ContentForFunding' is missing in target file.")
        print_errors_and_exit(errors)

    if not isinstance(target_categories_root, dict):
        errors.append("Root value under 'ContentForFunding' must be a JSON object.")
        print_errors_and_exit(errors)

    target_categories = set(target_categories_root.keys())

    # 3. Category Consistency Checks
    missing_cats = ref_categories - target_categories
    extra_cats = target_categories - ref_categories

    for cat in missing_cats:
        errors.append(f"Missing category in target file: '{cat}'")
    for cat in extra_cats:
        errors.append(f"Unexpected category in target file: '{cat}'")

    if missing_cats or extra_cats:
        print_errors_and_exit(errors)

    # 4. Schema and Content Inspection
    seen_names = {}
    seen_urls = {}
    total_entities = 0

    for category, entities in target_categories_root.items():
        if not isinstance(entities, list):
            errors.append(f"Category '{category}' must be a list of entities, got {type(entities).__name__}")
            continue

        schema = GOVERNMENT_SCHEMA if category == "Government" else STANDARD_SCHEMA

        for idx, entity in enumerate(entities):
            total_entities += 1
            if not isinstance(entity, dict):
                errors.append(f"[{category}] Entity at index {idx} must be a JSON object, got {type(entity).__name__}")
                continue

            # Check for name duplicates
            name = entity.get("Name")
            if name:
                norm_name = normalize_name(name)
                if norm_name in seen_names:
                    prev_name, prev_cat = seen_names[norm_name]
                    errors.append(f"Duplicate entity name detected: '{name}' in category '{category}' is a duplicate of '{prev_name}' in category '{prev_cat}'")
                else:
                    seen_names[norm_name] = (name, category)

            # Check for website duplicates
            website = entity.get("Official_Website")
            if website:
                norm_url = normalize_url(website)
                if norm_url in seen_urls:
                    prev_url, prev_name, prev_cat = seen_urls[norm_url]
                    errors.append(f"Duplicate website URL detected: '{website}' for '{name}' in '{category}' is a duplicate of '{prev_url}' for '{prev_name}' in '{prev_cat}'")
                else:
                    seen_urls[norm_url] = (website, name, category)

            # Run field-by-field schema validation
            validate_entity(entity, schema, category, idx, errors)

    # 5. Entity Count Constraint Check
    if total_entities < args.min_count:
        errors.append(f"Total entity count is {total_entities}, which is less than the required minimum of {args.min_count}.")

    print_errors_and_exit(errors)

if __name__ == "__main__":
    main()
```

---

## 3. Test Runner Design: `test_verify_funding_db.py`

To test `verify_funding_db.py` without permanently adding mock files, the test suite generates valid and invalid databases dynamically using Python's `tmp_path` fixture.

```python
import subprocess
import json
import pytest
import sys

BASE_REF_CONTENT = {
    "ContentForFunding": {
        "Universities": {
            "Why": "Partnerships",
            "Priority": "Critical",
            "Category_For_Company": ["Research"]
        },
        "Government": {
            "Why": "Grants",
            "Priority": "Critical",
            "Structure": {}
        }
    }
}

VALID_UNIVERSITY = {
    "Name": "Stanford University",
    "Category": "Universities",
    "Category_For_Company": ["Research"],
    "Priority": "Critical",
    "Country": "USA",
    "City": "Stanford",
    "Official_Website": "https://stanford.edu",
    "Official_Email": "info@stanford.edu",
    "LinkedIn": "https://linkedin.com/school/stanford",
    "Phone": "+16507232300",
    "Description": "Stanford University description details."
}

VALID_GOVERNMENT = {
    "Name": "National Science Foundation",
    "Official_Website": "https://nsf.gov",
    "Funding_Programs": ["SBIR"],
    "Last_Project_Link": "https://nsf.gov/award",
    "Eligibility": ["US Entities"],
    "Required_Documents": ["Proposal"],
    "Funding_Amount": "$250k",
    "Application_Process": ["Fastlane submission"],
    "Success_Stories": ["Google"],
    "Acceptance_Rate": "15%",
    "Expected_Duration": "6 months",
    "Notes": "Notes on funding",
    "Steps_For_Any_Project_To_Get_Funded": ["Prepare proposal"],
    "Steps_For_This_Project_To_Get_Funded": ["Prepare Smart & Connected Communities pitch"]
}

@pytest.fixture
def ref_file(tmp_path):
    f = tmp_path / "ContentForFunding.json"
    f.write_text(json.dumps(BASE_REF_CONTENT))
    return f

def run_validator(db_file, ref_file, min_count=2):
    return subprocess.run([
        sys.executable, "verify_funding_db.py", 
        str(db_file), 
        "--reference-path", str(ref_file),
        "--min-count", str(min_count)
    ], capture_output=True, text=True)

def test_fully_valid_db(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY],
            "Government": [VALID_GOVERNMENT]
        }
    }
    db_file = tmp_path / "valid.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 0
    assert "Verification Succeeded" in result.stdout

def test_missing_root_key(tmp_path, ref_file):
    target_content = {
        "WrongRoot": {}
    }
    db_file = tmp_path / "missing_root.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Root key 'ContentForFunding' is missing" in result.stderr

def test_missing_category(tmp_path, ref_file):
    # Missing 'Government' category
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY]
        }
    }
    db_file = tmp_path / "missing_cat.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=0)
    assert result.returncode == 1
    assert "Missing category in target file: 'Government'" in result.stderr

def test_missing_required_field(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    del bad_univ["Country"] # Country is required
    
    target_content = {
        "ContentForFunding": {
            "Universities": [bad_univ],
            "Government": [VALID_GOVERNMENT]
        }
    }
    db_file = tmp_path / "missing_field.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Missing required field 'Country'" in result.stderr

def test_invalid_field_type(tmp_path, ref_file):
    bad_gov = VALID_GOVERNMENT.copy()
    bad_gov["Eligibility"] = "Should be a list, not string"
    
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY],
            "Government": [bad_gov]
        }
    }
    db_file = tmp_path / "bad_type.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "must be a list, got str" in result.stderr

def test_placeholder_value(tmp_path, ref_file):
    bad_univ = VALID_UNIVERSITY.copy()
    bad_univ["Name"] = "TBD" # Placeholder
    
    target_content = {
        "ContentForFunding": {
            "Universities": [bad_univ],
            "Government": [VALID_GOVERNMENT]
        }
    }
    db_file = tmp_path / "placeholder.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "has placeholder value 'TBD'" in result.stderr

def test_duplicate_name(tmp_path, ref_file):
    # Same name under different categories
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Name"] = "Stanford University" # Normalizes same as VALID_UNIVERSITY name
    
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY],
            "Government": [dup_gov]
        }
    }
    db_file = tmp_path / "dup_name.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate entity name detected" in result.stderr

def test_duplicate_website(tmp_path, ref_file):
    dup_gov = VALID_GOVERNMENT.copy()
    dup_gov["Official_Website"] = "http://www.stanford.edu/" # Normalizes to stanford.edu
    
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY],
            "Government": [dup_gov]
        }
    }
    db_file = tmp_path / "dup_website.json"
    db_file.write_text(json.dumps(target_content))
    
    result = run_validator(db_file, ref_file, min_count=2)
    assert result.returncode == 1
    assert "Duplicate website URL detected" in result.stderr

def test_insufficient_entity_count(tmp_path, ref_file):
    target_content = {
        "ContentForFunding": {
            "Universities": [VALID_UNIVERSITY],
            "Government": [VALID_GOVERNMENT]
        }
    }
    db_file = tmp_path / "insufficient.json"
    db_file.write_text(json.dumps(target_content))
    
    # We require 5 but only have 2
    result = run_validator(db_file, ref_file, min_count=5)
    assert result.returncode == 1
    assert "is less than the required minimum of 5" in result.stderr
```

---

## 4. Specification of Dummy Test Files

### A. Valid Dummy Data Structure (`dummy_valid.json`)
Requires `--min-count 2` (or lower) for validation pass when running locally for unit testing, or containing 150+ mock entries for default run.

```json
{
  "ContentForFunding": {
    "Universities": [
      {
        "Name": "Stanford University",
        "Category": "Universities",
        "Category_For_Company": ["Research Project", "AI Startup"],
        "Priority": "Critical",
        "Country": "USA",
        "City": "Stanford",
        "Official_Website": "https://stanford.edu",
        "Official_Email": "info@stanford.edu",
        "LinkedIn": "https://linkedin.com/school/stanford-university",
        "Phone": "+16507232300",
        "Description": "Stanford University is a private research university in Stanford, California."
      }
    ],
    "Research Centers": [],
    "Cultural Centers": [],
    "Innovation Hubs": [],
    "Incubators": [],
    "Accelerators": [],
    "Educational Organizations": [],
    "Educational Centers": [],
    "NGOs": [],
    "International Organizations": [],
    "Competitions": [],
    "Hackathons": [],
    "Awards": [],
    "Fellowships": [],
    "Investors": [],
    "Angel Networks": [],
    "Venture Capital": [],
    "Government": [
      {
        "Name": "National Science Foundation",
        "Official_Website": "https://nsf.gov",
        "Funding_Programs": ["SBIR", "STTR"],
        "Last_Project_Link": "https://nsf.gov/awards",
        "Eligibility": ["Small businesses", "US citizens"],
        "Required_Documents": ["Proposal", "Budget"],
        "Funding_Amount": "$256,000",
        "Application_Process": ["Online application", "Peer review"],
        "Success_Stories": ["Google started with NSF funding"],
        "Acceptance_Rate": "15%",
        "Expected_Duration": "6-12 months",
        "Notes": "Great pre-seed non-dilutive capital.",
        "Steps_For_Any_Project_To_Get_Funded": ["Register on sam.gov"],
        "Steps_For_This_Project_To_Get_Funded": ["Target SBIR educational portal"]
      }
    ]
  }
}
```

### B. Invalid Dummy Data Structure (`dummy_invalid.json`)
Used to verify validator catchability of critical rules (placeholder, missing categories, and schema mismatch).

```json
{
  "ContentForFunding": {
    "Universities": [
      {
        "Name": "TBD", 
        "Category": "Universities",
        "Category_For_Company": ["AI Startup"],
        "Priority": "Critical",
        "Country": "Egypt",
        "City": "Cairo",
        "Official_Website": "invalid-url-format", 
        "Official_Email": "fake@email.com", 
        "LinkedIn": "",
        "Phone": "0000000", 
        "Description": "This contains placeholder details"
      }
    ],
    "Government": [
      {
        "Name": "Egypt ITIDA",
        "Official_Website": "https://itida.gov.eg",
        "Funding_Programs": "Should be list, but is a string", 
        "Last_Project_Link": "https://itida.gov.eg/projects",
        "Eligibility": ["Egyptian startups"],
        "Required_Documents": ["Company registration"],
        "Funding_Amount": "100k EGP",
        "Application_Process": ["Submit proposal"],
        "Success_Stories": ["Several companies funded"],
        "Acceptance_Rate": "30%",
        "Expected_Duration": "3 months",
        "Notes": "Great local funding option.",
        "Steps_For_Any_Project_To_Get_Funded": ["Apply online"],
        "Steps_For_This_Project_To_Get_Funded": ["Follow ITIDA rules"]
      }
    ]
  }
}
```
*Note: Categories "Research Centers", "Cultural Centers", etc. are omitted in `dummy_invalid.json`, which will trigger Category Consistency failures.*
