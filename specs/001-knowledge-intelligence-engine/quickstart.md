# Quickstart Validation Guide: Knowledge Intelligence Engine (KIE)

**Feature:** Knowledge Intelligence Engine (KIE)  
**Spec Directory:** [specs/001-knowledge-intelligence-engine/](file:///d:/projects/laravel_projects/college_project/specs/001-knowledge-intelligence-engine/)

---

## Runnable Validation Scenarios

### Scenario 1: Pipeline Knowledge Processing Phase Execution
1. Run Stage 7A through 7D against test curriculum material (`test_phys_101.pdf`).
2. **Verification Check 1:** Verify that `relationships.json` and `knowledge_graph.json` are created in `Generating/Materials/test_phys_101/`.
3. **Verification Check 2:** Verify that `knowledge_assets.json` and `knowledge_fragments.json` pass schema validation against `KA-SCHEMA-2` and `KF-SCHEMA-1`.
4. **Verification Check 3:** Verify that `embedding_registry.json` and `index_registry.json` list active indices with non-zero vector entry counts.

### Scenario 2: Grounded Q&A Search with Evidence Package Output
1. Issue query: *"Explain Newton's Second Law with formula and Egyptian Arabic analogy."*
2. **Verification Check 1:** Confirm `PlannerDecisionLog` records selected strategies (`DenseStrategy`, `BM25Strategy`, `GraphStrategy`).
3. **Verification Check 2:** Confirm response contains green inline citations and emitted `EvidencePackage` passes JSON validation with `confidence_band` equal to `VERY_HIGH` or `HIGH`.

### Scenario 3: Out-of-Scope Query Abstention Test
1. Issue out-of-scope query: *"How do I bake a chocolate cake?"*
2. **Verification Check 1:** Confirm `confidence_band` is evaluated as `UNSUPPORTED`.
3. **Verification Check 2:** Confirm system output explicitly abstains: *"The requested topic is not covered in your course materials."*
