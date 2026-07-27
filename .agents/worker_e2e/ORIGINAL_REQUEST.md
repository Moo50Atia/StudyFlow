## 2026-07-12T09:15:24Z

You are the Worker for the E2E Testing Track.
Your working directory is d:/projects/laravel_projects/college_project/.agents/worker_e2e.
Your task is to implement the E2E verification script `verify_funding_db.py` and a test suite to verify its correctness.

1. Read the Explorer design and synthesized findings in:
   - d:/projects/laravel_projects/college_project/.agents/explorer_e2e_3/analysis.md
2. Implement `verify_funding_db.py` in the project root (d:/projects/laravel_projects/college_project/verify_funding_db.py) based on the synthesized Python design.
   It must:
   - Support a default target path of "Funding/ContentForFunding_Expanded.json" and a custom path via command line arguments.
   - Accept a reference path via --reference-path (defaulting to "Funding/ContentForFunding.json").
   - Accept --min-count (defaulting to 150).
   - Return exit code 0 on success, non-zero on failure.
   - Strictly validate JSON structure, category match (Universities, Government, etc.), schema conformity (Custom Government Schema vs Standard Schema), placeholder values (TBDs), duplicate names (using collapsed alphanumeric case-insensitive normalization), and duplicate websites (ignoring scheme/www/trailing slashes).
   - Ensure list items are not empty strings and descriptions are >= 10 chars.
3. Implement `test_verify_funding_db.py` in the project root to run pytest unit tests.
   It should:
   - Test a fully valid db mock dataset and expect exit code 0.
   - Test various invalid variations (missing root key, missing category, metadata mismatch, missing required field, invalid type, placeholder value, duplicate name, duplicate website, insufficient entity count) and expect exit code 1.
   - Use pytest's tmp_path fixture to dynamically create files for tests, so no dummy files pollute the database directory permanently.
4. Create static dummy data files for manual testing:
   - Create `Funding/ContentForFunding_Expanded_Valid_Dummy.json` (a valid mock database that passes checks with min-count=2).
   - Create `Funding/ContentForFunding_Expanded_Invalid_Dummy.json` (an invalid mock database with intentional errors like placeholders, invalid emails, metadata mismatches).
5. Run the pytest suite and run verify_funding_db.py directly against the dummy files to verify everything passes. Document the run commands and outputs.
6. Write a handoff report documenting the file paths created, verification results, and any instructions in `handoff.md` (or `changes.md`) in your working directory.
7. Notify the parent orchestrator (conversation ID: fe7a8a07-944f-48be-ba17-e665c9ebf8f7) when done using send_message.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
