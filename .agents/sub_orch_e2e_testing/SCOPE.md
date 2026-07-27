# Scope: E2E Testing Track

## Architecture
- Target file: `verify_funding_db.py`
- Setup test runner, validation rules, compliance checks, and target verification constraints.
- Output `TEST_READY.md` when the test suite is fully functional.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Test Harness Design | Design the structure of `verify_funding_db.py` | None | DONE |
| 2 | Implementation | Implement checks for schema correctness, name normalisation, de-duplication, format validations, and count check | M1 | DONE |
| 3 | Verification | Verify verification script works properly and publishes `TEST_READY.md` | M2 | DONE |
