# Research & Architectural Decisions: Knowledge Intelligence Engine (KIE)

**Feature:** Knowledge Intelligence Engine (KIE)  
**Spec Directory:** [specs/001-knowledge-intelligence-engine/](file:///d:/projects/laravel_projects/college_project/specs/001-knowledge-intelligence-engine/)

---

## 1. Research Topics & Resolution Summary

### Research Topic 1: Asset-Fragment Decoupling & Storage Strategy
* **Decision:** Decouple logical Knowledge Assets (canonical educational concepts, definitions, formulas, analogies) from physical Knowledge Fragments (100–300 token text chunks optimized for vector embeddings).
* **Rationale:** Embedding models perform best on dense 100–300 token windows, whereas educational comprehension requires complete multi-paragraph explanations. Decoupling ensures precision retrieval while maintaining complete pedagogical context.
* **Alternatives Evaluated:** Single monolithic chunking (rejected due to retrieval noise) and dynamic windowing without fragment boundaries (rejected due to non-deterministic vector index alignment).

### Research Topic 2: Explicit Asset Relationships vs. Static Knowledge Graph
* **Decision:** Store directional, typed relationships (`DependsOn`, `Explains`, `References`, `UsesFormula`, `Generalizes`, `Specializes`, `AlternativeExplanation`, etc.) directly on Knowledge Assets. Derive the Knowledge Graph dynamically.
* **Rationale:** Allows atomic, incremental updates to individual Knowledge Assets without re-generating an entire monolithic graph structure.
* **Alternatives Evaluated:** Hardcoded graph adjacency matrix (rejected due to brittleness during incremental HIL edits).

### Research Topic 3: Pluggable Strategy Architecture for Retrieval
* **Decision:** Enforce `RetrievalStrategyInterface` across all search strategies (Dense, BM25, GraphRAG, Metadata, Visual, Temporal).
* **Rationale:** Decouples search execution from the Knowledge Retrieval Planner, enabling new retrieval models (e.g. SQL, Hybrid Sparse-Dense, Cross-Encoder Re-Ranker) to be plugged in seamlessly without altering core logic.
* **Alternatives Evaluated:** Hardcoded hybrid search routine (rejected due to extensibility limits).

### Research Topic 4: Policy-Based Confidence Engine & Safe Abstention
* **Decision:** Enforce 5 strict policy confidence bands (`VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW`, `UNSUPPORTED`).
* **Rationale:** Raw floating-point cosine similarity cutoffs vary across domains and embedding models. Policy-driven bands provide deterministic system response behaviors and safe abstention when content is out of scope.
* **Alternatives Evaluated:** Static cosine threshold (e.g., score $< 0.70$) (rejected due to inconsistent false-positive rates).
