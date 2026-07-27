# Data Model: Knowledge Intelligence Engine (KIE)

**Feature:** Knowledge Intelligence Engine (KIE)  
**Spec Directory:** [specs/001-knowledge-intelligence-engine/](file:///d:/projects/laravel_projects/college_project/specs/001-knowledge-intelligence-engine/)

---

## 1. Core Data Entities

### 1.1 Knowledge Asset (`KnowledgeAssetV2`)
* **Purpose:** Canonical educational entity representing a specific concept, formula, law, analogy, or case study.
* **Key Fields:** `asset_id` (UUID), `material_id`, `asset_type`, `title`, `content_primary`, `relationships` (Array of typed links), `quality_score` (Object), `version_history` (Array of version diffs), `provenance` (Source offsets), `lifecycle_state`.
* **Lifecycle States:** `RAW`, `EXTRACTED`, `REVISED`, `REJECTED`, `VALIDATED`, `APPROVED`, `PUBLISHED`, `ARCHIVED`, `DEPRECATED`, `ROLLED_BACK`.

### 1.2 Knowledge Fragment (`KnowledgeFragment`)
* **Purpose:** Atomic text chunk (100–300 tokens) derived from a Knowledge Asset for vector embedding and BM25 indexing.
* **Key Fields:** `fragment_id` (UUID), `asset_id` (UUID), `material_id`, `chunk_index`, `token_count`, `content_text`, `context_prefix`, `provenance`, `embedding_checksum`.

### 1.3 Embedding Registry (`EmbeddingRegistry`)
* **Purpose:** Registry metadata tracking active embedding model, dimensions, normalization, and checksums.
* **Key Fields:** `registry_id`, `material_id`, `embedding_model`, `dimensions`, `normalization_method`, `creation_timestamp`, `checksum`, `compatibility_version`.

### 1.4 Index Registry (`IndexRegistry`)
* **Purpose:** Registry tracking active vector, BM25, and graph indices.
* **Key Fields:** `index_id`, `material_id`, `index_type`, `total_entries`, `index_status`, `created_at_stage`, `generator_metadata`, `associated_embedding_registry_id`.

### 1.5 Evidence Package (`EvidencePackage`)
* **Purpose:** Output audit payload emitted with every generated response.
* **Key Fields:** `package_id`, `query_text`, `response_text`, `confidence_band`, `confidence_score`, `planner_decision_log_id`, `retrieved_asset_ids`, `citation_map`, `prompt_template_version`, `model_version`, `execution_latency_ms`.

---

## 2. Entity Relationships Diagram

```
[ PDF Document ]
      │
      ▼
[ Knowledge Asset ] ── (Has 1..N) ──► [ Knowledge Fragment ] ── (Mapped to) ──► [ Dense Embedding Vector ]
      │                                                                                │
      ├── (Connects via) ──► [ Typed Relationship ]                                   │
      │                                                                                ▼
      └── (Tracked in) ────► [ Quality Score & Version History ]              [ Index Registry ]
```
