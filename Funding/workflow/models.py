"""
models.py
Data models and dataclasses for the Funding Enrichment Workflow.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class FundingEntityItem:
    id: int
    category_id: int
    category_name: str
    name: str
    priority: str
    country: Optional[str] = None
    city: Optional[str] = None
    official_website: Optional[str] = None
    official_email: Optional[str] = None
    linkedin: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    entity_type: str = "standard"

@dataclass
class SourceRecord:
    field_name: str
    field_value: Any
    source_type: str = "Official Website"
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    confidence_score: float = 1.0
    verification_status: str = "Verified"

@dataclass
class ContactRecord:
    name: str
    position: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    phone: Optional[str] = None
    confidence_score: float = 1.0
    source_url: Optional[str] = None

@dataclass
class EnrichmentResult:
    entity_id: int
    raw_output: str
    parsed_json: Optional[Dict[str, Any]] = None
    success: bool = False
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    execution_time_seconds: float = 0.0

@dataclass
class ValidationResult:
    is_valid: bool
    cleaned_data: Dict[str, Any] = field(default_factory=dict)
    sources: List[SourceRecord] = field(default_factory=list)
    contacts: List[ContactRecord] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
