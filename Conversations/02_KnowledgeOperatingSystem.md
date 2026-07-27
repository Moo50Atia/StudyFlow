# 02. Knowledge Operating System (KOS) Architecture Specification

---

> **Document Metadata**  
> **Document Identifier:** `02_KnowledgeOperatingSystem.md`  
> **Layer:** Layer 2/3 (Parent Runtime Architecture Specification)  
> **Version:** 1.0.0  
> **Status:** Official Specification  
> **Authority:** Chief Software Architect & AI Systems Architect  
> **Applies To:** Platform KOS Kernel, Service Runtime, Plugin Runtime, Worker Runtime, KIE Subsystem, Security & Registries  
> **Parent Documents:** [00_DocumentationStandards.md](file:///d:/projects/laravel_projects/college_project/Conversations/00_DocumentationStandards.md), [01_ProjectVision.md](file:///d:/projects/laravel_projects/college_project/Conversations/01_ProjectVision.md)  
> **Child Subsystem Specifications:** [03_SystemArchitecture.md](file:///d:/projects/laravel_projects/college_project/Conversations/03_SystemArchitecture.md), [04_Pipeline.md](file:///d:/projects/laravel_projects/college_project/Conversations/04_Pipeline.md), [21_KnowledgeIntelligenceSpecification.md](file:///d:/projects/laravel_projects/college_project/Conversations/21_KnowledgeIntelligenceSpecification.md)

---

## 1. Executive Overview & KOS Philosophy

### 1.1 System Identity & Paradigm Shift
The **Knowledge Operating System (KOS)** is the master runtime architecture of the platform. It provides an enterprise-grade execution kernel, plugin lifecycle manager, multi-tenant security sandbox, capability registry, resource orchestrator, and event bus.

Under this parent architecture, the **Knowledge Intelligence Engine (KIE)** is **not** the entire platform; it is **one major intelligence subsystem** running natively on top of the KOS kernel.

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                           KNOWLEDGE OPERATING SYSTEM (KOS) KERNEL                         │
│                                                                                           │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │   Service Runtime       │  │    Plugin Runtime       │  │     Worker Runtime       │  │
│  └────────────┬────────────┘  └────────────┬────────────┘  └────────────┬─────────────┘  │
│               │                            │                            │                │
│               ▼                            ▼                            ▼                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              CAPABILITY REGISTRY                                    │  │
│  │  [Grounded Chat] [Study Guide] [Flashcards] [Quiz Gen] [Visual Scene] [Podcast Audio]│  │
│  └─────────────────────────────────────────┬───────────────────────────────────────────┘  │
│                                            │                                              │
│                                            ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    KNOWLEDGE INTELLIGENCE ENGINE (KIE) SUBSYSTEM                    │  │
│  │                                                                                     │  │
│  │  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐  │  │
│  │  │ Search Service Layer   │  │ Execution Planner      │  │ Prompt Optimizer Layer │  │  │
│  │  └────────────────────────┘  └────────────────────────┘  └────────────────────────┘  │  │
│  │  ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐  │  │
│  │  │ Independent Citation   │  │ Policy Confidence      │  │ Evidence Package v1    │  │  │
│  │  └────────────────────────┘  └────────────────────────┘  └────────────────────────┘  │  │
│  └─────────────────────────────────────────┬───────────────────────────────────────────┘  │
│                                            │                                              │
│                                            ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           CANONICAL KNOWLEDGE STORE LAYER                           │  │
│  │  [Assets Store] ──► [Fragments Store] ──► [Relationships Store] ──► [Metadata Store] │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Architectural Tenets
* **KOS-TENET-1 (Subsystem Decoupling):** KIE and all future intelligence modules run as managed subsystems inside KOS. KIE MUST NOT act as the host runtime process.
* **KOS-TENET-2 (Canonical Knowledge Store Authority):** Repositories are abstraction APIs. The **Knowledge Store Layer** is the sole canonical source of truth for assets, fragments, metadata, and versioning.
* **KOS-TENET-3 (Dynamic Capability Discovery):** Educational capabilities (Flashcards, Quiz, Podcast, Grounded Chat) are registered in the **Capability Registry** independently from plugins.
* **KOS-TENET-4 (Full Lifecycle Governance):** All plugins and background workers MUST obey strict lifecycle states (`Install`, `Load`, `Enable`, `Disable`, `Upgrade`, `Unload`, `Health Check`).
* **KOS-TENET-5 (Complete Execution Traceability):** Every request generates an end-to-end **Execution Trace** payload tracking lifecycle events from initial query parsing to final Evidence Package rendering.

---

## 2. KOS Runtime Architecture

### 2.1 Runtime Components
1. **Service Runtime:** Manages synchronous REST/LTI requests, dependency injection bindings, and middleware security checks.
2. **Plugin Runtime:** Isolates and executes 3rd-party and native educational plugins inside secure execution sandboxes.
3. **Worker Runtime:** Manages asynchronous background workers (`EmbeddingWorker`, `IndexWorker`, `ValidationWorker`, `AnalyticsWorker`, `PodcastWorker`, `FlashcardWorker`, `SceneWorker`, `CleanupWorker`).
4. **Lifecycle Manager:** Controls system startup, grace shutdowns, health checks, and subsystem dependency initialization.

---

## 3. Plugin Lifecycle & Capability Registry

### 3.1 Plugin Lifecycle Protocol
Every plugin loaded by KOS MUST implement standard lifecycle hooks (`KOS-PLUGIN-LIFE-1`):

```
 [ INSTALL ] ──► [ LOAD ] ──► [ ENABLE ] ──► [ HEALTH CHECK: OK ]
                                  │
                   ┌──────────────┼──────────────┐
                   ▼              ▼              ▼
              [ DISABLE ]    [ UPGRADE ]     [ UNLOAD ]
```

* `Install()`: Validates plugin manifest, dependencies, and security signatures.
* `Load()`: Allocates memory sandboxes and binds plugin interfaces.
* `Enable()`: Registers plugin capabilities with the central **Capability Registry**.
* `Disable()`: Temporarily unregisters capabilities without clearing memory.
* `Upgrade()`: Hot-swaps plugin binary/bytecode while preserving session state.
* `Unload()`: Flushes plugin caches and frees allocated resources.
* `HealthCheck()`: Returns health status (`HEALTHY`, `DEGRADED`, `CRITICAL`).

### 3.2 Capability Registry Schema
Educational capabilities register independently of plugin code (`CAP-REG-1`):

```json
{
  "capability_id": "cap_flashcards_v2",
  "capability_name": "Spaced Repetition Flashcards",
  "providing_plugin_id": "plugin_learning_suite",
  "status": "ENABLED",
  "required_asset_types": ["DEF", "ACR", "EQN"],
  "health_status": "HEALTHY"
}
```

---

## 4. Multi-Tenant Security & Resource Isolation

### 4.1 Security Layer Components
* **Tenant Isolation:** Enforces material-level and organization-level data boundaries. Cross-tenant data bleed is strictly prohibited at the store level.
* **Permission Engine:** RBAC and ABAC checks verifying user capabilities before invoking services.
* **Secret Management:** Vault-backed API key and credential encryption.
* **Audit Logger:** Encrypted, append-only security logs recording all privileged store mutations.

---

## 5. Canonical Knowledge Store vs. Repository Abstraction

Repositories MUST NOT act as canonical data owners. The **Knowledge Store Layer** is the master source of truth.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              REPOSITORIES ABSTRACTION API                              │
│   [AssetRepository] [FragmentRepository] [RelationshipRepository] [IndexRepository]   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Delegation & Caching
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              CANONICAL KNOWLEDGE STORE                                │
│   • Assets Store        • Fragments Store        • Relationships Store                 │
│   • Metadata Store      • Versions Store         • Attachments & Embeddings Store      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Search Service Layer & Intelligent Planner Execution

The **Search Service Layer** wraps retrieval operations, exposing clean request/response models while hiding internal planner complexity.

```
[ User Request ] ──► [ Search Service (SearchRequest) ] ──► [ Search Session & Context ]
                                                                     │
                                                                     ▼
                                                        [ Intelligent Planner ]
                                                         (Cost & Latency Estimator)
                                                                     │
                                                                     ▼
                                                        [ Search Pipeline Execution ]
                                                                     │
                                                                     ▼
                                                        [ SearchResponse Output ]
```

* **SearchRequest / SearchResponse:** Clean API DTOs containing search terms, user filters, and output payloads.
* **Intelligent Planner:** Estimates token cost, latency budgets, and constructs dynamic execution graphs before dispatching retrievers.

---

## 7. Prompt System, Citation Subsystem & Evidence Package v1

### 7.1 Prompt Optimization Pipeline
Prompts pass through a 5-tier pipeline: `Prompt Registry` $\rightarrow$ `Prompt Compiler` $\rightarrow$ `Prompt Optimizer` $\rightarrow$ `Prompt Cache` $\rightarrow$ `Prompt Executor`.

### 7.2 Independent Citation Subsystem
Divided into 6 single-responsibility components:
1. `ClaimDetector`: Extracts factual assertions from LLM output.
2. `EvidenceMatcher`: Scans retrieved Knowledge Fragments for semantic matches.
3. `OffsetMapper`: Maps claims back to exact PDF character offsets (`char_start`, `char_end`).
4. `CitationFormatter`: Formats citations into target syntax (`[Source: Page X]`).
5. `CitationRenderer`: Renders visual highlights and UI quote overlays.
6. `CitationValidator`: Verifies citation accuracy prior to release.

### 7.3 Evidence Package v1 Schema (`EV-PKG-V1`)
All generated outputs return a versioned Evidence Package (`EV-PKG-V1`):

```json
{
  "evidence_package_version": "v1.0",
  "package_id": "ev_pkg_88102a",
  "query_text": "Explain Newton's Second Law",
  "response_text": "Newton's Second Law states F=ma...",
  "confidence_band": "VERY_HIGH",
  "confidence_score": 0.96,
  "planner_decision_log_id": "pdl_9921",
  "retrieved_asset_ids": ["ast_def_001"],
  "citation_map": [],
  "execution_latency_ms": 620
}
```

---

## 8. Multi-Registry Architecture (8 Independent Registries)

KOS enforces 8 dedicated, single-responsibility registries:

1. **Embedding Registry:** Tracks vector embedding models, dimensions, and checksums.
2. **Index Registry:** Tracks HNSW vector, BM25, and graph search indices.
3. **Model Registry:** Manages LLM model versions, context windows, and pricing.
4. **Tokenizer Registry:** Manages tokenizers and encoding schemes.
5. **Prompt Registry:** Stores versioned prompt templates (`PT-SCHEMA-1`).
6. **Plugin Registry:** Tracks installed plugin manifests and security keys.
7. **Worker Registry:** Manages active background worker instances and health states.
8. **Capability Registry:** Discovers and registers educational platform capabilities.

---

## 9. End-to-End Execution Trace & Enterprise Benchmark Subsystem

### 9.1 Complete Execution Trace
Every request generates a full exportable `ExecutionTrace` payload (`TRACE-V1`):

```
Query ──► Planner ──► Retrievers ──► Fusion ──► Context Opt ──► Prompt Compile ──► LLM Gen ──► Citation ──► Verification ──► Evidence Package
```

### 9.2 Enterprise Benchmark Subsystem
* **Golden Queries Dataset:** Curated set of standard academic questions with known ground-truth citations.
* **Benchmark Engine:** Runs automated regression tests measuring Retrieval Recall, Precision@K, Prompt Compile Speed, Citation Accuracy, and End-to-End Latency.

---

## 10. Developer Tooling & CLI Suite

KOS includes developer tooling for system debugging:

* **KOS CLI (`kos-cli`):** Terminal command-line tool for managing plugins, running benchmarks, and inspecting registries.
* **Debug Console:** Web-based interactive portal for inspecting active sessions.
* **Index Inspector:** Tool for inspecting HNSW vector indices and BM25 token frequencies.
* **Knowledge Explorer:** Visualizer for Knowledge Assets and relationship edges.
* **Registry Viewer:** Real-time dashboard displaying registry states.

---

## 11. Backward Compatibility & Architectural Inheritance Matrix

The introduction of **KOS** as Layer 2/3 architecture **preserves 100% backward compatibility** with all existing lower-level specifications:

| Specification Document | Parent Architecture | Relationship & Compatibility Rule |
|---|---|---|
| [03_SystemArchitecture.md](file:///d:/projects/laravel_projects/college_project/Conversations/03_SystemArchitecture.md) | `02_KnowledgeOperatingSystem.md` | Inherits KOS Kernel runtime & stateless worker pool guidelines. |
| [04_Pipeline.md](file:///d:/projects/laravel_projects/college_project/Conversations/04_Pipeline.md) | `02_KnowledgeOperatingSystem.md` | Stages 7A-7D execute inside KOS Worker Runtime. |
| [21_KnowledgeIntelligenceSpecification.md](file:///d:/projects/laravel_projects/college_project/Conversations/21_KnowledgeIntelligenceSpecification.md) | `02_KnowledgeOperatingSystem.md` | KIE runs as a managed Subsystem inside KOS Kernel. |

---

## 12. System Glossary

* **Knowledge Operating System (KOS):** The master runtime architecture managing plugins, security, capabilities, workers, and subsystems.
* **Capability Registry:** Central registry for dynamic discovery of educational features (Flashcards, Podcast, Quiz).
* **Execution Trace:** Complete telemetry log recording the end-to-end lifecycle of a query.
* **Knowledge Store:** Canonical storage layer holding assets, fragments, relationships, and metadata.
* **Evidence Package v1:** Schema-versioned payload returned with generated responses containing audit metadata and citations.
