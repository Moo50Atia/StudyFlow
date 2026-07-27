# Handoff Report — STEM Verification Script

## Observation
1. Located existing verifiers in the project directory, specifically `verify_funding_db.py`, which is a database verification script at `d:/projects/laravel_projects/college_project/verify_funding_db.py`.
2. Verified that the directory `STEM` and file `STEM.json` do not currently exist in the workspace root by performing a recursive search for name pattern `*STEM*` with `find_by_name`, which returned `Found 0 results`.
3. Created and modified the script `verify_stem.py` at `d:/projects/laravel_projects/college_project/verify_stem.py`.
4. Created a temporary test script `test_verify_stem_runner.py` at `d:/projects/laravel_projects/college_project/test_verify_stem_runner.py` and executed it via `python test_verify_stem_runner.py` under the directory `d:/projects/laravel_projects/college_project`. The output returned:
   ```
   Running test: Valid STEM JSON...
   --- Output for stem_test_lbz_u977.json ---
   Exit code: 0
   SUCCESS: 'C:\Users\Acer\AppData\Local\Temp\stem_test_lbz_u977.json' is fully valid.
   ...
   ALL TESTS PASSED SUCCESSFULLY!
   ```
5. Ran `python verify_stem.py` to confirm handling of missing file. The output returned exit code 1 and stdout/stderr matching:
   ```
   FAILURE: Validation failed for 'D:\projects\laravel_projects\college_project\STEM\STEM.json'. Found 1 errors:
    - Target file not found: D:\projects\laravel_projects\college_project\STEM\STEM.json
   ```

## Logic Chain
1. Based on Observation 1, the codebase prefers standard Python libraries and class-based layout for database verifiers.
2. Based on the lack of `STEM/STEM.json` (Observation 2) and the user requirements, the `verify_stem.py` script must handle missing files gracefully by returning a non-zero exit code.
3. Implemented validation rules in `verify_stem.py` covering:
   - Root array containing exactly 1 element.
   - Presences of required school keys: `Name`, `Location`, `Non_Official_Contacts`, `Decision_Makers`, `General_Info`, `Funding_And_Projects`.
   - Structural checks (Location contains Address and Maps_Link; Decision_Makers contains Name, Role, LinkedIn; Funding_And_Projects contains Name, Year, Funding_Body, Amount, Description).
   - Value validation: Check year range [2021, 2026] and existence of at least 1 funding project.
   - Placeholder checking (case-insensitive patterns: TBD, N/A, todo, placeholder, none, dummy, fake, etc.).
   - Format validation for URLs (using standard format matching) and LinkedIn (specifically checking hostname domain is `linkedin.com` or ends with `lnkd.in`).
4. Verified that the implementation works correctly (Observation 4) by asserting that valid dummy files pass with exit code 0, and all invalid dummy files (with schema violations, invalid years, placeholder values, invalid LinkedIn URLs, or incorrect element count) fail with exit code 1.
5. Confirmed that default executions fail cleanly (Observation 5) with a non-zero exit code when the target `STEM/STEM.json` file is missing.

## Caveats
- Checked URL syntax using standard regular expressions and `urlparse`. We do not verify network status of the URL (i.e. whether the site is up/reachable) due to CODE_ONLY network restrictions.
- Assumed `Non_Official_Contacts` can hold strings (e.g. phone/emails) or objects (nested keys). If holding objects, keys/values are scanned recursively for formatting and placeholders.

## Conclusion
The `verify_stem.py` script has been successfully implemented at `d:/projects/laravel_projects/college_project/verify_stem.py` in accordance with all constraints and specifications. It functions as a standalone verification executable.

## Verification Method
To verify the script:
1. Ensure Python 3 is installed.
2. Run the script against a valid test STEM JSON file to check that it exits with code 0:
   ```bash
   python verify_stem.py <path_to_valid_json_file>
   ```
3. Run the script without arguments or against an invalid STEM JSON file to check that it exits with code 1:
   ```bash
   python verify_stem.py
   ```
