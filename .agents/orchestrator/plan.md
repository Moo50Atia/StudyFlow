# Execution Plan: Dakhlia STEM School Research

## Objective
Perform targeted research on the Dakhlia STEM School (Egypt) to gather direct contacts, decision-maker LinkedIn profiles, precise geographic details, and historical projects or funding over the last 5 years (2021-2026). Save the validated data in `STEM.json` inside `d:/projects/laravel_projects/college_project/STEM` and verify it using `verify_stem.py`.

## Milestone 1: E2E Testing Track (Verification Setup)
- Target: Create `verify_stem.py` at the project root to validate `STEM/STEM.json`:
  - Parses successfully as JSON.
  - Ensures the school is present.
  - Checks format correctness for all website/LinkedIn URLs and contact formats.
  - Validates that no placeholder values (TBD, N/A, etc.) are present.
  - Enforces that at least one valid project/funding entry is listed for the school.
  - Validates that the school object includes keys for: `Name`, `Location` (with `Address` and `Maps_Link`), `Non_Official_Contacts` (array of contact details), `Decision_Makers` (array of objects with `Name`, `Role`, and `LinkedIn`), `General_Info` (object containing key parameters), and `Funding_And_Projects` (array of objects detailing each grant/project).
  - Each funding/project object contains: `Name`, `Year` (must be 2021-2026), `Funding_Body`, `Amount`, and `Description`.

## Milestone 2: Implementation Track (Browser-based Research and Data Compilation)
- Target: Deploy browser subagents to:
  - Search official and unofficial sources for Dakhlia STEM School.
  - Extract direct alternative contacts (direct phone, emails, personal contact of coordinators/teachers).
  - Extract decision makers (principals, coordinators, headteachers) and their professional LinkedIn profiles.
  - Locate precise geographic coordinates / address / Google Maps link.
  - Identify historical projects or funding from 2021-2026.
- Target: Save the validated data in `STEM.json` inside the directory `d:/projects/laravel_projects/college_project/STEM`.

## Milestone 3: QA & Verification Gate
- Target: Verify the research and data compilation:
  - Run `python verify_stem.py` and ensure it passes successfully with zero errors/warnings.
  - Run Forensic Audit to verify integrity (no hardcoded/cheated data).
