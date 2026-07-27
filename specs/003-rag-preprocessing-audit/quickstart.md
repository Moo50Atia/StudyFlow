# Quickstart & Validation Guide: RAG Preprocessing Pipeline

This document explains how to use the RAG Preprocessing pipeline to convert PDFs into structured, indexable embeddings suitable for Retrieval-Augmented Generation.

## 1. Prerequisites

1. Set your `PYTHONPATH` to the `Interactive-Seens-Material` root directory.
   ```bash
   export PYTHONPATH="Interactive-Seens-Material"
   ```
2. Make sure you have your API Key assigned for vectorization/structure extraction:
   ```bash
   export STUDYFLOW_AI_API_KEY="your_api_key_here"
   ```
3. Poppler utilities (pdftoppm) installed and in PATH (required for PDF extraction/OCR checks).

## 2. Running the Pipeline

The pipeline orchestrates 12 individual processing stages that systematically extract, parse, clean, chunk, route, structure, and embed documents. 

### Full End-to-End Execution
To run a document completely through all stages:
```bash
python Interactive-Seens-Material/Generating/pipeline.py \
  --input "Interactive-Seens-Material/Generating/Unit 2 - Objects and Classes - SP25.pdf" \
  --name Unit2
```
*Note: Depending on configuration, the pipeline will issue a HITL (Human-in-the-Loop) pause after structure generation to allow manual review of the generated structure.*

### Single Stage Execution
To run a specific stage (e.g. testing just the vectorization on an already chunked document):
```bash
python Interactive-Seens-Material/Generating/pipeline.py \
  --name Unit2 \
  --stage vectorize
```

### Fast Index Testing
To validate chunking, vectorization, and indexing output quickly without executing subsequent expensive graph generation routines:
```bash
python Interactive-Seens-Material/Generating/pipeline.py \
  --input "Interactive-Seens-Material/Generating/Unit 2 - Objects and Classes - SP25.pdf" \
  --name Unit2_Test \
  --index-test
```

## 3. Generated Outputs

Executing the index test generates several output files in `Interactive-Seens-Material/Generating/Materials/[name]/`:
- **`chunk_manifest.json`**: Semantic, token-oriented chunks maintaining strict integrity for code blocks and tables. Each chunk uses a deterministic SHA-256 identifier.
- **`vectors.json`**: Mathematical embeddings mappings tied identically to the chunk identifiers.
- **`structure.json`**: LLM-extracted document hierarchical framework.
- **`knowledge_index.json`**: Consolidated records incorporating the chunk text, vector embeddings, and 15 strict structure-enriched metadata fields (ready to be injested into Qdrant/Pinecone).

## 4. Validation Scenarios

### Scenario A: Semantic Boundaries Check
* **Goal**: Verify that code blocks are not split across chunks and boundaries align with headings.
* **Validation**: Run the verification script:
  ```powershell
  pytest Generating/tests/test_chunk_boundaries.py
  ```

### Scenario B: Referential Integrity Check
* **Goal**: Assert 1:1 matching between vector manifest and knowledge index entries, with zero orphans.
* **Validation**: Run:
  ```powershell
  pytest Generating/tests/test_indexing_integrity.py
  ```

### Scenario C: Metadata Verification
* **Goal**: Ensure all 15 metadata fields exist and are populated with correct types.
* **Validation**: Run:
  ```powershell
  pytest Generating/tests/test_metadata_filtering.py
  ```
