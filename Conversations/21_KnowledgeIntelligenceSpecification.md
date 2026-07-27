# 21. Knowledge Intelligence Engine (KIE) Specification

---

> **Document Metadata**  
> **Document Identifier:** `21_KnowledgeIntelligenceSpecification.md`  
> **Layer:** Layer 5 (Topic-Specific Enterprise Specification)  
> **Version:** 2.0.0  
> **Status:** Official Specification  
> **Authority:** Chief Software Architect & AI Systems Architect  
> **Applies To:** Platform Knowledge Core, Python AI Pipeline, Retrieval Engine, Learning Services, Analytics Engine, Registries  
> **Parent Documents:** [00_DocumentationStandards.md](file:///d:/projects/laravel_projects/college_project/Conversations/00_DocumentationStandards.md), [01_ProjectVision.md](file:///d:/projects/laravel_projects/college_project/Conversations/01_ProjectVision.md), [03_SystemArchitecture.md](file:///d:/projects/laravel_projects/college_project/Conversations/03_SystemArchitecture.md), [04_Pipeline.md](file:///d:/projects/laravel_projects/college_project/Conversations/04_Pipeline.md)

---

## 1. Executive Overview & System Philosophy

### 1.1 System Identity & Architectural Paradigm Shift
The **Knowledge Intelligence Engine (KIE)** is the central knowledge infrastructure of the platform. The platform is **not** a traditional chatbot, a raw PDF vector search engine, or a simple NotebookLM clone. It is an **Educational Knowledge Infrastructure**.

While traditional Retrieval-Augmented Generation (RAG) models treat vector search as the primary source of truth, KIE establishes structured, fine-grained **Knowledge Assets** and **Knowledge Fragments** as first-class, immutable domain entities. Vector retrieval is categorized as **one pluggable strategy** among many inside a larger, multi-layered Knowledge Architecture.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE OPERATING SYSTEM (KOS) VISION                            │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            PLUGIN-BASED SERVICES LAYER                            │  │
│  │   [Grounded Chat] [Study Guide] [Flashcards] [Quiz Gen] [Visual Scenes] [Podcast]  │  │
│  └─────────────────────────────────────────┬─────────────────────────────────────────┘  │
│                                            │ Consumes                                   │
│                                            ▼                                            │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                        KNOWLEDGE INTELLIGENCE ENGINE (KIE)                        │  │
│  │                                                                                   │  │
│  │  ┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐  │  │
│  │  │  Query Understanding   │ │  Retrieval Planner     │ │ Context Optimizer      │  │  │
│  │  └────────────────────────┘ └────────────────────────┘ └────────────────────────┘  │  │
│  │  ┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐  │  │
│  │  │  Prompt Construction   │ │    Citation Engine     │ │   Confidence Engine    │  │  │
│  │  └────────────────────────┘ └────────────────────────┘ └────────────────────────┘  │  │
│  │                                         │                                         │  │
│  │                                         ▼                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                         CANONICAL KNOWLEDGE LAYER                           │  │  │
│  │  │  [Knowledge Assets] ──► [Explicit Relationships] ──► [Knowledge Fragments]   │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────▲─────────────────────────────────────────┘  │
└────────────────────────────────────────────┼────────────────────────────────────────────┘
                                             │ Generated & Governed
                                             │
┌────────────────────────────────────────────┴────────────────────────────────────────────┐
│                  AI INGESTION & PROCESSING PIPELINE (Stages 1 through 7D)               │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Architectural Tenets
* **KIE-TENET-1 (Asset-Fragment Separation):** Knowledge Assets represent canonical logical concepts, while Knowledge Fragments represent the underlying retrieval and embedding units.
* **KIE-TENET-2 (Derived Knowledge Graphs):** The Knowledge Graph MUST be dynamically derived from explicit, typed Knowledge Asset relationships (`DependsOn`, `Explains`, `References`, etc.), rather than acting as a static primary store.
* **KIE-TENET-3 (Pluggable Retrieval Strategies):** Retrieval engines MUST implement a unified strategy interface (`RetrievalStrategyInterface`). The Knowledge Retrieval Planner dynamically selects strategies based on query intent.
* **KIE-TENET-4 (Zero-Hallucination Policy Grounding):** Responses MUST be backed by a standalone **Citation Engine** and verified against policy-driven confidence bands, outputting a complete **Evidence Package** for every execution.
* **KIE-TENET-5 (Strict Immutability & Provenance):** Student state, session memory, and prompt templates MUST remain strictly isolated from canonical Knowledge Assets and Fragments.

---

## 2. Knowledge Hierarchy & Fragment Layer

The KIE establishes a 7-level structural hierarchy for educational content.

```
Document (PDF Source)
   └── Chapter
        └── Lesson
             └── Section
                  └── Knowledge Asset (Logical Concept Entity)
                       └── Knowledge Fragment (Retrieval & Embedding Unit)
                            └── Dense Embedding Vector
```

### 2.1 Distinction Between Assets and Fragments
* **Knowledge Asset:** The canonical, human-understandable educational entity (e.g., a specific Definition, Formula, Law, or Egyptian Arabic Analogy). It holds pedagogical metadata, full version histories, quality scores, and explicit relationships.
* **Knowledge Fragment:** The atomic chunk of text (100–300 tokens) derived from a Knowledge Asset or Section boundary, optimized specifically for dense vector embedding and sparse BM25 indexing. A single Knowledge Asset MAY span multiple Knowledge Fragments.

### 2.2 Knowledge Fragment JSON Schema
Every Knowledge Fragment written to disk (`knowledge_fragments.json`) MUST comply with schema contract `KF-SCHEMA-1`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "KnowledgeFragment",
  "type": "object",
  "required": [
    "fragment_id",
    "asset_id",
    "material_id",
    "chunk_index",
    "token_count",
    "content_text",
    "provenance",
    "embedding_checksum"
  ],
  "properties": {
    "fragment_id": { "type": "string", "format": "uuid" },
    "asset_id": { "type": "string", "format": "uuid" },
    "material_id": { "type": "string" },
    "chunk_index": { "type": "integer" },
    "token_count": { "type": "integer" },
    "content_text": { "type": "string" },
    "context_prefix": { "type": "string" },
    "provenance": {
      "type": "object",
      "required": ["source_pdf_uuid", "page_number", "char_start", "char_end"],
      "properties": {
        "source_pdf_uuid": { "type": "string" },
        "page_number": { "type": "integer" },
        "char_start": { "type": "integer" },
        "char_end": { "type": "integer" }
      }
    },
    "embedding_checksum": { "type": "string" }
  }
}
```

---

## 3. First-Class Knowledge Assets & Typed Relationships

### 3.1 Typed Knowledge Asset Relationships
Knowledge Assets are interconnected via explicit, typed directional relationships. The system Knowledge Graph is constructed dynamically by traversing these relationships.

```
                  ┌───────────────────────────────┐
                  │   Core Principle / Law [LAW]  │
                  └───────────────┬───────────────┘
                                  │
                       Relationship: Explains
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │  Concept Definition [DEF]     │
                  └───────────────┬───────────────┘
                                  │
                       Relationship: UsesFormula
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ Formula & Equation [EQN]      │
                  └───────────────────────────────┘
