import json
import re

egypt_path = "d:/projects/laravel_projects/college_project/Funding/egypt_mena_entities.json"
global_path = "d:/projects/laravel_projects/college_project/Funding/global_entities.json"

EXACT_PLACEHOLDERS = {
    'tbd', 'placeholder', 'todo', 'n/a', 'na', 'none', 'null', 'nil', '-', '--', 'undefined', 'temp'
}
SUBSTRING_PLACEHOLDERS = ['placeholder', 'dummy', 'fake', 'test@']
DUMMY_DOMAINS = ['example.com', 'test.com', 'email.com', 'domain.com', 'fake.com']

def is_placeholder(val, field_name=None):
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
    if field_name == "Phone" and any(seq in val_clean for seq in ['123456', '000000', '111111', '999999']):
        return True
    return False

def check_dict(d, ctx):
    for k, v in d.items():
        if isinstance(v, str):
            if is_placeholder(v, k):
                print(f"[{ctx}] Placeholder in '{k}': '{v}'")
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str) and is_placeholder(item, k):
                    print(f"[{ctx}] Placeholder in '{k}[{i}]': '{item}'")

with open(egypt_path, "r", encoding="utf-8") as f:
    egypt_data = json.load(f)
for cat, ents in egypt_data["ContentForFunding"].items():
    for idx, ent in enumerate(ents):
        check_dict(ent, f"Egypt -> {cat} -> {ent.get('Name', idx)}")

with open(global_path, "r", encoding="utf-8") as f:
    global_data = json.load(f)
for idx, ent in enumerate(global_data):
    check_dict(ent, f"Global -> {ent.get('Category', 'Unknown')} -> {ent.get('Name', idx)}")

print("Done placeholder check.")
