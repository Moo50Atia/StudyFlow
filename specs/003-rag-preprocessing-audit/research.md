# Research Log: RAG Preprocessing Audit

This document details the architectural decisions, design choices, and alternatives evaluated for implementing the RAG Preprocessing Audit feature.

---

## Decision 1: Hierarchical Semantic Chunking and Heading Detection

* **Decision**: Implement a heuristic header and layout detector during the `chunk` stage (Stage 4), combined with a post-structure enrichment pass in the pipeline to update metadata once the official `structure.json` is generated.
* **Rationale**: The pipeline's stage ordering (Chunking = Stage 4, Structure Extraction = Stage 8) means that the official `structure.json` is not available when chunks are created. A dual-pass solution is chosen:
  1. The chunker performs a heuristic scan of the extracted plain text to detect slide/heading headers (e.g., using double-newline transitions and page offset mappings).
  2. The pipeline's final stage (or structure stage) runs an enrichment pass to map each chunk's `start_char_offset` and `end_char_offset` to the corresponding official Chapter and Lesson from `structure.json`, updating the fields in `chunk_manifest.json` and `knowledge_index.json`.
* **Alternatives Considered**:
  * **Reordering Pipeline Stages**: Moving structure extraction before chunking. Rejected because structure extraction itself depends on chunks to avoid sending monolithic texts to the LLM (violates FR-010).
  * **Pure Heuristic Chunking**: Relying only on regex. Rejected because it cannot guarantee alignment with the pedagogical lesson boundaries defined by the AI.

---

## Decision 2: Prevention of Splits in Unbreakable Semantic Blocks

* **Decision**: Implement an interval-based boundary adjustment algorithm. The scanner pre-detects coordinates of:
  * **Code Blocks**: Scanning for block boundaries, programming keywords (`class`, `void`, `main`), and matching brace depth `{}`.
  * **Tables**: Scanning for line-by-line tabular spacing or grid layout patterns.
  * **Math Formulas**: Scanning for equation syntax, operator density, and block-aligned mathematical equations.
  * **Figure Captions**: Scanning for "Figure X:" or "Fig X:" prefixes.
  When a chunk split is requested at target character limit or page break, the split index is shifted to the nearest boundary outside these active intervals.
* **Rationale**: Meets SC-001 (100% preservation of code blocks and tables) with mathematical precision and without incurring LLM API costs during chunking.
* **Alternatives Considered**:
  * **LLM-based Chunking**: Using an LLM to decide split points. Rejected due to cost, latency, and context limits for large books (e.g., the 114-page PDF).

---

## Decision 3: Stable Deterministic Hashing for Chunk IDs

* **Decision**: Use SHA-256 hashing of the normalized text content to generate stable, unique chunk IDs (e.g., `chunk_[hash_prefix]`).
* **Rationale**: Ensures duplicate text segments (e.g. repeated page headers/footers) are mapped to a single chunk ID, avoiding redundant vector generation. Provides stable references that remain unchanged across runs unless the source content is altered.
* **Alternatives Considered**:
  * **Sequential IDs**: (Current implementation `chunk_001`, `chunk_002`). Rejected because any small change shifts all downstream IDs, breaking external database alignments and making incremental updates impossible.

---

## Decision 4: Standardizing 15-Field Metadata Payload

* **Decision**: Enforce a strict schema containing all 15 required metadata fields across `Chunk` (in `chunk_schema.py`), `ChunkVector` (in `schema.py`), and `IndexEntry` (in `schema.py`).
* **Rationale**: Simplifies integration with vector databases like Qdrant/FAISS, as the metadata fields are populated uniformly and validated by Pydantic.
* **Alternatives Considered**:
  * **Dynamic Payload Dicts**: Storing arbitrary key-value pairs. Rejected because it easily leads to schema drift and missing fields, violating SC-004.
