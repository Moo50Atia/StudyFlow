## 2026-07-12T09:23:49Z
You are Worker Generation 2 for the E2E Testing Track.
Your working directory is d:/projects/laravel_projects/college_project/.agents/worker_e2e_gen2.
Your task is to fix 8 logic bugs and robustness edge cases in `verify_funding_db.py` so that all unit tests in `test_verify_funding_db.py` AND the stress tests in `test_stress_funding_db.py` pass cleanly.

1. Read the following files:
   - Challenger handoff: d:/projects/laravel_projects/college_project/.agents/challenger_e2e_2/handoff.md
   - Auditor handoff: d:/projects/laravel_projects/college_project/.agents/auditor_e2e/handoff.md
   - The validator: d:/projects/laravel_projects/college_project/verify_funding_db.py
   - The stress tests: d:/projects/laravel_projects/college_project/test_stress_funding_db.py
2. Fix the following 8 bugs in `verify_funding_db.py`:
   - **LinkedIn Phishing Domain Bypass**: Update the LinkedIn format check. Use `urllib.parse.urlparse` (or regex) to parse the URL. Ensure that the hostname is exactly `linkedin.com` or ends with `.linkedin.com` (e.g. `www.linkedin.com`). Do not permit query strings/paths to trigger match.
   - **Digit-Free Phone Numbers**: Ensure that phone validation rejects strings that contain only spaces and punctuation without digits. Check that the phone contains at least 5 digits (e.g. `sum(1 for c in val if c.isdigit()) >= 5`).
   - **Reference JSON Parsing Crash**: Ensure that if the reference JSON is invalid or parses to `None` or a list instead of a dict, log an error and return False, avoiding `AttributeError`.
   - **Category Metadata Structure Crash**: If a category inside the reference JSON is configured as a list or string instead of a dictionary, log an error and skip/continue, avoiding crash.
   - **False Positive Duplicate Names**: If the normalized name is empty `""`, do not treat it as a duplicate name.
   - **False Positive Duplicate Websites**: If the normalized website URL is empty `""`, do not treat it as a duplicate website.
   - **URL Case-Sensitivity Loss**: Update `normalize_url` so it only lowercases the scheme and domain parts, leaving the path and query parameters case-sensitive.
   - **Optional Field Whitespace Bypass**: For optional fields (like LinkedIn or Phone), strip the value. If it contains only whitespace, treat it as empty/None and skip format check, but if it is required and contains only whitespace, fail it.
3. Run the tests using pytest:
   - Run `pytest test_verify_funding_db.py`
   - Run `pytest test_stress_funding_db.py`
   Verify that all tests in both files pass.
4. Run `python verify_funding_db.py Funding/ContentForFunding_Expanded_Valid_Dummy.json --min-count 2` to verify it passes.
5. Write your handoff report and verification outputs to `handoff.md` in your working directory.
6. Notify the parent orchestrator (conversation ID: fe7a8a07-944f-48be-ba17-e665c9ebf8f7) when done using send_message.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
