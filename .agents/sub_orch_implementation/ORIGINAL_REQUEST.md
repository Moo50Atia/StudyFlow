# Original User Request

## Initial Request — 2026-07-12T12:11:30+03:00

You are the Implementation Track Sub-Orchestrator. Your working directory is d:/projects/laravel_projects/college_project/.agents/sub_orch_implementation.
Your task is to build a massive global Funding Intelligence Database of at least 150+ high-quality verified entities by expanding all categories in Funding/ContentForFunding.json, and saving the output to Funding/ContentForFunding_Expanded.json.

Instructions:
1. Read d:/projects/laravel_projects/college_project/.agents/sub_orch_implementation/SCOPE.md and the parent scope d:/projects/laravel_projects/college_project/.agents/orchestrator/PROJECT.md.
2. Initialize your BRIEFING.md and progress.md in your working directory.
3. Follow the Orchestrator Procedure (Assess, Decompose, or run the Iteration Loop) to implement the database expansion.
4. Deploy browser subagents to manually search official sites, university pages, and incubator/accelerator lists worldwide. Prioritize Egypt and MENA, then Europe and North America.
5. Retrieve and map discovered entities to exact schemas:
   - Government Category: Name, Official_Website, Funding_Programs, Last_Project_Link, Eligibility, Required_Documents, Funding_Amount, Application_Process, Success_Stories, Acceptance_Rate, Expected_Duration, Notes, Steps_For_Any_Project_To_Get_Funded, Steps_For_This_Project_To_Get_Funded.
   - All Other Categories: Name, Category, Category_For_Company, Priority, Country, City, Official_Website, Official_Email, LinkedIn, Phone, Description (or Why).
6. Ensure no placeholder values or fake emails/websites are present. Normalize names and merge duplicates.
7. The database must contain at least 150+ verified entities.
8. Monitor the creation of `TEST_READY.md` at project root. Once the E2E verification runner is ready, execute `python verify_funding_db.py` to ensure the generated `Funding/ContentForFunding_Expanded.json` passes all tests with exit code 0.
9. Verify your work using reviewers and challengers. Run a Forensic Audit.
10. Update progress.md and BRIEFING.md. Once done, write handoff.md in your working directory and notify the parent orchestrator (conversation ID: 4633414d-a806-4057-8b1f-51ecc6b03c03) using send_message.
