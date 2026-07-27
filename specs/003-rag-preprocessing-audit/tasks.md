# Tasks: RAG Preprocessing Audit

**Input**: Design documents from `/specs/003-rag-preprocessing-audit/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are requested and included to verify semantic chunk boundaries, metadata filtering, and referential integrity.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `Generating/` at repository root level for backend pipeline modules, `tests/` for pipeline verification tests.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize git branch and verify pytest environment in repository root
- [X] T002 Update chunk size settings (to 800-1500 tokens, approx 2500-5000 characters, hard upper limit 1800 tokens to align with token-oriented chunking) and overlap (to 300-500 chars) in Generating/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Define environment variable overrides for chunk size constraints (token-oriented: 800-1500 tokens / 2500-5000 characters, hard upper limit 1800 tokens) in Generating/config.py
- [X] T004 Create helper test datasets and mock document generators in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Semantic Search Context Retrieval (Priority: P1) 🎯 MVP

**Goal**: Split documents into 800-1500 token chunks (approx 2500-5000 characters, hard upper limit 1800 tokens, token-oriented chunking) using heading heuristics and page alignment while keeping code blocks, tables, math formulas, and figure captions unbroken.

**Independent Test**: Run `pytest tests/test_chunk_boundaries.py` to verify chunks are 800-1500 tokens (approx 2500-5000 characters, hard upper limit 1800 tokens, token-oriented chunking), overlap is 300-500 characters, and code/tables are not split inside.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T005 [P] [US1] Create unit tests for unbreakable blocks (code, math, tables, figures) in tests/test_unbreakable_blocks.py
- [X] T006 [P] [US1] Create integration tests for chunk boundaries, sizes (800-1500 tokens / approx 2500-5000 characters, hard upper limit 1800 tokens, token-oriented chunking), and overlap in tests/test_chunk_boundaries.py

### Implementation for User Story 1

- [X] T007 [US1] Implement slide heading heuristic detection in Generating/Chunking/chunk_manager.py
- [X] T008 [US1] Implement unbreakable block scanner logic in Generating/Chunking/chunk_manager.py
- [X] T009 [US1] Implement interval-aware boundary adjustment algorithm in Generating/Chunking/chunk_manager.py
- [X] T010 [US1] Update chunk schema representation and properties in Generating/Chunking/chunk_schema.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Metadata Filtering (Priority: P2)

**Goal**: Populate 15 required metadata fields (including `semantic_path`, `lecture_id`, `lecture_title`, etc.) for every chunk and entry, enabling precise database filtering.

**Independent Test**: Run `pytest tests/test_metadata_filtering.py` to verify all 15 metadata fields exist in `knowledge_index.json` and filtering by `lecture_id` returns only chunks from that lecture.

### Tests for User Story 2

- [X] T011 [P] [US2] Create unit tests for metadata structure and query filtering in tests/test_metadata_filtering.py

### Implementation for User Story 2

- [X] T012 [P] [US2] Update index and metadata schema representation in Generating/Indexing/schema.py
- [X] T013 [US2] Update index entry mapping and creation logic in Generating/Indexing/indexing_manager.py
- [X] T014 [US2] Implement structural enrichment pass in Generating/pipeline.py to match chunks with the official structure.json hierarchy

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Vector Database Interoperability (Priority: P3)

**Goal**: Ensure 100% referential integrity with zero orphans between `manifest.json`, `chunk_manifest.json`, `vectors.json`, and `knowledge_index.json` using deterministic hashing.

**Independent Test**: Run `pytest tests/test_indexing_integrity.py` to verify 1:1 mapping count, zero orphan entries, and deterministic ID format.

### Tests for User Story 3

- [X] T015 [P] [US3] Create integration tests for 1:1 mapping and deterministic hashing validation in tests/test_indexing_integrity.py

### Implementation for User Story 3

- [X] T016 [P] [US3] Update vector schema representation to support deterministic chunk IDs in Generating/Vectorization/schema.py
- [X] T017 [US3] Implement deterministic hashing logic for chunk IDs in Generating/Vectorization/vectorization_manager.py
- [X] T018 [US3] Implement duplicate chunk detection and merging in Generating/Chunking/chunk_manager.py
- [X] T019 [US3] Enforce strict referential integrity check before pipeline completion in Generating/pipeline.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T020 Run full end-to-end regression validation suite against Unit 2 - Objects and Classes - SP25.pdf
- [X] T021 [P] Create final engineering report in specs/003-rag-preprocessing-audit/report.md
- [X] T022 [P] Update documentation in specs/003-rag-preprocessing-audit/quickstart.md

---

## Phase 7: RAG Validation & Benchmarking

**Purpose**: Validate that the generated preprocessing artifacts are truly ready for Retrieval-Augmented Generation (RAG) and production vector databases.

- [X] T023 [P] Create unit tests for semantic chunk quality (dominant topic, no lecture mixing, no section leakage, heading alignment, semantic boundary score) in tests/test_semantic_chunks.py
- [X] T024 [P] Create retrieval simulation tests (measuring Recall@1, Recall@3, Recall@5; Target Recall@3 >= 95%) in tests/test_retrieval_quality.py
- [X] T025 Generate chunk statistics report outputting total chunks, average chunk size, minimum/maximum size, overlap average, token average, semantic violations, and distribution metrics into Generating/Materials/[material_name]/chunk_statistics.json

### Metadata & Architecture Validation

- [X] T026 [P] Create metadata completeness validation tests (ensure 15 fields, no NULL/empty/placeholder, unique lecture/chunk IDs, valid semantic_path) in tests/test_metadata_validation.py
- [X] T027 [P] Create embedding validation tests (dimension verification, no NaN/Infinity, vector norm > 0, metadata matches) in tests/test_embedding_validation.py
- [X] T028 [P] Create duplicate chunk validation tests (identical chunks generate identical hashes, duplicate detection works, merged chunk metadata matches) in tests/test_duplicate_chunks.py
- [X] T029 [P] Implement tests ensuring incremental processing (unchanged chunks are NOT re-embedded, only modified chunks receive new embeddings, cache reuse correctness) in tests/test_incremental_processing.py
- [X] T030 [P] Create stable hash verification tests (validate identical input produces identical chunk IDs, identical hashes, identical vector IDs, deterministic output) in tests/test_hash_stability.py
- [X] T031 [P] Create manifest consistency validation tests (verify zero orphans, zero missing references, 1:1 mapping, checksum consistency from manifest down to knowledge index) in tests/test_manifest_consistency.py

### Performance & End-State Verification

- [X] T032 [P] Benchmark preprocessing pipeline collecting execution time, memory usage, CPU usage, embedding and indexing throughput in tests/test_performance.py (Target: 114-page textbook processed under one minute)
- [X] T033 Generate a comprehensive final RAG readiness report and readiness percentage in Generating/Materials/[material_name]/rag_readiness_report.json and Generating/Materials/[material_name]/rag_readiness_report.md (verify schema compatibility with Qdrant, FAISS, Chroma, Pinecone, Milvus)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete
- **RAG Validation & Benchmarking (Phase 7)**: Depends on all previous phases being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 and US2

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Phase 7 validation test suites marked [P] can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit tests for unbreakable blocks in tests/test_unbreakable_blocks.py"
Task: "Create integration tests for chunk boundaries, sizes, and overlap in tests/test_chunk_boundaries.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Complete Phase 7 Validation → Run all validation suites, generate final engineering and benchmarking reports. Only after all validation tasks pass should the preprocessing pipeline be considered production-ready.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

### Production Acceptance Criteria

The preprocessing pipeline is considered complete and production-ready only if:

✓ Semantic chunk validation passes (T023)

✓ Retrieval benchmark passes (T024)

✓ Metadata completeness is 100% (T026)

✓ Embedding validation passes (T027)

✓ Referential integrity is 100% (T031)

✓ Duplicate detection passes (T028)

✓ Stable hashing passes (T030)

✓ Performance benchmark passes (T032)

✓ Final RAG readiness report is generated (T033)
