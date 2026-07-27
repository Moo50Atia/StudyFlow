"""
KIE Domain Models, Persistence Models, and DTOs
==============================================
Domain models and Data Transfer Objects for Knowledge Assets, Fragments, and Evidence Packages.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import uuid
import time


class KnowledgeAssetDomainModel(BaseModel):
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    material_id: str
    asset_type: str
    title: str
    content_primary: str
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    quality_score: Dict[str, float] = Field(default_factory=dict)
    version_history: List[Dict[str, Any]] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    lifecycle_state: str = "VALIDATED"


class KnowledgeFragmentDomainModel(BaseModel):
    fragment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    material_id: str
    chunk_index: int
    token_count: int
    content_text: str
    context_prefix: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    embedding_checksum: str
