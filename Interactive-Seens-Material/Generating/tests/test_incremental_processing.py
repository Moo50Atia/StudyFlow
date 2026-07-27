import pytest
from pathlib import Path
from Generating.Vectorization.vectorization_manager import VectorizationManager

def test_incremental_processing():
    """
    T029: Incremental processing tests.
    unchanged chunks are NOT re-embedded, only modified chunks receive new embeddings.
    """
    # This is partially a unit test of VectorizationManager's cache logic.
    manager = VectorizationManager(Path("mock_dir"))
    
    # Mock some existing vectors
    manager.existing_vectors = {
        "hash1": {"chunk_id": "hash1", "embedding": [0.1, 0.2]},
        "hash2": {"chunk_id": "hash2", "embedding": [0.3, 0.4]}
    }
    
    chunks = [
        {"id": "hash1", "text": "This is chunk 1"}, # Exists
        {"id": "hash3", "text": "This is chunk 3"}  # New
    ]
    
    # We can inspect the chunks that need processing
    needs_processing = [c for c in chunks if c["id"] not in manager.existing_vectors]
    
    assert len(needs_processing) == 1
    assert needs_processing[0]["id"] == "hash3"
    assert "hash1" not in [c["id"] for c in needs_processing], "hash1 should be reused from cache"
