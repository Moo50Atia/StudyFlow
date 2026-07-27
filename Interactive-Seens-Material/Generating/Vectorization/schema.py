"""
Vector Schema — Pydantic models for vectors.json.

Design decisions:
    - Full chunk text is NOT stored here (it exists in chunk_manifest.json
      + extracted_text.txt). Only references (chunk_id, offsets) are kept.
    - chunk_hash enables future incremental indexing (skip unchanged chunks).
    - Stable identifiers (document_id, schema_version) support evolution.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChunkVector(BaseModel):
    """A single chunk's embedding vector with reference metadata."""
    chunk_id: str = Field(..., description="Original chunk ID from chunk_manifest.json")
    chunk_hash: str = Field(
        ...,
        description="SHA-256 hash of the chunk text content "
                    "(for future incremental re-vectorization)"
    )
    start_page: int = Field(0, description="First page number in this chunk")
    end_page: int = Field(0, description="Last page number in this chunk")
    char_count: int = Field(0, description="Character count of the chunk text")
    token_estimate: int = Field(0, description="Estimated token count")
    start_char_offset: int = Field(0, description="Start character offset in full text")
    end_char_offset: int = Field(0, description="End character offset in full text")
    embedding: list[float] = Field(default_factory=list, description="Embedding vector")


class VectorManifest(BaseModel):
    """Complete vector manifest for a document."""
    document_id: str = Field(
        ..., description="Stable UUID identifying the source document"
    )
    schema_version: str = Field("1.0.0", description="Schema version for evolution")
    created_at: str = Field(..., description="ISO 8601 timestamp of generation")
    source_file: str = Field(..., description="Name of the source file")
    total_vectors: int = Field(0, description="Total number of generated vectors")
    embedding_model: str = Field(..., description="Embedding model used")
    embedding_provider: str = Field(
        ..., description="Provider identifier (gemini, sentence-transformers, etc.)"
    )
    vector_dimension: int = Field(0, description="Dimension of each vector")
    total_characters: int = Field(0, description="Total characters across all chunks")
    total_pages: int = Field(0, description="Total pages in the source document")
    vectors: list[ChunkVector] = Field(default_factory=list)
