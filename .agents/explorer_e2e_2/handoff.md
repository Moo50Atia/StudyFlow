# Handoff Report: E2E Verification Design

This report outlines the technical findings and proposed design for `verify_funding_db.py` and its corresponding test runner `test_verify_funding_db.py` under the E2E Testing Track.

## 1. Observation

Direct observations and file analysis conducted:
- **Scope File** (`d:/projects/laravel_projects/college_project/.agents/sub_orch_e2e_testing/SCOPE.md`):
  - Target file is specified as `verify_funding_db.py` (Line 4):
    > `Target file: verify_funding_db.py`
  - Purpose: "Setup test runner, validation rules, compliance checks, and target verification constraints." (Line 5)
- **Project File** (`d:/projects/laravel_projects/college_project/.agents/orchestrator/PROJECT.md`):
  - Defines the verification contract (Lines 29-37), including:
    > "1. It exists and is valid JSON."
    > "2. It has the same categories and hierarchy as Funding/ContentForFunding.json."
    > "3. Every entity conforms to its schema (Government vs Standard)."
    > "4. There are no placeholder values, fake emails, or dummy websites."
    > "5. There are no duplicate names or websites."
    > "6. The database contains at least 150+ verified entities."
    > "Must return exit code 0 on success, non-zero on failure."
- **Reference JSON** (`d:/projects/laravel_projects/college_project/Funding/ContentForFunding.json`):
  - Defines exactly 18 categories under the root key `"ContentForFunding"`.
  - Defines the schema structure for `"Government"` (Lines 146-161):
    > `"Structure": { "Name": "", "Official_Website": "", "Funding_Programs": [], "Last_Project_Link": "", "Eligibility": [], "Required_Documents": [], "Funding_Amount": "", "Application_Process": [], "Success_Stories": [], "Acceptance_Rate": "", "Expected_Duration": "", "Notes": "", "Steps_For_Any_Project_To_Get_Funded": [], "Steps_For_This_Project_To_Get_Funded": [] }`
- **Sub-Orchestrator Request** (`d:/projects/laravel_projects/college_project/.agents/sub_orch_e2e_testing/ORIGINAL_REQUEST.md`):
  - Specifies Standard Schema types (Lines 30-41):
    > "Other category entities conform to the standard entity schema: Name: string, Category: string, Category_For_Company: list of strings, Priority: string, Country: string, City: string, Official_Website: string (valid URL), Official_Email: string (valid email format), LinkedIn: string (valid URL or empty/optional), Phone: string (valid phone number or empty/optional), Description/Why: string"

## 2. Logic Chain

From these observations, we constructed the following design reasoning:
1. **Source of Truth for Categories**: The script `verify_funding_db.py` must load `Funding/ContentForFunding.json` to dynamically extract the 18 master categories. It must assert that the target JSON file contains exactly these 18 keys under `"ContentForFunding"` and no other keys.
2. **Schema Separation**: Government schema requires 14 keys with a mix of string and list of strings types. Standard schema requires 11 keys (with `LinkedIn` and `Phone` optional/nullable, and `Description` or `Why` accepted as description). The script must select the validation ruleset based on whether the entity belongs to `"Government"` or another category.
3. **De-duplication Logic**: Duplicate detection needs to be global (cross-category) and robust against trivial format variations:
   - Names normalized by lower-casing, stripping punctuation/spaces, and removing common business suffixes (`Inc.`, `LLC.`, `Ltd.`, etc.).
   - URLs normalized by stripping schemes (`http://`, `https://`), `www.`, and trailing slashes.
4. **Placeholder Detection**: Strings must be scanned for common mock signatures (`tbd`, `todo`, `placeholder`, `fake@email.com`, `example.com`, `0000000`, etc.) using word-boundary regexes and domain checks.
5. **Testability of Total Count**: The default run requires 150+ entities. However, to run unit tests with small dummy datasets, the validator script should accept a `--min-count <N>` command-line option.
6. **Subprocess Test Runner**: `test_verify_funding_db.py` will use `pytest` and `tmp_path` to generate valid and invalid datasets dynamically, executing the validator in a subprocess and checking exit codes (0 for success, 1 for failure). This avoids polluting the codebase with static dummy files.

## 3. Caveats

- **Description vs Why**: In standard entities, the field is occasionally referred to as `Description` or `Why`. The proposed script validates `Description`, but falls back to checking `Why` if `Description` is not present.
- **Python Environment**: We assume `pytest` is available globally in the python environment, as indicated by the `.pytest_cache` in the workspace root.
- **LinkedIn/Phone Nullability**: These are optional. The script allows them to be absent, `None`, or empty strings. If present and non-empty, they must match their respective format patterns.

## 4. Conclusion

The technical design and complete python implementation logic for `verify_funding_db.py` and `test_verify_funding_db.py` are fully defined. The proposed code structure is written in `analysis.md` inside this directory.

## 5. Verification Method

Once implemented, the verification suite can be run using the following command at the project root:
```bash
pytest test_verify_funding_db.py
```
To run the validator manually on the main database:
```bash
python verify_funding_db.py Funding/ContentForFunding_Expanded.json
```
If invalid files are tested, they must return exit code `1` and list the errors in `stderr`. If a valid file is tested, it must return exit code `0` and print a success message to `stdout`.
