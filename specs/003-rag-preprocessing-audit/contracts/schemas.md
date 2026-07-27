# JSON Schemas: RAG Preprocessing Audit

This document contains the JSON Schema definitions for the artifacts produced by the preprocessing stages.

---

## 1. Chunk Manifest Schema (`chunk_manifest.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChunkManifest",
  "type": "object",
  "required": ["source_file", "total_chunks", "total_characters", "total_pages", "chunk_target_size", "chunk_overlap", "chunks"],
  "properties": {
    "source_file": { "type": "string" },
    "total_chunks": { "type": "integer" },
    "total_characters": { "type": "integer" },
    "total_pages": { "type": "integer" },
    "chunk_target_size": { "type": "integer" },
    "chunk_overlap": { "type": "integer" },
    "chunks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "id", "document_id", "lecture_id", "lecture_title", "section_title",
          "page_start", "page_end", "start_offset", "end_offset",
          "token_estimate", "character_count", "chunk_hash", "source_file", "semantic_path"
        ],
        "properties": {
          "id": { "type": "string" },
          "document_id": { "type": "string" },
          "lecture_id": { "type": "string" },
          "lecture_title": { "type": "string" },
          "section_title": { "type": "string" },
          "subsection_title": { "type": ["string", "null"] },
          "page_start": { "type": "integer" },
          "page_end": { "type": "integer" },
          "start_offset": { "type": "integer" },
          "end_offset": { "type": "integer" },
          "token_estimate": { "type": "integer" },
          "character_count": { "type": "integer" },
          "chunk_hash": { "type": "string" },
          "source_file": { "type": "string" },
          "semantic_path": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 2. Vectors Schema (`vectors.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VectorManifest",
  "type": "object",
  "required": [
    "document_id", "schema_version", "created_at", "source_file",
    "total_vectors", "embedding_model", "embedding_provider",
    "vector_dimension", "total_characters", "total_pages", "vectors"
  ],
  "properties": {
    "document_id": { "type": "string" },
    "schema_version": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "source_file": { "type": "string" },
    "total_vectors": { "type": "integer" },
    "embedding_model": { "type": "string" },
    "embedding_provider": { "type": "string" },
    "vector_dimension": { "type": "integer" },
    "total_characters": { "type": "integer" },
    "total_pages": { "type": "integer" },
    "vectors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "chunk_id", "chunk_hash", "start_page", "end_page",
          "char_count", "token_estimate", "start_char_offset", "end_char_offset",
          "embedding"
        ],
        "properties": {
          "chunk_id": { "type": "string" },
          "chunk_hash": { "type": "string" },
          "start_page": { "type": "integer" },
          "end_page": { "type": "integer" },
          "char_count": { "type": "integer" },
          "token_estimate": { "type": "integer" },
          "start_char_offset": { "type": "integer" },
          "end_char_offset": { "type": "integer" },
          "embedding": {
            "type": "array",
            "items": { "type": "number" }
          }
        }
      }
    }
  }
}
```

---

## 3. Knowledge Index Schema (`knowledge_index.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KnowledgeIndex",
  "type": "object",
  "required": [
    "index_id", "document_id", "schema_version", "created_at",
    "source_file", "total_entries", "embedding_model", "vector_dimension",
    "backend", "entries"
  ],
  "properties": {
    "index_id": { "type": "string" },
    "document_id": { "type": "string" },
    "schema_version": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "source_file": { "type": "string" },
    "total_entries": { "type": "integer" },
    "embedding_model": { "type": "string" },
    "vector_dimension": { "type": "integer" },
    "backend": { "type": "string" },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "entry_id", "chunk_id", "chunk_hash", "text",
          "start_page", "end_page", "char_count", "token_estimate",
          "embedding", "metadata"
        ],
        "properties": {
          "entry_id": { "type": "string" },
          "chunk_id": { "type": "string" },
          "chunk_hash": { "type": "string" },
          "text": { "type": "string" },
          "start_page": { "type": "integer" },
          "end_page": { "type": "integer" },
          "char_count": { "type": "integer" },
          "token_estimate": { "type": "integer" },
          "embedding": {
            "type": "array",
            "items": { "type": "number" }
          },
          "metadata": {
            "type": "object",
            "required": [
              "source_file", "document_id", "lecture_id", "lecture_title",
              "section_title", "page_start", "page_end", "start_offset", "end_offset",
              "token_estimate", "character_count", "chunk_hash", "semantic_path"
            ]
          }
        }
      }
    }
  }
}
```
