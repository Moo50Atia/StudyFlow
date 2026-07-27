import pytest
from Generating.Indexing.schema import KnowledgeIndex
from Generating.Vectorization.schema import VectorManifest
from Generating.Chunking.chunk_schema import ChunkManifest

def test_referential_integrity():
    # Load mock manifests
    chunk_man = ChunkManifest(
        source_file="test.pdf",
        total_chunks=2,
        total_characters=100,
        total_pages=1,
        chunk_target_size=50,
        chunk_overlap=10,
        chunks=[
            {"id": "hash1", "start_page": 1, "end_page": 1, "char_count": 50, "token_estimate": 10, "start_char_offset": 0, "end_char_offset": 50},
            {"id": "hash2", "start_page": 1, "end_page": 1, "char_count": 50, "token_estimate": 10, "start_char_offset": 50, "end_char_offset": 100}
        ]
    )
    
    vec_man = VectorManifest(
        document_id="doc1",
        created_at="2026-07-10T00:00:00Z",
        source_file="test.pdf",
        embedding_model="model",
        embedding_provider="gemini",
        vector_dimension=768,
        total_vectors=2,
        vectors=[
            {"chunk_id": "hash1", "chunk_hash": "hash1", "embedding": [0.1]},
            {"chunk_id": "hash2", "chunk_hash": "hash2", "embedding": [0.2]}
        ]
    )
    
    # Validation: 1:1 mapping
    assert len(chunk_man.chunks) == len(vec_man.vectors)
    chunk_ids = {c.id for c in chunk_man.chunks}
    vec_chunk_ids = {v.chunk_id for v in vec_man.vectors}
    assert chunk_ids == vec_chunk_ids, "Mismatch between chunk IDs and vector chunk IDs"

def test_deterministic_hashing():
    from Generating.Chunking.chunk_manager import ChunkManager
    manager = ChunkManager(target_size=100, overlap=10)
    
    text1 = "This is a test document. It has some text."
    text2 = "This is a test document. It has some text."
    
    man1 = manager.chunk_text(text1)
    man2 = manager.chunk_text(text2)
    
    # Same content should produce identical chunk IDs
    assert man1.chunks[0].id == man2.chunks[0].id
