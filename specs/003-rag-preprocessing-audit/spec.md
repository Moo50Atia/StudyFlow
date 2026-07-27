# Feature Specification: RAG Preprocessing Audit

**Feature Branch**: `[003-rag-preprocessing-audit]`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Semantic Search Context Retrieval (Priority: P1)

The RAG system performs a semantic search over the vector index to retrieve specific, highly relevant chunks of the book that precisely answer user queries (e.g., "What is inheritance?"). The retrieved chunks are complete explanations rather than cut-off fragments.

**Why this priority**: The primary value of a RAG system depends on the semantic completeness of the retrieved chunks. If chunks are arbitrarily split, the LLM will generate poor answers.

**Independent Test**: Can be fully tested by verifying that a search for a specific concept returns a standalone chunk that contains the entire definition, code example, or table without arbitrary truncation.

**Acceptance Scenarios**:

1. **Given** a document with a code example and explanation, **When** chunked, **Then** the code example and its explanation are kept within the same chunk.
2. **Given** a 114-page book, **When** processed by the pipeline, **Then** it produces multiple semantic chunks of 4000-7000 characters rather than a single monolithic chunk.

---

### User Story 2 - Metadata Filtering (Priority: P2)

The RAG application filters search results using specific metadata to narrow down the search space to a particular lecture, section, or page range, thus improving retrieval accuracy and reducing hallucinations.

**Why this priority**: Filtering by lecture or topic is essential to provide targeted answers within a specific domain or chapter.

**Independent Test**: Can be fully tested by verifying that `knowledge_index.json` contains complete metadata properties for every chunk, enabling precise queries.

**Acceptance Scenarios**:

1. **Given** a generated chunk, **When** inspecting its metadata, **Then** it contains a `semantic_path` (e.g. Programming -> OOP -> Inheritance), `lecture_id`, and `page_start`/`page_end`.
2. **Given** a subset of chunks belonging to a specific lecture, **When** filtering the index by `lecture_id`, **Then** only chunks from that lecture are returned.

---

### User Story 3 - Vector Database Interoperability (Priority: P3)

The AI engineering team takes the generated artifacts (`vectors.json`, `knowledge_index.json`) and loads them into a production vector database (like Qdrant, FAISS, or Pinecone) without needing to clean or restructure the data.

**Why this priority**: The current backend is local JSON, but production will use a real vector DB. The structure must be compatible out-of-the-box.

**Independent Test**: Can be fully tested by validating that the vectors and chunk manifests have exactly a 1-to-1 mapping and use deterministic hashing for IDs.

**Acceptance Scenarios**:

1. **Given** a list of chunks and vectors, **When** counting them, **Then** the count is exactly the same and no orphan records exist.
2. **Given** the JSON structures, **When** importing to a mock vector DB format, **Then** no missing keys or mismatched dimensions occur.

### Edge Cases

- What happens when a section or subsection is far smaller than the 4000-character target limit? (Should it be merged with the next section or kept separate to preserve semantic boundaries?)
- What happens when a single code block or table exceeds the 7000-character upper bound?
- How does the system handle tables that span across page boundaries when mapping `page_start` and `page_end`?
- How are duplicate texts (e.g., headers repeated on every page) handled during deterministic hashing?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST chunk documents based on semantic hierarchy with this priority order: Lecture > Section > Subsection > Heading hierarchy > Character limit fallback.
- **FR-002**: The system MUST NOT split text in the middle of explanations, code examples, mathematical derivations, tables, or figure descriptions.
- **FR-003**: The system MUST target chunk sizes of 800–1500 tokens or 4000–7000 characters.
- **FR-004**: The system MUST implement overlap of 300–500 characters exclusively between adjacent chunks.
- **FR-005**: Every chunk MUST contain the following metadata: `chunk_id`, `document_id`, `lecture_id`, `lecture_title`, `section_title`, `subsection_title` (if applicable), `page_start`, `page_end`, `start_offset`, `end_offset`, `token_estimate`, `character_count`, `chunk_hash`, `source_file`, and `semantic_path`.
- **FR-006**: The system MUST map each vector to exactly one semantic chunk (no entire-book or multi-lecture embeddings).
- **FR-007**: The system MUST detect duplicate chunks and use deterministic hashing.
- **FR-008**: The system MUST produce a `knowledge_index.json` that supports metadata filtering by lecture, pages, topic, and section.
- **FR-009**: The system MUST ensure strict referential integrity between `manifest.json`, `chunk_manifest.json`, `vectors.json`, and `knowledge_index.json` (zero orphans).
- **FR-010**: The preprocessing pipeline architecture, extraction, OCR, and structure generation MUST NOT be modified unless absolutely required.
- **FR-011**: The system MUST output an engineering report detailing problems found, changes made, modified files, backward compatibility, performance impact, and retrieval improvements.

### Key Entities

- **Chunk**: A semantically complete segment of text, constrained by length and logical boundaries, containing rich hierarchical metadata.
- **Vector**: A high-dimensional numerical representation of a single Chunk.
- **Knowledge Index Entry**: The metadata record linking a Chunk to its Vector and enabling filtering/routing during retrieval.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of generated chunks preserve code blocks, tables, and mathematical formulas without internal splits.
- **SC-002**: 100% referential integrity exists between chunks and vectors (1:1 mapping, 0 orphans).
- **SC-003**: 95%+ of chunks fall within the 4000-7000 character bound unless restricted by unbreakable semantic blocks.
- **SC-004**: `knowledge_index.json` successfully contains all 15 required metadata fields for every single chunk.
- **SC-005**: Processing the 114-page book completes successfully without out-of-memory exceptions and supports future vector DBs (FAISS, Milvus, etc.).

## Assumptions

- The existing Gemini Embeddings integration works correctly and accurately returns vectors.
- Target RAG system can handle inputs up to 1500 tokens per chunk.
- The OCR and Extraction stages already provide enough raw formatting markers (like Markdown or JSON blocks) to identify code examples, tables, and headings correctly.
- A basic token estimation approach (e.g., characters / 4) is acceptable for the `token_estimate` field if a tokenizer is not explicitly provided.
