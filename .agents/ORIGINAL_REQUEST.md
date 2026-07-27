# Original User Request

## 2026-07-12T09:09:39Z

# Goal
Build a massive global Funding Intelligence Database by expanding all categories in `Funding/ContentForFunding.json` following the specified schemas and priorities.

Working directory: d:/projects/laravel_projects/college_project
Integrity mode: development

## Requirements

### R1. Category Expansion via Manual Search
Use browser subagents to manually search official sites, government pages, university resources, and incubator/accelerator lists worldwide. Recursively discover funding entities, prioritizing Egypt, MENA, Europe, and North America.

### R2. Dual Schema Mapping
Map each discovered entity to the exact schema defined for its category:
- **Government Category:** Use the custom Government schema (Name, Official Website, Funding Programs, Last Project Link, Eligibility, Required Documents, etc.).
- **All Other Categories:** Use the standard entity schema (Name, Category, Category_For_Company, Priority, Country, City, Official_Website, Official_Email, etc.).

### R3. Quality Assurance and Duplication Merging
Normalize all entity names, merge duplicates, and verify that all contact information (Official_Website, Official_Email, LinkedIn, etc.) is correct and points to official pages.

### R4. Automated Verification Script
Implement and run a verification python script `verify_funding_db.py` that validates the syntax, hierarchy, schema alignment of all entities, and ensures zero duplicates exist.

## Acceptance Criteria

### Data & Schema Compliance
- Output is written to `Funding/ContentForFunding_Expanded.json`.
- The JSON structure preserves the original categories and hierarchy exactly as in `ContentForFunding.json`.
- Every entity complies with either the Government schema or the Standard schema, with all fields correctly populated.
- No placeholder values or fake emails/websites are present.

### Database Scale
- The expanded database contains at least 150+ high-quality, verified entities across all categories, with a primary focus on Egypt and MENA.

### Programmatic Verification
- Running `python verify_funding_db.py` passes successfully with no errors or validation warnings.

## Follow-up — 2026-07-15T22:49:20+03:00

Perform targeted research on the **Dakhlia STEM School** (also known as Dakahlia STEM School) in Egypt to gather direct contacts, decision-maker LinkedIn profiles, precise geographic details, and historical projects or funding over the last 5 years (2021-2026). Save the validated data in `STEM.json`.

Working directory: d:/projects/laravel_projects/college_project/STEM
Integrity mode: development

## Requirements

### R1. School Contact and Location Research
- Discover direct, alternative (non-official/informal) contact channels, including direct phone lines, emails, or personal contacts of coordinators/teachers if available, rather than just the generic Ministry hotline.
- Identify key decision-makers (principals, coordinators, headteachers) and gather their professional LinkedIn profile URLs.
- Locate the precise geographic location (address and coordinates/Google Maps link) of the school.
- Compile any other high-value organizational information that can be utilized for partnership or connection.

### R2. Funding and Project History (Last 5 Years)
- Research all funding, sponsorships, grants, or development projects the school has received or participated in since 2021 (the last 5 years).
- For each project/funding entry, document:
  - Project/Fund Name
  - Year
  - Funding Body/Sponsor/Partner
  - Amount or Valued Support (if public/available)
  - Detailed description of the project, scope, and objectives.

### R3. Output Data Structure (STEM.json)
- Generate a validated JSON file named `STEM.json` containing the findings structured as an array of school objects.
- Ensure the data uses clean, validated keys without placeholders.

### R4. Programmatic Verification
- Implement a verification script `verify_stem.py` that validates `STEM.json`:
  - Parses successfully as JSON.
  - Ensures the school is present.
  - Checks format correctness for all website/LinkedIn URLs and contact formats.
  - Validates that no placeholder values (TBD, N/A, etc.) are present.
  - Enforces that at least one valid project/funding entry is listed for the school.

## Acceptance Criteria

### Data Conformity
- [ ] The file `STEM.json` exists in the working directory and contains exactly one school object representing the Dakhlia STEM School.
- [ ] The school object includes keys for: `Name`, `Location` (with `Address` and `Maps_Link`), `Non_Official_Contacts` (array of contact details), `Decision_Makers` (array of objects with `Name`, `Role`, and `LinkedIn`), `General_Info` (object containing key parameters), and `Funding_And_Projects` (array of objects detailing each grant/project).
- [ ] Each funding/project object contains: `Name`, `Year`, `Funding_Body`, `Amount`, and `Description`.
- [ ] No dummy, placeholder, or TBD values are present in the JSON file.

### Verification Execution
- [ ] Running `python verify_stem.py` passes successfully with no errors or validation warnings.
