## 2026-07-15T19:51:14Z
Implement a verification script verify_stem.py at d:/projects/laravel_projects/college_project/verify_stem.py.

Requirements for verify_stem.py:
1. It must validate the file d:/projects/laravel_projects/college_project/STEM/STEM.json.
2. It must check that STEM.json is a valid JSON file and contains a list/array with exactly 1 school object.
3. The school object must contain these fields: Name, Location, Non_Official_Contacts, Decision_Makers, General_Info, Funding_And_Projects.
4. Location must be an object with keys: Address, Maps_Link.
5. Non_Official_Contacts must be an array of strings or contact details.
6. Decision_Makers must be an array of objects, each with: Name, Role, LinkedIn.
7. Funding_And_Projects must be an array of objects, each with: Name, Year, Funding_Body, Amount, Description.
8. Validate that at least one project/funding entry is listed, and that the years are in the last 5 years (2021-2026).
9. Perform strict checks that no placeholder values (TBD, N/A, todo, placeholder, none, etc. - case insensitive) are present in any string.
10. Check format correctness for URLs (Maps_Link, LinkedIn, and any websites).
11. Return exit code 0 if valid, non-zero exit code if invalid.
12. Write clean, robust, and well-documented Python code.

Before concluding, verify your implementation by creating temporary dummy JSON files (both valid and invalid) and executing verify_stem.py on them to confirm that it correctly reports success and failure. Make sure to clean up the dummy files afterwards.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your working directory is d:/projects/laravel_projects/college_project/.agents/worker_m1. Write progress.md and handoff.md there.
