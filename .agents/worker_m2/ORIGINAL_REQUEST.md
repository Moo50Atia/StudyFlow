## 2026-07-12T09:12:36Z
You are the Global Data Collector. Your working directory is d:/projects/laravel_projects/college_project/.agents/worker_m2.
Your task is to search, discover, and extract at least 80 high-quality verified funding entities globally (focusing on Europe, North America, etc.) matching the categories in Funding/ContentForFunding.json.
You must read the categories in d:/projects/laravel_projects/college_project/Funding/ContentForFunding.json.
Use browser tools (browser-mcp, puppeteer, or mcp-nodriver) to search official pages, university directories, and incubator/accelerator directories (e.g. Y Combinator, Techstars, Sequoia Capital, Stanford University, Oxford University, etc.) in Europe, North America, and other regions.

Ensure that:
1. Every entity conforms to its schema:
   - Government: Name, Official_Website, Funding_Programs, Last_Project_Link, Eligibility, Required_Documents, Funding_Amount, Application_Process, Success_Stories, Acceptance_Rate, Expected_Duration, Notes, Steps_For_Any_Project_To_Get_Funded, Steps_For_This_Project_To_Get_Funded.
   - All other categories: Name, Category, Category_For_Company, Priority, Country, City, Official_Website, Official_Email, LinkedIn, Phone, Description.
2. There are absolutely no placeholder values, fake emails, or dummy websites.
3. Save the results to d:/projects/laravel_projects/college_project/Funding/global_entities.json.
4. Set up your progress.md and BRIEFING.md in your working directory. Update progress.md as you work.
5. Once you are done, write handoff.md in your working directory and notify the parent via send_message.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
