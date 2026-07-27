"""
Vectorization Manager — Generates embeddings for document chunks.

Reads chunk_manifest.json, loads chunk text from extracted_text.txt,
generates an embedding for each chunk via a pluggable EmbeddingProvider,
and persists vectors.json with references (not duplicated text).

This stage does NOT implement retrieval, search, or RAG.
"""

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from Generating.Vectorization.providers.base_provider import EmbeddingProvider
from Generating.Vectorization.schema import ChunkVector, VectorManifest

logger = logging.getLogger(__name__)


def _get_provider(provider_name: str, **kwargs) -> EmbeddingProvider:
    """
    Factory function to instantiate an EmbeddingProvider by name.

    Args:
        provider_name: One of 'gemini', etc.
        **kwargs: Passed to the provider constructor.

    Returns:
        An EmbeddingProvider instance.

    Raises:
        ValueError: If the provider name is not recognized.
    """
    if provider_name == "gemini":
        from Generating.Vectorization.providers.gemini_provider import (
            GeminiProvider,
        )
        return GeminiProvider(**kwargs)
    else:
        raise ValueError(
            f"Unknown embedding provider: '{provider_name}'. "
            f"Available: gemini"
        )


class VectorizationManager:
    """
    Converts text chunks into embedding vectors.

    Usage:
        manager = VectorizationManager(provider)
        manifest = manager.vectorize(chunk_manifest_data, full_text)
        manager.save_vectors(manifest, output_dir)
    """

    def __init__(self, provider: EmbeddingProvider):
        """
        Args:
            provider: An EmbeddingProvider implementation.
        """
        self.provider = provider

    def vectorize(
        self,
        chunk_manifest_data: dict,
        full_text: str,
        document_id: Optional[str] = None,
    ) -> VectorManifest:
        """
        Generate embeddings for every chunk.

        Args:
            chunk_manifest_data: Parsed chunk_manifest.json dict.
            full_text: The full extracted text (for slicing chunk content).
            document_id: Optional stable document UUID. Generated if not provided.

        Returns:
            VectorManifest with all chunk vectors (text not duplicated).
        """
        chunks = chunk_manifest_data.get("chunks", [])
        source_file = chunk_manifest_data.get("source_file", "unknown")
        total_pages = chunk_manifest_data.get("total_pages", 0)
        total_characters = chunk_manifest_data.get("total_characters", 0)
        doc_id = document_id or uuid.uuid4().hex

        logger.info(
            f"Vectorizing {len(chunks)} chunks with provider: "
            f"{self.provider.model_name} (dim={self.provider.dimension})"
        )

        vectors: list[ChunkVector] = []
        for i, chunk in enumerate(chunks):
            start = chunk.get("start_char_offset", 0)
            end = chunk.get("end_char_offset", 0)
            chunk_text = full_text[start:end]

            if not chunk_text.strip():
                logger.warning(f"  Chunk {chunk.get('id', i)}: empty text, skipping")
                continue

            # Content hash for future incremental indexing
            chunk_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()

            embedding = self.provider.embed(chunk_text)

            vectors.append(ChunkVector(
                chunk_id=chunk.get("id", f"chunk_{i+1:03d}"),
                chunk_hash=chunk_hash,
                start_page=chunk.get("start_page", 0),
                end_page=chunk.get("end_page", 0),
                char_count=chunk.get("char_count", len(chunk_text)),
                token_estimate=chunk.get("token_estimate", 0),
                start_char_offset=start,
                end_char_offset=end,
                embedding=embedding,
            ))

            logger.info(
                f"  {chunk.get('id', i)}: "
                f"{len(chunk_text)} chars → {len(embedding)}-dim vector"
            )

        manifest = VectorManifest(
            document_id=doc_id,
            schema_version="1.0.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            source_file=source_file,
            total_vectors=len(vectors),
            embedding_model=self.provider.model_name,
            embedding_provider=type(self.provider).__name__,
            vector_dimension=self.provider.dimension,
            total_characters=total_characters,
            total_pages=total_pages,
            vectors=vectors,
        )

        logger.info(
            f"Vectorization complete: {manifest.total_vectors} vectors, "
            f"model={self.provider.model_name}, dim={self.provider.dimension}"
        )

        return manifest

    def save_vectors(self, manifest: VectorManifest, output_dir: str) -> None:
        """Save vector manifest to JSON."""
        output_path = Path(output_dir) / "vectors.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(), f, indent=2, ensure_ascii=False)
        logger.info(f"Saved vectors: {output_path}")

    def load_vectors(self, output_dir: str) -> VectorManifest:
        """Load vector manifest from JSON."""
        vectors_path = Path(output_dir) / "vectors.json"
        with open(vectors_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VectorManifest.model_validate(data)
