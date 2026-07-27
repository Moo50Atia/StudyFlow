## 2026-07-12T09:18:10Z

You are the JSON Merger & QA agent. Your working directory is d:/projects/laravel_projects/college_project/.agents/worker_m3.
Your task is to merge the two collected datasets:
1. d:/projects/laravel_projects/college_project/Funding/egypt_mena_entities.json (97 entities)
2. d:/projects/laravel_projects/college_project/Funding/global_entities.json (95 entities)
Into the final expanded database: d:/projects/laravel_projects/college_project/Funding/ContentForFunding_Expanded.json.

Instructions:
1. Read the original categories metadata and structure rules from d:/projects/laravel_projects/college_project/Funding/ContentForFunding.json.
2. The final JSON must root at a single object with a key "ContentForFunding". Inside it, each of the 18 categories must be present, with all of its original metadata (Why, Priority, Category_For_Company) preserved exactly, and all entities nested under the "Entities" key as a list.
3. Write a robust Python script to merge these entities, perform name normalisation, and merge/de-duplicate duplicates based on normalized names and normalized websites.
4. Ensure all standard schema fields (Category, Priority, Category_For_Company) are correctly populated. For Category, it must match the category name. For Priority, it must match the category's Priority. For Category_For_Company, it must match the category's Category_For_Company.
5. Verify that no placeholder values, fake emails, fake domains, or fake phone sequences exist in the final database.
6. Execute the merge, save the output to d:/projects/laravel_projects/college_project/Funding/ContentForFunding_Expanded.json, and run the E2E verification using python verify_funding_db.py to ensure it passes.
7. Set up your progress.md and BRIEFING.md in your working directory. Update progress.md as you work.
8. Once you are done and verify_funding_db.py passes with exit code 0, write handoff.md in your working directory and notify the parent via send_message.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
