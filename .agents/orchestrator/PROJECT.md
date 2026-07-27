# Project: Dakhlia STEM School Research & Verification

## Architecture
- Target JSON Output: `STEM/STEM.json`
- Verification script: `verify_stem.py`
- Data flow:
  1. Use browser subagents to research the Dakhlia STEM School (Egypt).
  2. Gather contact channels, decision makers with LinkedIn profiles, maps link, and 2021-2026 funding/projects history.
  3. Compile data to `STEM/STEM.json`.
  4. Write and run `verify_stem.py` to validate `STEM/STEM.json`.
  5. Run Forensic Auditor to check compliance.

## Code Layout
- `STEM/STEM.json` - Data file
- `verify_stem.py` - Automated verification and validation script

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | E2E Testing Track | Implement `verify_stem.py` | None | DONE |
| 2 | Implementation Track | Research school, gather projects, compile to `STEM/STEM.json` | None | DONE |
| 3 | Final Verification | Run validation checks, clean audit, pass 100% | M1, M2 | DONE |

## Interface Contracts
### `verify_stem.py` API Contract
- Must read `STEM/STEM.json` and validate that:
  1. It exists and is valid JSON.
  2. It contains exactly one school object representing the Dakhlia STEM School.
  3. The school object includes keys: `Name`, `Location` (with `Address` and `Maps_Link`), `Non_Official_Contacts` (array of contact details), `Decision_Makers` (array of objects with `Name`, `Role`, and `LinkedIn`), `General_Info` (object containing key parameters), and `Funding_And_Projects` (array of objects detailing each grant/project).
  4. Each funding/project object contains: `Name`, `Year`, `Funding_Body`, `Amount`, and `Description`.
  5. Year must be within 2021-2026.
  6. No placeholder or dummy values (TBD, N/A, etc.) are present.
  7. At least one valid project/funding entry is listed.
  8. Website/LinkedIn URLs and contact formats are valid.
- Must return exit code 0 on success, non-zero on failure.
