import json
import re
import sys
import os
from typing import Dict, Any, List, Set, Tuple

# Normalization functions matching verifier
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

# Placeholder detection constants
EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake', 'test@']
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com', 'fake.com']
FAKE_PHONE_SUBSTRINGS = ['123456', '000000', '111111', '999999']

def is_placeholder(val: Any, field_name: str = None) -> bool:
    if not isinstance(val, str):
        return False
    val_clean = val.strip().lower()
    if val_clean in EXACT_PLACEHOLDERS:
        return True
    for kw in SUBSTRING_PLACEHOLDERS:
        if kw in val_clean:
            return True
    if any(dom in val_clean for dom in DUMMY_DOMAINS):
        return True
    if field_name == "Phone" and any(seq in val_clean for seq in FAKE_PHONE_SUBSTRINGS):
        return True
    return False

def clean_placeholder_or_fake(val: Any, field_name: str = None) -> Any:
    if isinstance(val, str):
        if is_placeholder(val, field_name):
            return ""
    return val

def merge_entities(ent1: Dict[str, Any], ent2: Dict[str, Any], is_govt: bool) -> Dict[str, Any]:
    # Merges ent2 into ent1 and returns a new entity
    merged = {}
    
    # All fields from both entities
    all_keys = set(ent1.keys()) | set(ent2.keys())
    
    for key in all_keys:
        val1 = ent1.get(key)
        val2 = ent2.get(key)
        
        # Clean placeholders
        val1 = clean_placeholder_or_fake(val1, key)
        val2 = clean_placeholder_or_fake(val2, key)
        
        if val1 and not val2:
            merged[key] = val1
        elif val2 and not val1:
            merged[key] = val2
        elif not val1 and not val2:
            merged[key] = "" if isinstance(val1, str) or isinstance(val2, str) else None
        else:
            # Both exist and are not empty
            if isinstance(val1, list) and isinstance(val2, list):
                # Merge lists, maintain order, remove duplicates
                seen = set()
                new_list = []
                for item in val1 + val2:
                    cleaned_item = clean_placeholder_or_fake(item)
                    if cleaned_item and cleaned_item not in seen:
                        seen.add(cleaned_item)
                        new_list.append(cleaned_item)
                merged[key] = new_list
            elif isinstance(val1, str) and isinstance(val2, str):
                if val1.strip().lower() == val2.strip().lower():
                    # Pick the one with better capitalization (e.g. more uppercase)
                    up1 = sum(1 for c in val1 if c.isupper())
                    up2 = sum(1 for c in val2 if c.isupper())
                    merged[key] = val1 if up1 >= up2 else val2
                else:
                    # Pick the longer one for description, otherwise ent1
                    if key == "Description":
                        merged[key] = val1 if len(val1) >= len(val2) else val2
                    elif key == "Official_Website":
                        # Pick the one starting with http/https
                        if val1.startswith("http") and not val2.startswith("http"):
                            merged[key] = val1
                        elif val2.startswith("http") and not val1.startswith("http"):
                            merged[key] = val2
                        else:
                            merged[key] = val1
                    else:
                        merged[key] = val1
            else:
                merged[key] = val1
                
    return merged

