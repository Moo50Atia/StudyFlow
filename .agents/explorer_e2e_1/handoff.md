# Handoff Report: E2E Testing Harness Design

## 1. Observation
We observed the following configurations, constraints, and contracts in the project files:
* **E2E Testing Scope** (`.agents/sub_orch_e2e_testing/SCOPE.md`):
  > `- Target file: verify_funding_db.py`
  > `- Setup test runner, validation rules, compliance checks, and target verification constraints.`
* **Parent Project Contract** (`.agents/orchestrator/PROJECT.md`):
  > `### verify_funding_db.py API Contract`
  > `Must read Funding/ContentForFunding_Expanded.json and validate that:`
  > `1. It exists and is valid JSON.`
  > `2. It has the same categories and hierarchy as Funding/ContentForFunding.json.`
  > `3. Every entity conforms to its schema (Government vs Standard).`
  > `4. There are no placeholder values, fake emails, or dummy websites.`
  > `5. There are no duplicate names or websites.`
  > `6. The database contains at least 150+ verified entities.`
  > `- Must return exit code 0 on success, non-zero on failure.`
* **Source Categories** (`Funding/ContentForFunding.json`):
  We observed 18 distinct categories (Universities, Research Centers, ..., Government).
  `Government` contains a custom `"Structure"` key:
  ```json
  "Structure": {
      "Name": "",
      "Official_Website": "",
      "Funding_Programs": [],
      "Last_Project_Link": "",
      "Eligibility": [],
      "Required_Documents": [],
      "Funding_Amount": "",
      "Application_Process": [],
      "Success_Stories": [],
      "Acceptance_Rate": "",
      "Expected_Duration": "",
      "Notes": "",
      "Steps_For_Any_Project_To_Get_Funded": [],
      "Steps_For_This_Project_To_Get_Funded": []
  }
  ```
* **Standard Category Schema** (`.agents/worker_m1/ORIGINAL_REQUEST.md`):
  We observed that the standard entity schema for all other 17 categories is:
  `Name, Category, Category_For_Company, Priority, Country, City, Official_Website, Official_Email, LinkedIn, Phone, Description.`

---

## 2. Logic Chain
Based on these observations, our design reasoning proceeds as follows:
1. **Preserving Hierarchy**: Because `ContentForFunding.json` contains metadata (e.g. `Why`, `Priority`, `Category_For_Company`, and `Structure`), mapping entities directly under the category keys would overwrite this metadata. Therefore, we propose that the expanded file `ContentForFunding_Expanded.json` maps each category to an object that preserves all original keys and appends an `"Entities"` key containing the list of entity records.
2. **Schema Separation**:
   * Entities in the `"Government"` category list must map exactly to the keys defined in the original `"Structure"` key.
   * Entities in all other 17 categories must map exactly to the Standard schema keys.
3. **Data Quality Restrictions**:
   * To prevent "TBD" or dummy values, fields must be checked against a blacklist of placeholders (case-insensitive exact match and domain/email substring checks).
   * Key string fields like `Description` and `Notes` must meet a minimum length constraint (e.g., 10 characters).
   * URL and Email validation must be enforced using strict regex matches.
4. **Duplicate Prevention**:
   * Entity names must be normalized (lowercased, whitespace collapsed) and tracked globally to prevent duplicates.
   * Official websites must be normalized (ignoring protocol, `www.`, and trailing slashes) and checked for uniqueness across the entire dataset.
5. **Completeness Constraint**:
   * The sum of sizes of the `"Entities"` lists across all 18 categories must be verified to be $\ge 150$.

---

## 3. Caveats
* **Optional Fields**: We assume that `LinkedIn` and `Phone` are optional in the Standard schema. If they are provided, they must match valid formats; if they are not provided, they can be empty strings. All other fields are mandatory and cannot be empty.
* **Metadata Equality**: We assume that the metadata fields in `ContentForFunding_Expanded.json` (such as `Why`, `Priority`, `Category_For_Company`, and `Structure`) must match the source file `ContentForFunding.json` exactly to verify that scrapers do not modify the category-level definition itself.

---

## 4. Conclusion
We have completed the design and blueprint for the E2E verification test harness.
* The detailed script structure is proposed in `analysis.md` in this directory.
* The mock data testing strategy including valid and invalid dummy datasets has been defined.
* A Python-based verification script blueprint has been written, ready to be picked up by the implementer agent.

---

## 5. Verification Method
To verify that this design satisfies the requirements:
1. **Design Review**: Inspect `d:/projects/laravel_projects/college_project/.agents/explorer_e2e_1/analysis.md` to review the proposed Python script code structure, URL/Email regex, and mock data designs.
2. **Implementation Verification**: Once the implementer agent writes `verify_funding_db.py` and the dummy files:
   * Execute `python verify_funding_db.py` against the valid dummy JSON file (expected exit code `0`).
   * Execute `python verify_funding_db.py` against the invalid dummy JSON file (expected exit code `1` with descriptive error logs).
