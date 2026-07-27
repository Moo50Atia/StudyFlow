# Original User Request

## 2026-07-12T09:11:27Z

You are the E2E Testing Track Sub-Orchestrator. Your working directory is d:/projects/laravel_projects/college_project/.agents/sub_orch_e2e_testing.
Your task is to implement the E2E test suite/verification script `verify_funding_db.py` and publish `TEST_READY.md` at the project root.

Instructions:
1. Read d:/projects/laravel_projects/college_project/.agents/sub_orch_e2e_testing/SCOPE.md and the parent scope d:/projects/laravel_projects/college_project/.agents/orchestrator/PROJECT.md.
2. Initialize your BRIEFING.md and progress.md in your working directory.
3. Follow the Orchestrator Procedure: Assess, Decompose if needed, or run the Iteration Loop (Explorer -> Worker -> Reviewer -> Challenger -> Auditor) to implement `verify_funding_db.py` and create `TEST_READY.md`.
4. The verify_funding_db.py script must validate:
   - File exists and is valid JSON.
   - Preserves original categories and hierarchy exactly as in ContentForFunding.json.
   - Government category entities conform exactly to the custom Government schema:
     - Name: string
     - Official_Website: string (valid URL)
     - Funding_Programs: list of strings
     - Last_Project_Link: string (valid URL)
     - Eligibility: list of strings
     - Required_Documents: list of strings
     - Funding_Amount: string
     - Application_Process: list of strings
     - Success_Stories: list of strings
     - Acceptance_Rate: string
     - Expected_Duration: string
     - Notes: string
     - Steps_For_Any_Project_To_Get_Funded: list of strings
     - Steps_For_This_Project_To_Get_Funded: list of strings
   - Other category entities conform to the standard entity schema:
     - Name: string
     - Category: string
     - Category_For_Company: list of strings
     - Priority: string
     - Country: string
     - City: string
     - Official_Website: string (valid URL)
     - Official_Email: string (valid email format)
     - LinkedIn: string (valid URL or empty/optional)
     - Phone: string (valid phone number or empty/optional)
     - Description/Why: string
   - No placeholder values, fake emails, or TBDs.
   - No duplicate names or official website URLs.
   - Contains at least 150+ verified entities in total.
5. Create dummy valid and invalid JSON data files to test the script, verify that it exits with 0 on success and non-zero on failure.
6. Verify your implementation using reviewers and challengers. Run a Forensic Audit to ensure compliance.
7. Publish `TEST_READY.md` at the project root.
8. Update progress.md and BRIEFING.md. Once done, write handoff.md in your working directory and notify the parent orchestrator (conversation ID: 4633414d-a806-4057-8b1f-51ecc6b03c03) using send_message.
