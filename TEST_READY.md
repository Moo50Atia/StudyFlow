# E2E Test Suite Ready

## Test Runner
- Commands to run the test suite:
  ```powershell
  # Run the unit tests
  pytest test_verify_funding_db.py

  # Run the stress tests
  pytest test_stress_funding_db.py

  # Run verification on the actual expanded database
  python verify_funding_db.py Funding/ContentForFunding_Expanded.json --min-count 150
  ```
- Expected outcome: All tests pass successfully (exit code 0), and database verification completes with a success message.

## Coverage Summary
| Tier | Count | Description |
|------|------:|-------------|
| 1. Feature Coverage | 6 | Happy-path tests for each core validation feature (Category Structure, Government Schema, Standard Schema, Placeholder Prevention, Global Uniqueness, Volume Constraint). |
| 2. Boundary & Corner | 8 | Boundary conditions, empty values, invalid types, phone/email formats, malformed configurations, and optional fields. |
| 3. Cross-Feature | 3 | Checks for duplicate names and websites across different category groups, and metadata mismatches. |
| 4. Real-World Application | 1 | Verification script executes against the production expanded database (`ContentForFunding_Expanded.json`) containing 261 live entities. |
| **Total** | **18** | |

## Feature Checklist
| Feature | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|:------:|:------:|:------:|:------:|
| Category Structure Integrity | 1 | 1 | 1 | ✓ |
| Government Schema Conformity | 1 | 2 | ✓ | ✓ |
| Standard Schema Conformity | 1 | 2 | ✓ | ✓ |
| Placeholder Prevention | 1 | 1 | ✓ | ✓ |
| Global Uniqueness | 1 | 1 | 1 | ✓ |
| Volume Constraint | 1 | 1 | ✓ | ✓ |
