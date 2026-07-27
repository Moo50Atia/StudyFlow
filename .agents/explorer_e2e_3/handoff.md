# Handoff Report: E2E Verification Track (Explorer 3)

## 1. Observation
We analyzed the following artifacts, requirements, and previous proposals in the workspace:
* **E2E Testing Scope** (`.agents/sub_orch_e2e_testing/SCOPE.md`):
  > `- Target file: verify_funding_db.py`
  > `- Setup test runner, validation rules, compliance checks, and target verification constraints.`
* **Parent Project Contract** (`.agents/orchestrator/PROJECT.md`):
  > `### verify_funding_db.py API Contract`
  > `- Must read Funding/ContentForFunding_Expanded.json and validate that:`
  > `  1. It exists and is valid JSON.`
  > `  2. It has the same categories and hierarchy as Funding/ContentForFunding.json.`
  > `  3. Every entity conforms to its schema (Government vs Standard).`
  > `  4. There are no placeholder values, fake emails, or dummy websites.`
  > `  5. There are no duplicate names or websites.`
  > `  6. The database contains at least 150+ verified entities.`
  > `- Must return exit code 0 on success, non-zero on failure.`
* **Source Categories Config** (`Funding/ContentForFunding.json`):
  Defines 18 distinct categories (e.g. `Universities`, `Research Centers`, ..., `Government`). For example, `Universities` is defined as:
  ```json
  "Universities": {
      "Why": "Research partnerships, incubation, grants, labs, professors, competitions.",
      "Priority": "Critical",
      "Category_For_Company": [
          "Research Project",
          "AI Startup",
          "EdTech",
          "University Collaboration"
      ]
  }
  ```
* **Structural Discrepancy between Prior Explorers**:
  * **Explorer 1** (`.agents/explorer_e2e_1/handoff.md` line 47):
    > `Preserving Hierarchy: Because ContentForFunding.json contains metadata ... we propose that the expanded file ContentForFunding_Expanded.json maps each category to an object that preserves all original keys and appends an "Entities" key containing the list of entity records.`
  * **Explorer 2** (`.agents/explorer_e2e_2/analysis.md` line 334):
    > `for category, entities in target_categories_root.items():`
    > `    if not isinstance(entities, list):`
* **Standard Category Schema** (`.agents/worker_m1/ORIGINAL_REQUEST.md` line 10):
  > `All other categories: Name, Category, Category_For_Company, Priority, Country, City, Official_Website, Official_Email, LinkedIn, Phone, Description.`

---

## 2. Logic Chain
1. **Hierarchy Preservation**: By comparing the category keys in `ContentForFunding.json` with the two proposed designs, mapping a category key directly to a list of entities (Explorer 2's design) discards category-level config metadata (`Why`, `Priority`, `Category_For_Company`). Therefore, to satisfy the requirement *"It has the same categories and hierarchy as Funding/ContentForFunding.json"*, the expanded file must match the source file structure exactly, with the actual entity lists nested within an `"Entities"` key (Explorer 1's design).
2. **Schema Separation**:
   * Entities in the `"Government"` category must map exactly to the keys defined in the original `"Structure"` key in `ContentForFunding.json`.
   * Entities in all other 17 categories must map exactly to the Standard schema keys.
3. **Data Quality Restriction**:
   * The verifier must check all fields against a case-insensitive exact and substring placeholder blacklist (`TBD`, `placeholder`, `fake`, `dummy`, `example.com`, etc.).
   * String fields like `Description` must meet a minimum length constraint (e.g., 10 characters) to avoid short, non-descriptive placeholders.
   * Format validations for URLs, emails, and phone numbers must be enforced using strict regexes.
4. **Duplicate Prevention**:
   * Entity names must be normalized (lowercased, corporate suffixes like `Inc.`, `LLC`, `Ltd.` removed, non-alphanumeric chars stripped) and tracked globally.
   * Official websites must be normalized (removing protocols, `www.`, and trailing slashes) and checked for uniqueness across the entire dataset.
5. **Volume Verification**:
   * The sum of entity counts across all 18 categories must be verified to be $\ge 150$.
6. **Testing via Python fixture**:
   * The test runner should use pytest's `tmp_path` fixture to dynamically test edge cases (such as duplicate names, missing fields, format violations) against `verify_funding_db.py` without writing permanent mock files to the workspace.

---

## 3. Caveats
* **Optional Fields**: `LinkedIn` and `Phone` are assumed optional in the Standard schema. If present, they must be formatted correctly; if absent, they can be empty strings. All other fields are mandatory.
* **Metadata Equality**: We assume that category-level metadata fields (like `Why`, `Priority`, etc.) must match the source config exactly to prevent scrapers from corrupting configuration.

---

## 4. Conclusion
We synthesized the E2E verification requirements and reconciled the differences between previous designs:
* We recommend the **Nested Object structure** to preserve original metadata hierarchy.
* We recommend a **Robust Normalization** strategy to prevent duplicate name/website evasion.
* We defined complete designs for the verification script `verify_funding_db.py` and the `pytest`-based test runner `test_verify_funding_db.py` (documented in `analysis.md` in this directory).
* We designed dummy valid and invalid datasets for manual validation testing (documented in `analysis.md` in this directory).

---

## 5. Verification Method
To verify the E2E testing design:
1. **Inspect Artifacts**: Check `analysis.md` in this folder for the proposed Python code and JSON schema models.
2. **Run Test Harness**: Once the implementer writes the script and tests, run:
   ```bash
   pytest test_verify_funding_db.py
   ```
   Confirm all test cases pass.
3. **Test CLI**: Execute:
   ```bash
   python verify_funding_db.py Funding/ContentForFunding_Expanded.json
   ```
   Confirm it fails if the file doesn't exist, and passes with exit code 0 when database expansion is complete.
