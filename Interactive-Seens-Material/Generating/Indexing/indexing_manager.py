"""
Indexing Manager — Builds a backend-agnostic knowledge index.

Reads vectors.json and resolves chunk text from chunk_manifest.json +
extracted_text.txt. Constructs a self-contained KnowledgeIndex object.

Persistence is a separate concern — save_index() currently writes local
JSON but can be replaced with Qdrant, SQLite, DuckDB, Milvus, Pinecone,
etc. without modifying the build logic.

This stage does NOT implement retrieval, similarity search, or RAG.
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from Generating.Indexing.schema import IndexEntry, KnowledgeIndex
from Generating.config import INDEXING_BACKEND

logger = logging.getLogger(__name__)


class IndexingManager:
    """
    Builds a knowledge index from embedding vectors.

    The manager is responsible for:
        1. Building the KnowledgeIndex object (business logic)
        2. Persisting it (save_index — replaceable backend)

    Usage:
        manager = IndexingManager()
        index = manager.build_index(vector_data, chunk_manifest_data, full_text)
        manager.save_index(index, output_dir)
    """

    def __init__(
        self,
        backend: Optional[str] = None,
    ):
        self.backend = backend or INDEXING_BACKEND

    def build_index(
        self,
        vector_manifest_data: dict,
        chunk_manifest_data: dict,
        full_text: str,
        structure_data: Optional[dict] = None,
    ) -> KnowledgeIndex:
        """
        Build a knowledge index by combining vectors with chunk text.

        Args:
            vector_manifest_data: Parsed vectors.json dict.
            chunk_manifest_data: Parsed chunk_manifest.json dict.
            full_text: The full extracted text (for resolving chunk text).
            structure_data: Optional parsed structure.json dict for semantic enrichment.

        Returns:
            KnowledgeIndex with self-contained entries.
        """
        vectors = vector_manifest_data.get("vectors", [])
        source_file = vector_manifest_data.get("source_file", "unknown")
        document_id = vector_manifest_data.get("document_id", "")
        embedding_model = vector_manifest_data.get("embedding_model", "")
        vector_dimension = vector_manifest_data.get("vector_dimension", 0)

        # Create a lookup for chunks from chunk_manifest_data
        chunks_map = {c.get("id"): c for c in chunk_manifest_data.get("chunks", [])}

        logger.info(
            f"Building knowledge index: {len(vectors)} vectors, "
            f"backend: {self.backend}"
        )

        entries: list[IndexEntry] = []
        for i, vector in enumerate(vectors):
            chunk_id = vector.get("chunk_id", "")
            chunk_info = chunks_map.get(chunk_id, {})
            
            # Resolve chunk text from offsets
            start = vector.get("start_char_offset", 0)
            end = vector.get("end_char_offset", 0)
            chunk_text = full_text[start:end]
            
            start_page = vector.get("start_page", 0)
            
            # Enrich from structure data
            lecture_id = ""
            lecture_title = ""
            chapter_id = ""
            section_id = ""
            subsection_id = ""
            semantic_path = ""
            
            if structure_data:
                lecture_id = structure_data.get("material", "Unknown")
                for ch in structure_data.get("chapters", []):
                    for mc in ch.get("mini_chapters", []):
                        for les in mc.get("lessons", []):
                            if les.get("page_start", 0) <= start_page <= les.get("page_end", 9999):
                                chapter_id = ch.get("id", "")
                                section_id = mc.get("id", "")
                                subsection_id = les.get("id", "")
                                lecture_title = les.get("title", "")
                                semantic_path = f"{ch.get('title', '')} > {mc.get('title', '')} > {les.get('title', '')}"
                                break
                        if subsection_id: break
                    if chapter_id: break

            prev_chunk_id = vectors[i-1].get("chunk_id") if i > 0 else None
            next_chunk_id = vectors[i+1].get("chunk_id") if i < len(vectors) - 1 else None

            # Some basic heading extraction
            heading = ""
            lines = chunk_text.strip().split("\n")
            if lines and lines[0].startswith("#"):
                heading = lines[0].lstrip("#").strip()

            meta = {
                "semantic_path": semantic_path,
                "lecture_id": lecture_id,
                "lecture_title": lecture_title,
                "chapter_id": chapter_id,
                "section_id": section_id,
                "subsection_id": subsection_id,
                "heading": heading,
                "language": "en",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "previous_chunk": prev_chunk_id,
                "next_chunk": next_chunk_id,
                "contains_images": chunk_info.get("contains_images", False),
                "contains_tables": chunk_info.get("contains_tables", False),
                "contains_code": chunk_info.get("contains_code", False),
                "contains_math": chunk_info.get("contains_math", False),
            }

            from Generating.Indexing.schema import IndexMetadata
            
            entry = IndexEntry(
                entry_id=f"idx_{i+1:04d}",
                chunk_id=chunk_id,
                chunk_hash=vector.get("chunk_hash", ""),
                text=chunk_text,
                start_page=start_page,
                end_page=vector.get("end_page", 0),
                char_count=vector.get("char_count", 0),
                token_estimate=vector.get("token_estimate", 0),
                embedding=vector.get("embedding", []),
                metadata=IndexMetadata(**meta),
            )
            entries.append(entry)

        index = KnowledgeIndex(
            index_id=uuid.uuid4().hex,
            document_id=document_id,
            schema_version="1.0.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            source_file=source_file,
            total_entries=len(entries),
            embedding_model=embedding_model,
            vector_dimension=vector_dimension,
            backend=self.backend,
            entries=entries,
        )

        logger.info(
            f"Knowledge index built: {index.total_entries} entries, "
            f"backend: {self.backend}"
        )

        return index

    def save_index(self, index: KnowledgeIndex, output_dir: str) -> None:
        """
        Persist the knowledge index.

        Current backend: local_json (writes knowledge_index.json).
        Future backends (Qdrant, SQLite, etc.) can override this method
        or be dispatched based on self.backend.
        """
        if self.backend == "local_json":
            self._save_local_json(index, output_dir)
        else:
            raise ValueError(
                f"Unsupported indexing backend: '{self.backend}'. "
                f"Available: local_json"
            )

    def _save_local_json(
        self, index: KnowledgeIndex, output_dir: str
    ) -> None:
        """Persist index as a local JSON file."""
        output_path = Path(output_dir) / "knowledge_index.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index.model_dump(), f, indent=2, ensure_ascii=False)
        logger.info(f"Saved knowledge index: {output_path}")

    def load_index(self, output_dir: str) -> KnowledgeIndex:
        """Load knowledge index from JSON."""
        index_path = Path(output_dir) / "knowledge_index.json"
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return KnowledgeIndex.model_validate(data)
