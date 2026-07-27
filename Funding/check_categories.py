import json
import os

funding_path = "d:/projects/laravel_projects/college_project/Funding/ContentForFunding.json"
egypt_path = "d:/projects/laravel_projects/college_project/Funding/egypt_mena_entities.json"
global_path = "d:/projects/laravel_projects/college_project/Funding/global_entities.json"

with open(funding_path, "r", encoding="utf-8") as f:
    funding_data = json.load(f)

with open(egypt_path, "r", encoding="utf-8") as f:
    egypt_data = json.load(f)

with open(global_path, "r", encoding="utf-8") as f:
    global_data = json.load(f)

funding_cats = set(funding_data["ContentForFunding"].keys())
print("Funding categories:", sorted(list(funding_cats)))

egypt_cats = set(egypt_data["ContentForFunding"].keys())
print("Egypt/MENA categories:", sorted(list(egypt_cats)))

global_cats = set([ent.get("Category") for ent in global_data if "Category" in ent])
print("Global categories:", sorted(list(global_cats)))

print("Egypt category difference (Egypt - Funding):", egypt_cats - funding_cats)
print("Global category difference (Global - Funding):", global_cats - funding_cats)
