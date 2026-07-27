"""
KOS Embedding and Index Registries
==================================
Manages registration, verification, and metadata schemas for vector embeddings and search indices.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class EmbeddingRegistryEntry(BaseModel):
    registry_id: str
    material_id: str
    embedding_model: str
    dimensions: int
    normalization_method: str = "L2"
    creation_timestamp: float = Field(default_factory=time.time)
    checksum: str
    compatibility_version: str = "v2.0"


class IndexRegistryEntry(BaseModel):
    index_id: str
    material_id: str
    index_type: str  # DENSE_VECTOR_HNSW, SPARSE_BM25, GRAPH_ADJACENCY
    total_entries: int
    index_status: str = "ACTIVE"
    created_at_stage: str = "Stage 7C"
    generator_metadata: Dict[str, Any] = Field(default_factory=dict)
    associated_embedding_registry_id: Optional[str] = None


class EmbeddingRegistry:
    def __init__(self):
        self._entries: Dict[str, EmbeddingRegistryEntry] = {}

    def register(self, entry: EmbeddingRegistryEntry) -> None:
        self._entries[entry.registry_id] = entry

    def get(self, registry_id: str) -> Optional[EmbeddingRegistryEntry]:
        return self._entries.get(registry_id)


class IndexRegistry:
    def __init__(self):
        self._entries: Dict[str, IndexRegistryEntry] = {}

    def register(self, entry: IndexRegistryEntry) -> None:
        self._entries[entry.index_id] = entry

    def get(self, index_id: str) -> Optional[IndexRegistryEntry]:
        return self._entries.get(index_id)
