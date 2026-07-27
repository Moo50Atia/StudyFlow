import json
import re
import sys
from urllib.parse import urlparse

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
    for key in entity:
        if key not in schema and not (key == "Why" and "Description" in schema):
            errors.append(f"[{category}] Entity '{entity_name}': Unexpected field '{key}'")
    for field, rule in schema.items():
        current_field = field
        if field == "Description" and "Description" not in entity and "Why" in entity:
            current_field = "Why"
        if rule["required"] and current_field not in entity:
            errors.append(f"[{category}] Entity '{entity_name}': Missing required field '{field}'")
            continue
        if current_field not in entity:
            continue
        val = entity[current_field]
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
            if not rule["required"] and (val is None or val == ""):
                continue
            if not isinstance(val, expected_type):
                errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' must be a {expected_type.__name__}, got {type(val).__name__}")
                continue
            if is_placeholder(val):
                errors.append(f"[{category}] Entity '{entity_name}': Field '{current_field}' has placeholder value '{val}'")
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
        if current_field == "Category" and val != category:
            errors.append(f"[{category}] Entity '{entity_name}': 'Category' field '{val}' does not match the actual category key '{category}'")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path")
    parser.add_argument("--min-count", type=int, default=80)
    args = parser.parse_args()
    
    errors = []
    try:
        with open(args.db_path, "r", encoding="utf-8") as f:
            target_data = json.load(f)
    except Exception as e:
        print(f"Error reading/parsing target file: {e}")
        sys.exit(1)
        
    target_categories_root = target_data.get("ContentForFunding")
    if not target_categories_root:
        print("Root key 'ContentForFunding' is missing or empty.")
        sys.exit(1)
        
    seen_names = {}
    seen_urls = {}
    total_entities = 0
    
    for category, entities in target_categories_root.items():
        if not isinstance(entities, list):
            errors.append(f"Category '{category}' must be a list of entities")
            continue
        schema = GOVERNMENT_SCHEMA if category == "Government" else STANDARD_SCHEMA
        for idx, entity in enumerate(entities):
            total_entities += 1
            name = entity.get("Name")
            if name:
                norm_name = normalize_name(name)
                if norm_name in seen_names:
                    errors.append(f"Duplicate name: '{name}' in '{category}' and '{seen_names[norm_name]}'")
                else:
                    seen_names[norm_name] = category
            website = entity.get("Official_Website")
            if website:
                norm_url = normalize_url(website)
                if norm_url in seen_urls:
                    errors.append(f"Duplicate website: '{website}' in '{category}' and '{seen_urls[norm_url]}'")
                else:
                    seen_urls[norm_url] = category
            validate_entity(entity, schema, category, idx, errors)
            
    if total_entities < args.min_count:
        errors.append(f"Total entity count is {total_entities}, expected at least {args.min_count}")
        
    if errors:
        print(f"FAILED: Found {len(errors)} errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Verified {total_entities} entities successfully. No errors.")
        sys.exit(0)

if __name__ == "__main__":
    main()
