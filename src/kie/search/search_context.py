"""
KIE Search Service Layer DTOs and Pipeline
===========================================
Defines SearchRequest, SearchContext, SearchSession, and SearchResponse.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import uuid
import time


class SearchRequest(BaseModel):
    query_text: str
    material_id: str
    user_id: Optional[str] = None
    role: str = "student"
    top_k: int = 5


class SearchContext(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    intent: Optional[str] = None
    selected_strategies: List[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    request_id: str
    query_text: str
    response_text: str
    confidence_band: str
    confidence_score: float
    evidence_package: Dict[str, Any]
    latency_ms: int