```

#### Approved Relationship Types:
* `DependsOn`: Target asset MUST be understood before source asset.
* `Explains`: Source asset provides explanatory text for target asset.
* `References`: Source asset explicitly cites target asset.
* `UsesFormula`: Source asset utilizes target mathematical equation (`EQN`).
* `Generalizes`: Source asset is a broader abstraction of target asset.
* `Specializes`: Source asset is a specific instance/case of target asset.
* `AlternativeExplanation`: Source asset provides a secondary view (e.g. Egyptian Arabic analogy `ALG_EG`).
* `SameConcept`: Source and target represent identical concepts in different chapters.
* `Prerequisite`: Foundational prerequisite knowledge.
* `Successor`: Logical next step in curriculum progression.
* `RelatedTo`: Symmetric associative link.

### 3.2 Canonical Knowledge Asset Schema (with Version History & Quality Score)
Every Knowledge Asset MUST validate against `KA-SCHEMA-2`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "KnowledgeAssetV2",
  "type": "object",
  "required": [
    "asset_id",
    "material_id",
    "asset_type",
    "title",
    "content_primary",
    "relationships",
    "quality_score",
    "version_history",
    "provenance",
    "lifecycle_state"
  ],
  "properties": {
    "asset_id": { "type": "string", "format": "uuid" },
    "material_id": { "type": "string" },
    "asset_type": { "type": "string" },
    "title": { "type": "string" },
    "content_primary": { "type": "string" },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["target_asset_id", "relationship_type"],
        "properties": {
          "target_asset_id": { "type": "string", "format": "uuid" },
          "relationship_type": { 
            "type": "string", 
            "enum": ["DependsOn", "Explains", "References", "UsesFormula", "Generalizes", "Specializes", "AlternativeExplanation", "SameConcept", "Prerequisite", "Successor", "RelatedTo"] 
          },
          "weight": { "type": "number", "default": 1.0 }
        }
      }
    },
    "quality_score": {
      "type": "object",
      "required": ["overall_score", "completeness", "provenance_quality", "readability", "retrieval_quality"],
      "properties": {
        "overall_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "completeness": { "type": "number" },
        "provenance_quality": { "type": "number" },
        "readability": { "type": "number" },
        "retrieval_quality": { "type": "number" },
        "embedding_quality": { "type": "number" }
      }
    },
    "version_history": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["version", "author", "timestamp", "approval_status", "change_reason"],
        "properties": {
          "version": { "type": "integer" },
          "author": { "type": "string" },
          "timestamp": { "type": "string" },
          "approval_status": { "type": "string" },
          "change_reason": { "type": "string" },
          "diff_summary": { "type": "string" }
        }
      }
    },
    "provenance": { "type": "object" },
    "lifecycle_state": { 
      "type": "string", 
      "enum": ["RAW", "EXTRACTED", "REVISED", "REJECTED", "VALIDATED", "APPROVED", "PUBLISHED", "ARCHIVED", "DEPRECATED", "ROLLED_BACK"] 
    }
  }
}
```

