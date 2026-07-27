"""
Index Schema — Pydantic models for knowledge_index.json.

Design decisions:
    - Full text IS stored here (unlike vectors.json) because the index
      is the self-contained, retrieval-ready artifact.
    - Stable identifiers (index_id, document_id) link back to source.
    - metadata dict is extensible for any future backend.
    - Backend field enables future storage migration without schema change.
"""

from pydantic import BaseModel, Field
from typing import Optional


class IndexMetadata(BaseModel):
    """Metadata schema for index entries with required fields."""
    semantic_path: str = Field(..., description="Semantic hierarchy path")
    lecture_id: str = Field(..., description="Lecture ID")
    lecture_title: str = Field(..., description="Lecture title")
    chapter_id: str = Field(..., description="Chapter ID")
    section_id: str = Field(..., description="Section ID")
    subsection_id: str = Field(..., description="Subsection ID")
    heading: str = Field(..., description="Heading associated with this chunk")
    language: str = Field(..., description="Language of chunk")
    created_at: str = Field(..., description="Creation timestamp")
    previous_chunk: Optional[str] = Field(None, description="Previous chunk ID")
    next_chunk: Optional[str] = Field(None, description="Next chunk ID")
    contains_images: bool = Field(False, description="Has images")
    contains_tables: bool = Field(False, description="Has tables")
    contains_code: bool = Field(False, description="Has code")
    contains_math: bool = Field(False, description="Has math")

class IndexEntry(BaseModel):
    """A single indexed entry with its vector, text, and metadata."""
    entry_id: str = Field(..., description="Stable unique entry ID")
    chunk_id: str = Field(..., description="Source chunk ID for traceability")
    chunk_hash: str = Field(
        "", description="SHA-256 hash of chunk text (for change detection)"
    )
    text: str = Field(..., description="Full chunk text (self-contained for retrieval)")
    start_page: int = Field(0, description="First page in this chunk")
    end_page: int = Field(0, description="Last page in this chunk")
    char_count: int = Field(0, description="Character count")
    token_estimate: int = Field(0, description="Estimated token count")
    embedding: list[float] = Field(default_factory=list, description="Embedding vector")
    metadata: IndexMetadata = Field(
        ...,
        description="Extensible metadata payload (backend-agnostic)"
    )


class KnowledgeIndex(BaseModel):
    """
    Backend-agnostic knowledge index.

    Designed so the storage backend can be replaced (Qdrant, Milvus,
    Pinecone, SQLite, DuckDB) without changing the pipeline interface.
    The IndexingManager builds this object; persistence is separate.
    """
    index_id: str = Field(..., description="Stable UUID for this index build")
    document_id: str = Field(
        ..., description="Source document UUID (from vectors.json)"
    )
    schema_version: str = Field("1.0.0", description="Index schema version")
    created_at: str = Field(..., description="ISO 8601 timestamp of index creation")
    source_file: str = Field(..., description="Name of the source file")
    total_entries: int = Field(0, description="Total indexed entries")
    embedding_model: str = Field(..., description="Embedding model used")
    vector_dimension: int = Field(0, description="Dimension of each vector")
    backend: str = Field(
        "local_json",
        description="Storage backend identifier (local_json, qdrant, sqlite, etc.)"
    )
    entries: list[IndexEntry] = Field(default_factory=list)
