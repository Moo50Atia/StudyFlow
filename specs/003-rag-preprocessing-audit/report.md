# Engineering Report: RAG Preprocessing Audit

## Overview
This report details the implementation of the RAG Preprocessing Audit (Specs 003). The objective was to transform a simplistic, character-based chunking pipeline into a deterministic, context-aware semantic pipeline optimized for Retrieval-Augmented Generation (RAG).

## Key Accomplishments

### 1. Semantic Search Context Retrieval (User Story 1)
- **Problem**: Original pipeline blindly split text at arbitrary character limits, destroying code blocks, math formulas, and tables, causing severe context fragmentation for the LLM.
- **Solution**: 
  - Implemented an `unbreakable block scanner` to detect Markdown code blocks, LaTeX math formulas, and Markdown tables.
  - Added a `heading heuristic detection` mechanism that aligns chunk boundaries with heading structures.
  - Implemented an interval-aware boundary adjustment algorithm that respects strict token limits (800-1500 tokens target, hard max 1800) while preventing arbitrary truncation.
- **Result**: Chunks now retain full semantic context. Code and tables are kept intact, significantly improving retrieval quality and context cohesiveness.

### 2. Metadata Filtering and Enrichment (User Story 2)
- **Problem**: Index metadata was just an untyped dictionary capturing basic file name and character offsets, which is insufficient for database filtering in advanced RAG scenarios.
- **Solution**:
  - Defined a strict Pydantic model (`IndexMetadata`) ensuring 15 critical schema fields.
  - Restructured the pipeline order (`route` and `structure` run prior to `index`), passing semantic hierarchy data (lecture IDs, section IDs, chapters, titles) directly to the chunk index mappings.
- **Result**: `knowledge_index.json` now includes precise hierarchical tags for every chunk, enabling precise query filtering by curriculum structure (e.g. "Only search within Unit 2, Section 3").

### 3. Vector Database Interoperability (User Story 3)
- **Problem**: Referential integrity was non-existent. Chunks used sequential string IDs (e.g., `chunk_001`), risking orphan chunks, duplication loops, and state invalidation on document updates.
- **Solution**:
  - Implemented deterministic SHA-256 chunk hashing (`text|start_page|end_page`) ensuring stable identifiers across pipeline executions.
  - Implemented deduplication merging at the chunk stage.
  - Enforced a strict 1:1 pipeline completion referential integrity check across `chunk_manifest.json`, `vectors.json`, and `knowledge_index.json`.
- **Result**: Complete 1:1 data mapping guaranteed. No orphan embeddings. Updates to documents will only trigger re-vectorization on modified chunks (enabling future caching optimizations).

## Pipeline Architecture Changes
The 12-stage pipeline was updated to ensure that structure extraction occurs *before* index generation:
1. Extract
2. OCR
3. Chunk (Deduplicated, Semantically aligned)
4. Vectorize (Generate SHA-256 mappings)
5. Route Detection
6. Structure Extraction (LLM hierarchy generation)
7. Index (Integrate vectors, chunks, and structure)
8. Knowledge Graph...

## Benchmarks & Testing
- An end-to-end regression validation ran perfectly on the `Unit 2 - Objects and Classes - SP25.pdf` file.
- The system automatically halts pipeline execution via HITL pauses or raises a `RuntimeError` if chunk manifests and vector manifests fall out of alignment.
- A test suite verifies boundary alignment, required metadata fields, 1:1 mapping, and reproducible hashing.

## Future Recommendations
- Implement a dedicated caching layer for LLM vector embeddings to reduce costs during partial PDF updates, fully leveraging the new deterministic hash architecture.
- Expand visual asset detection to map `contains_images` dynamically to bounded box coordinates for multimodal retrieval.