### 3.3 Expanded HIL Workflow & Lifecycle Paths
The Human-in-the-Loop (HIL) workflow supports complete revision, rejection, and rollback loops:

```
[ RAW ] ──► ( Stage 7B ) ──► [ EXTRACTED ]
                                  │
                        ┌─────────┴─────────┐
                        ▼                   ▼
                  [ REJECTED ]        [ VALIDATED ]
                        │                   │
                        ▼                   ▼
                [ REPROCESSING ]   [ HIL Node Review ]
                        │                   │
                        └─────────┬─────────┘
                                  ▼
                            [ APPROVED ] ──► [ PUBLISHED ] ──► [ ROLLED_BACK ]
```

---

## 4. AI Pipeline Integration: Knowledge Processing Phase

In [04_Pipeline.md](file:///d:/projects/laravel_projects/college_project/Conversations/04_Pipeline.md), Stage 7 is expanded into a 4-stage **Knowledge Processing Phase**:

```
Stage 6: Structure Mapping
              │
              ▼
STAGE 7A: Relationship Extraction & Graph Derivation (`knowledge_relationships`)
              │ Outputs: relationships.json, knowledge_graph.json
              ▼
STAGE 7B: Asset & Fragment Decomposition (`knowledge_assets`)
              │ Outputs: knowledge_assets.json, knowledge_fragments.json
              ▼
STAGE 7C: Hybrid Indexing & Registries Build (`knowledge_index`)
              │ Outputs: vector_index.bin, bm25_index.json, index_registry.json
              ▼
STAGE 7D: Asynchronous Background Queue Dispatch (`background_dispatch`)
              │ Triggers: Background Workers for async synthesis & pre-caching
              ▼
Stage 8: Question Extraction ──► Stage 9: Section Rewrite (KIE-Augmented)
```

---

## 5. Registries & Resource Subsystems

### 5.1 Embedding Registry Schema
Every generated vector embedding batch MUST be registered in `embedding_registry.json` (`REG-EMB-1`):

```json
{
  "registry_id": "emb_reg_98f4a12c",
  "material_id": "mat_eng_101",
  "embedding_model": "text-embedding-3-large",
  "dimensions": 1536,
  "normalization_method": "L2",
  "creation_timestamp": "2026-07-22T09:50:00Z",
  "checksum": "sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "compatibility_version": "v2.0"
}
```

### 5.2 Index Registry Schema
All active and historical search indices MUST be registered in `index_registry.json` (`REG-IDX-1`):

```json
{
  "index_id": "idx_vec_001",
  "material_id": "mat_eng_101",
  "index_type": "DENSE_VECTOR_HNSW",
  "total_entries": 420,
  "index_status": "ACTIVE",
  "created_at_stage": "Stage 7C",
  "generator_metadata": { "algorithm": "HNSW", "ef_construction": 200, "M": 16 },
  "associated_embedding_registry_id": "emb_reg_98f4a12c"
}
```

### 5.3 Cost & Resource Tracking Subsystem
The KIE tracks operational token expenditure and resource costs across all operations:

```json
{
  "tracking_id": "cost_run_8819a",
  "material_id": "mat_eng_101",
  "embedding_cost_usd": 0.042,
  "retrieval_cost_usd": 0.008,
  "reranking_cost_usd": 0.015,
  "generation_cost_usd": 0.120,
  "storage_bytes": 1428500,
  "per_user_consumption": {
    "user_101": { "query_count": 14, "tokens_consumed": 18200 }
  }
}
```

---

## 6. Query Understanding & Knowledge Retrieval Planner

The **Knowledge Retrieval Planner** dynamically formulates retrieval strategies based on query intent.

```
                           [ User Input Query ]
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │   Query Understanding   │
                        └────────────┬────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE RETRIEVAL PLANNER & PLUGINS                             │
│                                                                                        │
│   Planner Strategy Interface: RetrievalStrategyInterface                               │
│                                                                                        │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│   │ DenseStrategy    │  │ BM25Strategy     │  │ GraphStrategy    │  │ VisualEngine │   │
│   └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘   │
│            │                     │                     │                   │           │
│            └─────────────────────┼─────────────────────┴───────────────────┘           │
│                                  │                                                     │
│                                  ▼                                                     │
│                     ┌──────────────────────────┐                                       │
│                     │ Planner Decision Log     │                                       │
│                     └────────────┬─────────────┘                                       │
└──────────────────────────────────┼─────────────────────────────────────────────────────┘
                                   │
                                   ▼
                      [ Context Optimization Layer ]
```

### 6.1 Pluggable Strategy Interface (`RetrievalStrategyInterface`)
All retrieval engines MUST implement the `RetrievalStrategyInterface` (`RSI-1`):

```python
class RetrievalStrategyInterface(ABC):
    @abstractmethod
    def execute_search(
        self, 
        query_text: str, 
        intent: QueryIntent, 
        top_k: int, 
        filters: Dict[str, Any]
    ) -> List[RetrievalCandidate]:
        """Executes targeted search and returns candidate Knowledge Fragments/Assets."""
        pass
```

### 6.2 Planner Decision Log
Every query execution generates a **Planner Decision Log** entry (`PDL-1`):

```json
{
  "log_id": "pdl_771a2c",
  "query_text": "What is Newton's Second Law and how is it used in impulse calculations?",
  "detected_intent": "INTENT_CALC",
  "selected_strategies": ["DenseStrategy", "BM25Strategy", "GraphStrategy"],
  "rejected_strategies": ["VisualEngine", "SQLStrategy"],
  "rationale": "INTENT_CALC requires exact LaTeX formula match (BM25) combined with concept definition (Dense) and prerequisite graph links (Graph).",
  "execution_timestamp": "2026-07-22T09:51:00Z"
}
```

---

## 7. Context Optimization & Prompt Construction Layer

The **Prompt Construction Layer** assembles final prompts from versioned templates, policies, and optimized context blocks.

```
[ Optimized Fragments ] ──► [ Prompt Construction Layer ] ◄── [ Versioned Prompt Templates ]
                                     │
                                     ▼
                             [ Final LLM Prompt ]
```

### 7.1 Prompt Templates as First-Class Versioned Artifacts
Every downstream service uses a versioned Prompt Template (`PT-SCHEMA-1`):

```json
{
  "template_id": "tmpl_quiz_gen_v3",
  "service_name": "QuizGeneratorService",
  "version": 3,
  "system_instruction": "You are an expert assessment writer. Generate multiple-choice questions strictly grounded in the provided Knowledge Assets.",
  "output_schema_json": { "type": "object", "properties": { "questions": { "type": "array" } } },
  "required_asset_types": ["DEF", "EQN", "ERR"]
}
```

---

## 8. Citation Engine & Evidence Package Specification

### 8.1 Independent Citation Engine
The **Citation Engine** operates independently of the LLM generator. It scans output text, detects factual claims, matches claims to source `KnowledgeFragment` offsets, and renders verified citations.

### 8.2 Evidence Package Output Schema
For every generated response, the system MUST emit a complete **Evidence Package** payload (`EVIDENCE-PKG-1`):

```json
{
  "package_id": "ev_pkg_991823",
  "query_text": "Explain Newton's Second Law",
  "response_text": "Newton's Second Law states that force equals mass times acceleration [Source: Page 12, Offset 450-520].",
  "confidence_band": "VERY_HIGH",
  "confidence_score": 0.94,
  "planner_decision_log_id": "pdl_771a2c",
  "retrieved_asset_ids": ["ast_def_001", "ast_eqn_002"],
  "citation_map": [
    {
      "claim_text": "force equals mass times acceleration",
      "asset_id": "ast_def_001",
      "pdf_uuid": "pdf_phys_101",
      "page_number": 12,
      "char_offset_start": 450,
      "char_offset_end": 520
    }
  ],
  "prompt_template_version": "tmpl_chat_v2",
  "model_version": "gemini-1.5-pro",
  "execution_latency_ms": 780
}
```

---

## 9. Policy-Based Knowledge Confidence Engine

Confidence bands govern safe system fallbacks (`CONF-BAND-1`):

| Confidence Band | Criteria | Action & System Response Behavior |
|---|---|---|
| **VERY HIGH** | RRF Score $\ge 0.85$, $100\%$ citation mapping | Output answer with green verified citations. |
| **HIGH** | RRF Score $0.70 - 0.84$, complete asset coverage | Output standard grounded answer with inline citations. |
| **MEDIUM** | RRF Score $0.50 - 0.69$, partial asset coverage | Output answer with explicit caution disclaimer. |
| **LOW** | RRF Score $0.35 - 0.49$, weak semantic match | Refuse direct answer; offer related lesson links. |
| **UNSUPPORTED** | RRF Score $< 0.35$, zero matching assets | **Explicit Abstention:** *"Topic not covered in course materials."* |

---

## 10. Educational Personalization & Conversational Memory Layer

Student state and conversation memory MUST remain isolated from static, canonical Knowledge Assets and Fragments (`PERS-ISO-1`).

```
┌───────────────────────────────────────┐     ┌───────────────────────────────────────┐
│     CANONICAL KNOWLEDGE LAYER         │     │     STUDENT PERSONALIZATION LAYER     │
│  (Shared, Immutable, Versioned)       │     │  (Tenant & Session Isolated State)    │
│  • Knowledge Assets & Fragments       │     │  • Session Memory & Conversation      │
│  • Explicit Asset Relationships       │     │  • Student Mastery & Weak Concepts    │
└───────────────────────────────────────┘     └───────────────────────────────────────┘
```

---

## 11. Plugin-Based Knowledge Services Framework

Downstream capabilities are implemented as modular service plugins consuming KIE Knowledge Assets via a standard interface (`KIEPluginInterface`).

```
                               ┌───────────────────────────────────┐
                               │     KIE PLUGIN EXTENSION CORE     │
                               └─────────────────┬─────────────────┘
                                                 │
      ┌──────────────────┬───────────────────────┼───────────────────────┬──────────────────┐
      ▼                  ▼                       ▼                       ▼                  ▼
[ChatPlugin]     [StudyGuidePlugin]     [FlashcardPlugin]         [QuizPlugin]        [PodcastPlugin]
```

---

## 12. Multi-Layer Caching Architecture

The KIE enforces a 6-tier caching hierarchy to maximize throughput and minimize API costs:

```
[ Session Cache ] ──► [ Response Cache ] ──► [ Citation Cache ] ──► [ Prompt Cache ] ──► [ Retrieval Cache ] ──► [ Embedding Cache ]
```

1. **Embedding Cache:** Stores computed vector embeddings keyed by `sha256(content_text)`.
2. **Retrieval Cache:** Caches candidate fragment lists keyed by `sha256(query_text + intent)`.
3. **Prompt Cache:** Caches assembled prompt strings prior to LLM submission.
4. **Citation Cache:** Caches verified claim-to-offset provenance mappings.
5. **Response Cache:** Stores full Evidence Packages for identical queries.
6. **Session Cache:** Manages transient user conversation history in Redis.

---

## 13. Asynchronous Background Workers Subsystem

Long-running generation and indexing tasks are handled by asynchronous Laravel Queue workers:

* **EmbeddingWorker:** Computes dense vector embeddings in batches during Stage 7C.
* **IndexingWorker:** Builds HNSW and BM25 search indices asynchronously.
* **ValidationWorker:** Runs Stage 10 coverage and grounding checks.
* **PodcastWorker:** Synthesizes two-host audio overview scripts.
* **FlashcardWorker:** Pre-generates spaced repetition flashcard decks upon material publication.

---

## 14. Retrieval Analytics & Knowledge Coverage Metrics

### 14.1 Metrics & Quality Scoring
* **Knowledge Coverage Score ($KCS$):** Measures percentage of source PDF text converted into active Knowledge Assets:
  $$KCS = \frac{\text{Total Characters in Knowledge Assets}}{\text{Total Characters in Source PDF}} \times 100$$
* **Asset Quality Score ($AQS$):** Evaluated per Knowledge Asset:
  $$AQS = 0.3(Completeness) + 0.3(Provenance) + 0.2(Readability) + 0.2(Retrieval)$$

---

## 15. Non-Functional Requirements & Enterprise SLAs

* **KIE-NFR-1 (Planner Latency):** Retrieval Planner decision execution MUST complete within **< 150ms**.
* **KIE-NFR-2 (Retrieval Latency):** Multi-strategy search MUST complete within **< 500ms** at $P_{95}$.
* **KIE-NFR-3 (Total End-to-End SLA):** Total KIE context delivery to service plugins MUST NOT exceed **800ms**.
* **KIE-NFR-4 (Multi-Tenant Isolation):** All indices, registries, and assets MUST remain strictly isolated within `Generating/Materials/[material_name]/`.

---

## 16. Requirement Traceability Matrix

| Requirement ID | Summary Description | Responsible Layer | Verification Method |
|---|---|---|---|
| `KIE-001` | Hierarchy MUST follow Doc $\rightarrow$ Asset $\rightarrow$ Fragment. | Section 2 | Schema Audit |
| `KIE-002` | Explicit typed relationships MUST be defined for Assets. | Section 3 | Schema Audit |
| `KIE-003` | Asset version history MUST include author, timestamp, diff. | Section 3 | Version Test |
| `KIE-004` | Retrieval Orchestrator renamed to Knowledge Retrieval Planner. | Section 6 | Code Inspection |
| `KIE-005` | Pluggable strategies MUST implement `RetrievalStrategyInterface`. | Section 6 | Interface Check |
| `KIE-006` | Prompt Construction Layer MUST build prompts from versioned templates. | Section 7 | Prompt Audit |
| `KIE-007` | Citation Engine MUST operate as an independent subsystem. | Section 8 | Subsystem Test |
| `KIE-008` | Evidence Package MUST be emitted for every response. | Section 8 | JSON Schema Test |
| `KIE-009` | Planner Decision Log MUST record strategy selection rationale. | Section 6 | Log Audit |
| `KIE-010` | Registries MUST track embeddings and search indices. | Section 5 | Registry Check |
| `KIE-011` | Multi-layer Caching MUST enforce 6 caching tiers. | Section 12 | Cache Test |
| `KIE-012` | Background Workers MUST handle async embedding/indexing jobs. | Section 13 | Queue Test |
| `KIE-013` | Downstream services MUST use plugin architecture. | Section 11 | Plugin Audit |

---

## 17. Architectural Decision Records (ADR)

### ADR 007: Separation of Knowledge Assets and Knowledge Fragments
* **Status:** Approved
* **Context:** Embedding models require fixed chunk sizes (100–300 tokens), while human learning requires complete conceptual definitions (which may span 1,000+ tokens).
* **Decision:** Decouple logical Knowledge Assets from physical Knowledge Fragments. Embed Fragments, but present Assets.
* **Consequences:** Ensures search precision without sacrificing pedagogical context.

### ADR 008: Explicit Asset Relationships over Static Knowledge Graphs
* **Status:** Approved
* **Context:** Hardcoding a static Knowledge Graph limits graph evolution and cross-course concept linking.
* **Decision:** Store directional, typed relationships (`DependsOn`, `Explains`, etc.) directly on Knowledge Assets. Derive the Knowledge Graph dynamically.
* **Consequences:** Makes knowledge graph updates atomic and incremental.

---

## 18. Strategic Vision: Pathway to Knowledge Operating System (KOS)

The **Knowledge Intelligence Engine (KIE)** represents the core intelligence subsystem of the platform's long-term product vision: the **Knowledge Operating System (KOS)**.

While the current implementation remains named KIE, every architectural layer—from decoupled Knowledge Fragments and explicit relationships to pluggable retrieval strategies, versioned prompt templates, and independent citation engines—is designed to ensure a seamless migration path toward a complete Knowledge Operating System in future major versions.

---

## 19. System Glossary

* **Knowledge Asset:** Canonical, human-understandable educational entity (Definition, Formula, Law).
* **Knowledge Fragment:** Atomic text chunk (100–300 tokens) derived from an Asset for embedding and retrieval.
* **Knowledge Retrieval Planner:** Dynamic component selecting search strategies based on query intent.
* **Evidence Package:** Complete JSON audit payload emitted with every generated response.
* **Planner Decision Log:** Record documenting why specific retrieval strategies were chosen or rejected.
* **Knowledge Operating System (KOS):** The future long-term architectural vision encompassing KIE, agentic workflows, and cross-course intelligence.
