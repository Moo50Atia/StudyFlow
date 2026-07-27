import os
import sys
import json
import re
from typing import Any

# Normalization functions matching verify_funding_db.py
def normalize_name(name: str) -> str:
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

def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""
    u = url.strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    return u.rstrip('/')

# Placeholder detection matching verify_funding_db.py
EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake', 'test@']
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com', 'fake.com']
FAKE_PHONE_SUBSTRINGS = ['123456', '000000', '111111', '999999']
TBD_REGEX = re.compile(r'\b(tbd|todo|n/a)\b', re.IGNORECASE)

def is_placeholder(val: str, field_name: str = None) -> bool:
    if not isinstance(val, str):
        return False
    val_clean = val.strip().lower()
    if val_clean in EXACT_PLACEHOLDERS:
        return True
    for kw in SUBSTRING_PLACEHOLDERS:
        if kw in val_clean:
            return True
    if TBD_REGEX.search(val_clean):
        return True
    if any(dom in val_clean for dom in DUMMY_DOMAINS):
        return True
    if field_name == "Phone" and any(seq in val_clean for seq in FAKE_PHONE_SUBSTRINGS):
        return True
    return False

def clean_placeholder(val: Any, field_name: str = None) -> Any:
    if isinstance(val, str):
        if is_placeholder(val, field_name):
            return ""
    elif isinstance(val, list):
        return [clean_placeholder(item, field_name) for item in val if not is_placeholder(item, field_name)]
    return val

def merge_entities(ent1: dict, ent2: dict, is_govt: bool) -> dict:
    merged = {}
    all_keys = set(ent1.keys()) | set(ent2.keys())
    
    for key in all_keys:
        val1 = ent1.get(key)
        val2 = ent2.get(key)
        
        # Clean placeholders
        val1 = clean_placeholder(val1, key)
        val2 = clean_placeholder(val2, key)
        
        if val1 is not None and val1 != "" and val1 != []:
            if val2 is not None and val2 != "" and val2 != []:
                # Both exist, merge
                if isinstance(val1, list) and isinstance(val2, list):
                    # Combine lists, preserve order, remove duplicates
                    seen = set()
                    new_list = []
                    for item in val1 + val2:
                        if item not in seen:
                            seen.add(item)
                            new_list.append(item)
                    merged[key] = new_list
                elif isinstance(val1, str) and isinstance(val2, str):
                    if val1.strip().lower() == val2.strip().lower():
                        # Capitalization choice
                        up1 = sum(1 for c in val1 if c.isupper())
                        up2 = sum(1 for c in val2 if c.isupper())
                        merged[key] = val1 if up1 >= up2 else val2
                    else:
                        if key == "Description":
                            merged[key] = val1 if len(val1) >= len(val2) else val2
                        elif key == "Official_Website":
                            # Prefer starting with http
                            if val1.startswith("http") and not val2.startswith("http"):
                                merged[key] = val1
                            else:
                                merged[key] = val2 if val2.startswith("http") else val1
                        else:
                            merged[key] = val1
                else:
                    merged[key] = val1
            else:
                merged[key] = val1
        else:
            merged[key] = val2
            
    return merged

