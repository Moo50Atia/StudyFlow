# Implementation Plan - verify_stem.py

## Objectives
1. Implement the Python verification script `verify_stem.py` at `d:/projects/laravel_projects/college_project/verify_stem.py`.
2. Validate `STEM/STEM.json` structure, schema, year ranges, dummy/placeholder detection, and URL/LinkedIn formats.
3. Verify the implementation by writing a temporary test script that creates valid and invalid dummy JSON files, runs `verify_stem.py` against them, asserts correct exit codes, and cleans them up.

## Verification Script Design (`verify_stem.py`)
- **CLI Options**: Support a file path argument (positional or `--file`) defaulting to `d:/projects/laravel_projects/college_project/STEM/STEM.json`.
- **Parsing**: Handle file not found and JSON syntax errors cleanly.
- **Root Validation**: Must be a JSON array with exactly 1 school object.
- **Field Checks**: Validate Name, Location, Non_Official_Contacts, Decision_Makers, General_Info, Funding_And_Projects.
- **Location Checks**: Validate Location.Address is non-empty, and Location.Maps_Link is a valid URL.
- **Contact Checks**: Validate array of strings or contact details.
- **Decision Maker Checks**: Validate array of Name, Role, LinkedIn (must be a valid LinkedIn URL starting with http/https).
- **Funding & Projects Checks**: Validate Name, Year (2021-2026), Funding_Body, Amount, Description. Array length must be >= 1.
- **Placeholder Detection**: Case-insensitive exact and whole-word regex matching for standard placeholders (TBD, N/A, todo, placeholder, none, dummy, fake, etc.).
- **URL/Email Formats**: Regex validation for URLs, Emails, and LinkedIn domains.
- **Exit Code**: Exit with 0 if validation succeeds; 1 if any validation error is detected.

## Test Strategy (Self-Verification)
1. Write a temporary Python script `test_verify_stem.py` that will:
   - Create a valid dummy JSON file `temp_valid.json`.
   - Run `python verify_stem.py temp_valid.json` and assert it exits with 0.
   - Create various invalid dummy JSON files (e.g., missing fields, invalid year, placeholder value, invalid LinkedIn URL, wrong element count).
   - Run `python verify_stem.py temp_invalid.json` for each and assert it exits with non-zero (1).
   - Clean up all temporary files.
2. Execute `test_verify_stem.py` using `run_command`.
3. If tests pass, delete `test_verify_stem.py`.

## Verification Steps
1. Create `verify_stem.py`.
2. Create and run `test_verify_stem.py`.
3. Check the command output for clean pass/fail assertions.
4. Clean up test files.
