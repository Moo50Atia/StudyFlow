# Data Model: RAG Preprocessing Audit

This document defines the schemas, validations, and constraints for the data entities involved in the preprocessing pipeline.

---

## 1. Entity Definitions

### Chunk (in `chunk_manifest.json`)
Represents a semantically complete section of the source document.

| Field Name | Type | Description | Validation/Constraint |
|---|---|---|---|
| `id` | `str` | Stable, deterministic chunk ID | `chunk_[a-f0-9]{12}` (12-char SHA-256 prefix) |
| `document_id` | `str` | Unique document ID | UUID v4 |
| `lecture_id` | `str` | Unique lecture ID | Slug or UUID |
| `lecture_title` | `str` | Pedagogical title of the lecture | Non-empty |
| `section_title` | `str` | Heading or chapter name | Non-empty |
| `subsection_title`| `Optional[str]` | Sub-heading name | Optional |
| `page_start` | `int` | Start page in source PDF | `>= 1` |
| `page_end` | `int` | End page in source PDF | `>= page_start` |
| `start_offset` | `int` | Start char offset in full text | `>= 0` |
| `end_offset` | `int` | End char offset in full text | `>= start_offset` |
| `token_estimate` | `int` | Estimated token count | `character_count / chars_per_token` |
| `character_count` | `int` | Exact character count | `4000` to `7000` (target range) |
| `chunk_hash` | `str` | Full content hash | SHA-256 |
| `source_file` | `str` | Source PDF filename | E.g., `source.pdf` |
| `semantic_path` | `str` | Hierarchical routing string | `Lecture -> Section -> Subsection` |

---

### ChunkManifest
Container for all generated chunks of a specific document.

| Field Name | Type | Description | Validation/Constraint |
|---|---|---|---|
| `source_file` | `str` | Original file path/name | Non-empty |
| `total_chunks` | `int` | Number of chunks | Matches `len(chunks)` |
| `total_characters`| `int` | Total chars in full text | Sum of non-overlapping chars |
| `total_pages` | `int` | Total pages in document | `>= 1` |
| `chunk_target_size`| `int` | Configured target size | `4000` to `7000` characters |
| `chunk_overlap` | `int` | Configured overlap | `300` to `500` characters |
| `chunks` | `list[Chunk]` | Ordered list of chunks | Non-empty |

---

### ChunkVector (in `vectors.json`)
The vector representation of a chunk.

| Field Name | Type | Description | Validation/Constraint |
|---|---|---|---|
| `chunk_id` | `str` | Matches parent Chunk's ID | Must exist in `chunk_manifest.json` |
| `chunk_hash` | `str` | Content hash | Matches parent Chunk's hash |
| `embedding` | `list[float]` | Embedding vector coefficients | Length matches model dimension (e.g., 768) |

---

### IndexEntry (in `knowledge_index.json`)
The retrieval-ready entry containing text, vector, and search metadata.

| Field Name | Type | Description | Validation/Constraint |
|---|---|---|---|
| `entry_id` | `str` | Unique indexing entry ID | `idx_[0-9]{4}` |
| `chunk_id` | `str` | Source chunk reference | Must exist in `chunk_manifest.json` |
| `text` | `str` | Full chunk text content | Exact match with text slice |
| `embedding` | `list[float]` | Vector coordinates | Length matches model dimension |
| `metadata` | `dict` | Extensible metadata payload | Must contain the 15 required fields |

---

## 2. Referential Integrity Constraints (Zero Orphans)

To achieve **SC-002**, the system enforces strict validation gates:
1. **Uniqueness**: Every `chunk_hash` must be unique in `chunk_manifest.json`. Duplicate contents are merged into a single chunk entry.
2. **1-to-1 Mapping**:
   * For every chunk in `chunk_manifest.json` $\rightarrow$ exactly one entry in `vectors.json`.
   * For every vector in `vectors.json` $\rightarrow$ exactly one entry in `knowledge_index.json`.
3. **Offset Validation**:
   * For every entry, `full_text[start_offset:end_offset]` must exactly match the `text` attribute stored in the index.
