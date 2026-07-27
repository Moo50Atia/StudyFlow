## 2026-07-15T20:21:54Z
Verify the compiled school dataset in STEM/STEM.json and run the validation script verify_stem.py.

Your tasks:
1. Verify that the file d:/projects/laravel_projects/college_project/STEM/STEM.json contains the correct data for Dakahlia STEM School.
2. Execute the verification script:
   ```powershell
   python verify_stem.py
   ```
   from the project root directory. Verify it exits with code 0.
3. Review the data to ensure that:
   - Location contains Address and Maps_Link (without @ to bypass the validator bug).
   - Non_Official_Contacts contains direct contacts.
   - Decision_Makers contains Ragab Algablawy (Principal), Basma Mohamed (EFL Coordinator), and Basma Elsayed (English Teacher) with LinkedIn profile URLs.
   - Funding_And_Projects has at least 5 entries since 2021 (the last 5 years) with details (Name, Year, Funding_Body, Amount, Description).
   - No placeholder values like TBD, N/A, etc. exist.
4. Document the execution output and your findings in handoff.md in your working directory.

Your working directory is d:/projects/laravel_projects/college_project/.agents/reviewer_m3. Write progress.md and handoff.md there.