def main():
    funding_path = "d:/projects/laravel_projects/college_project/Funding/ContentForFunding.json"
    egypt_path = "d:/projects/laravel_projects/college_project/Funding/egypt_mena_entities.json"
    global_path = "d:/projects/laravel_projects/college_project/Funding/global_entities.json"
    expanded_path = "d:/projects/laravel_projects/college_project/Funding/ContentForFunding_Expanded.json"
    
    # 1. Load Reference Config
    print("Loading reference config...")
    with open(funding_path, "r", encoding="utf-8") as f:
        ref_data = json.load(f)
    ref_cats = ref_data["ContentForFunding"]
    
    # Initialize categories in final data structure
    final_content = {}
    for cat_name, cat_meta in ref_cats.items():
        final_content[cat_name] = {
            "Why": cat_meta["Why"],
            "Priority": cat_meta["Priority"]
        }
        if "Category_For_Company" in cat_meta:
            final_content[cat_name]["Category_For_Company"] = cat_meta["Category_For_Company"]
        if "Structure" in cat_meta:
            final_content[cat_name]["Structure"] = cat_meta["Structure"]
        final_content[cat_name]["Entities"] = []
        
    # 2. Collect all entities from both sources
    raw_entities = [] # list of (entity_dict, source_name)
    
    # Load Egypt/MENA
    print("Loading Egypt/MENA entities...")
    with open(egypt_path, "r", encoding="utf-8") as f:
        egypt_data = json.load(f)
    for cat_name, entities in egypt_data["ContentForFunding"].items():
        for ent in entities:
            # Ensure Category field is populated
            ent["Category"] = cat_name
            raw_entities.append((ent, "Egypt/MENA"))
            
    # Load Global
    print("Loading Global entities...")
    with open(global_path, "r", encoding="utf-8") as f:
        global_data = json.load(f)
    for ent in global_data:
        raw_entities.append((ent, "Global"))
        
    print(f"Total raw entities collected: {len(raw_entities)}")
    
    # 3. Deduplicate and merge globally
    # We will map normalized_name -> entity
    # and normalized_url -> entity (if url is present)
    merged_entities: List[Dict[str, Any]] = []
    
    name_to_index: Dict[str, int] = {}
    url_to_index: Dict[str, int] = {}
    
    for ent, source in raw_entities:
        name = ent.get("Name")
        url = ent.get("Official_Website")
        cat = ent.get("Category")
        
        # Validate Category is correct
        if not cat or cat not in ref_cats:
            print(f"Warning: Entity '{name}' has invalid category '{cat}'")
            continue
            
        norm_name = normalize_name(name)
        norm_url = normalize_url(url)
        
        # Check if we have seen this entity before
        idx = None
        if norm_name in name_to_index:
            idx = name_to_index[norm_name]
            print(f"Duplicate name detected: '{name}' in '{cat}' from '{source}' matches existing entity '{merged_entities[idx]['Name']}' in '{merged_entities[idx]['Category']}'")
        elif norm_url and norm_url in url_to_index:
            idx = url_to_index[norm_url]
            print(f"Duplicate URL detected: '{url}' for '{name}' in '{cat}' from '{source}' matches existing website '{merged_entities[idx]['Official_Website']}' for '{merged_entities[idx]['Name']}' in '{merged_entities[idx]['Category']}'")
            
        if idx is not None:
            # Merge with existing entity
            is_govt = (cat == "Government" or merged_entities[idx].get("Category") == "Government")
            merged_ent = merge_entities(merged_entities[idx], ent, is_govt)
            
            # If the category is different, keep the one that is Government, or has higher priority
            # Let's inspect category priority: Critical > High > Medium
            cat1 = merged_entities[idx].get("Category")
            cat2 = cat
            if cat1 != cat2:
                # Decide which category to use
                priority_map = {"Critical": 3, "High": 2, "Medium": 1}
                p1 = priority_map.get(ref_cats[cat1]["Priority"], 0) if cat1 in ref_cats else 0
                p2 = priority_map.get(ref_cats[cat2]["Priority"], 0) if cat2 in ref_cats else 0
                if p2 > p1:
                    merged_ent["Category"] = cat2
                    print(f"Category updated from '{cat1}' to '{cat2}' due to higher priority.")
                else:
                    merged_ent["Category"] = cat1
                    
            merged_entities[idx] = merged_ent
            
            # Update mappings with new values just in case
            new_name = merged_ent.get("Name")
            new_url = merged_ent.get("Official_Website")
            new_norm_name = normalize_name(new_name)
            new_norm_url = normalize_url(new_url)
            if new_norm_name != norm_name:
                name_to_index[new_norm_name] = idx
            if new_norm_url and new_norm_url != norm_url:
                url_to_index[new_norm_url] = idx
        else:
            # Add as new entity
            idx = len(merged_entities)
            merged_entities.append(ent)
            name_to_index[norm_name] = idx
            if norm_url:
                url_to_index[norm_url] = idx
                
    print(f"Total entities after merging and deduplication: {len(merged_entities)}")
    
    # 4. Clean placeholders, populate schema fields, and group by category
    category_entities: Dict[str, List[Dict[str, Any]]] = {cat: [] for cat in ref_cats}
    
    for ent in merged_entities:
        cat_name = ent.get("Category")
        if not cat_name or cat_name not in ref_cats:
            continue
            
        ref_meta = ref_cats[cat_name]
        
        # Clear/clean phone and linkedin placeholders
        for opt_field in ["LinkedIn", "Phone"]:
            if opt_field in ent:
                val = ent[opt_field]
                if is_placeholder(val, opt_field):
                    ent[opt_field] = ""
                    
        # Populate standard category fields
        if cat_name != "Government":
            ent["Category"] = cat_name
            ent["Priority"] = ref_meta["Priority"]
            ent["Category_For_Company"] = ref_meta["Category_For_Company"]
            
            # Clean and ensure standard required fields exist
            for field in ["Name", "Country", "City", "Official_Website", "Official_Email", "Description"]:
                if field not in ent:
                    ent[field] = ""
                else:
                    ent[field] = clean_placeholder_or_fake(ent[field], field)
            
            # Clean optional fields if they are in ent
            if "LinkedIn" in ent:
                ent["LinkedIn"] = clean_placeholder_or_fake(ent["LinkedIn"], "LinkedIn")
            if "Phone" in ent:
                ent["Phone"] = clean_placeholder_or_fake(ent["Phone"], "Phone")
        else:
            # Government entity schema verification
            # Make sure we clean all Government fields
            for field, val in ent.items():
                if isinstance(val, str):
                    ent[field] = clean_placeholder_or_fake(val, field)
                elif isinstance(val, list):
                    ent[field] = [clean_placeholder_or_fake(item, field) for item in val if clean_placeholder_or_fake(item, field)]
                    
            # Ensure Category, Priority, Category_For_Company do not exist in Government entities
            # because GOVERNMENT_SCHEMA doesn't have them
            ent.pop("Category", None)
            ent.pop("Priority", None)
            ent.pop("Category_For_Company", None)
            
        category_entities[cat_name].append(ent)
        
    # Write to final structure
    for cat_name in ref_cats:
        final_content[cat_name]["Entities"] = category_entities[cat_name]
        
    output_data = {
        "ContentForFunding": final_content
    }
    
    # Save output
    print(f"Saving merged output to {expanded_path}...")
    with open(expanded_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
        
    print("Merge completed successfully!")

if __name__ == "__main__":
    main()