def run():
    funding_path = "Funding/ContentForFunding.json"
    egypt_path = "Funding/egypt_mena_entities.json"
    global_path = "Funding/global_entities.json"
    expanded_path = "Funding/ContentForFunding_Expanded.json"
    
    # Check that input files exist
    for p in [funding_path, egypt_path, global_path]:
        if not os.path.exists(p):
            print(f"Error: {p} does not exist", file=sys.stderr)
            sys.exit(1)
            
    # Load categories metadata
    with open(funding_path, "r", encoding="utf-8") as f:
        ref_data = json.load(f)
    ref_cats = ref_data["ContentForFunding"]
    
    # Initialize output data structure
    expanded_content = {}
    for cat_name, cat_meta in ref_cats.items():
        expanded_content[cat_name] = {
            "Why": cat_meta["Why"],
            "Priority": cat_meta["Priority"]
        }
        if "Category_For_Company" in cat_meta:
            expanded_content[cat_name]["Category_For_Company"] = cat_meta["Category_For_Company"]
        if "Structure" in cat_meta:
            expanded_content[cat_name]["Structure"] = cat_meta["Structure"]
        expanded_content[cat_name]["Entities"] = []
        
    # Read egypt_mena_entities.json
    with open(egypt_path, "r", encoding="utf-8") as f:
        egypt_data = json.load(f)
    egypt_content = egypt_data["ContentForFunding"]
    
    # Read global_entities.json
    with open(global_path, "r", encoding="utf-8") as f:
        global_entities = json.load(f)
        
    # Standardize and collect all entities
    # Format of each item: (entity_dict, category_name, source)
    all_raw_entities = []
    
    # Process Egypt/MENA
    for cat_name, entities in egypt_content.items():
        for ent in entities:
            # Egypt entities might not have category or metadata matching, let's add it
            ent_copy = ent.copy()
            ent_copy["Category"] = cat_name
            all_raw_entities.append((ent_copy, cat_name, "Egypt/MENA"))
            
    # Process Global
    for ent in global_entities:
        cat_name = ent.get("Category")
        if not cat_name:
            print(f"Warning: Global entity without category: {ent.get('Name')}")
            continue
        if cat_name not in ref_cats:
            print(f"Warning: Global entity has invalid category '{cat_name}': {ent.get('Name')}")
            continue
        all_raw_entities.append((ent.copy(), cat_name, "Global"))
        
    print(f"Total raw entities loaded: {len(all_raw_entities)}")
    
    # Deduplicate and merge globally
    # We maintain a list of unique merged entities
    unique_entities = []
    # Maps to find indices in unique_entities
    norm_name_to_idx = {}
    norm_url_to_idx = {}
    
    for ent, cat_name, source in all_raw_entities:
        name = ent.get("Name")
        url = ent.get("Official_Website")
        
        norm_name = normalize_name(name)
        norm_url = normalize_url(url)
        
        match_idx = None
        if norm_name in norm_name_to_idx:
            match_idx = norm_name_to_idx[norm_name]
            print(f"Duplicate Name match: '{name}' ({source}) matches existing '{unique_entities[match_idx].get('Name')}' in category '{unique_entities[match_idx].get('_Category')}'")
        elif norm_url and norm_url in norm_url_to_idx:
            match_idx = norm_url_to_idx[norm_url]
            print(f"Duplicate URL match: '{url}' ({source}) matches existing '{unique_entities[match_idx].get('Official_Website')}' in category '{unique_entities[match_idx].get('_Category')}'")
            
        if match_idx is not None:
            # We found a duplicate, let's merge
            is_govt = (cat_name == "Government" or unique_entities[match_idx].get("_Category") == "Government")
            merged_ent = merge_entities(unique_entities[match_idx], ent, is_govt)
            
            # If the category is different, resolve it
            cat1 = unique_entities[match_idx].get("_Category")
            cat2 = cat_name
            if cat1 != cat2:
                # Decide category by priority: Critical > High > Medium
                priority_map = {"Critical": 3, "High": 2, "Medium": 1}
                p1 = priority_map.get(ref_cats[cat1]["Priority"], 0) if cat1 in ref_cats else 0
                p2 = priority_map.get(ref_cats[cat2]["Priority"], 0) if cat2 in ref_cats else 0
                chosen_cat = cat2 if p2 > p1 else cat1
                merged_ent["_Category"] = chosen_cat
                print(f"Resolved category mismatch: '{cat1}' vs '{cat2}'. Selected '{chosen_cat}'.")
            else:
                merged_ent["_Category"] = cat1
                
            unique_entities[match_idx] = merged_ent
            
            # Update mappings in case names or URLs changed
            new_name = merged_ent.get("Name")
            new_url = merged_ent.get("Official_Website")
            new_norm_name = normalize_name(new_name)
            new_norm_url = normalize_url(new_url)
            if new_norm_name != norm_name:
                norm_name_to_idx[new_norm_name] = match_idx
            if new_norm_url and new_norm_url != norm_url:
                norm_url_to_idx[new_norm_url] = match_idx
        else:
            # New unique entity
            idx = len(unique_entities)
            ent["_Category"] = cat_name
            unique_entities.append(ent)
            norm_name_to_idx[norm_name] = idx
            if norm_url:
                norm_url_to_idx[norm_url] = idx
                
    print(f"Total unique entities after merge: {len(unique_entities)}")
    
    # Now build the final structured database
    for ent in unique_entities:
        cat_name = ent.pop("_Category")
        ref_meta = ref_cats[cat_name]
        
        # Clean all placeholder/fake values in all fields
        for field in list(ent.keys()):
            ent[field] = clean_placeholder(ent[field], field)
            
        if cat_name != "Government":
            # For standard schema, ensure these fields are populated
            ent["Category"] = cat_name
            ent["Priority"] = ref_meta["Priority"]
            ent["Category_For_Company"] = ref_meta["Category_For_Company"]
            
            # Clean and check optional fields: Phone and LinkedIn
            # In STANDARD_SCHEMA, Phone and LinkedIn are not required, but if they exist, they must be formatted correctly.
            # If we cleaned them to empty strings, let's remove them or keep them empty if they are optional.
            # In verify_funding_db.py:
            # if not rule["required"] and val in (None, ""): continue
            # So setting to "" is fine, or we can just leave it as "".
            if "LinkedIn" in ent and ent["LinkedIn"] == "":
                # Keep it or remove it? Let's leave it as "" or remove it. Let's keep it as "".
                pass
            if "Phone" in ent and ent["Phone"] == "":
                pass
        else:
            # For Government, ensure Category, Priority, Category_For_Company are NOT present
            ent.pop("Category", None)
            ent.pop("Priority", None)
            ent.pop("Category_For_Company", None)
            
        expanded_content[cat_name]["Entities"].append(ent)
        
    output_data = {
        "ContentForFunding": expanded_content
    }
    
    with open(expanded_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print(f"Saved expanded database to {expanded_path}")
    
    # 5. E2E Verification
    print("Running E2E verification...")
    from verify_funding_db import DatabaseVerifier
    verifier = DatabaseVerifier(expanded_path, funding_path, min_count=150)
    success = verifier.verify()
    if success:
        print("SUCCESS: Funding expanded database verification passed successfully. No errors.")
        return True
    else:
        print(f"FAILURE: Verification found {len(verifier.errors)} compliance violations:", file=sys.stderr)
        for err in verifier.errors:
            print(f" - {err}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
