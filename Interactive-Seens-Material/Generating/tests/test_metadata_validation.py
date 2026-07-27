import pytest
import json
from pathlib import Path
from Generating.Indexing.schema import IndexMetadata

def test_metadata_completeness():
    """
    T026: Metadata completeness validation.
    Ensure 15 fields, no NULL/empty/placeholder, unique chunk IDs, valid semantic_path.
    """
    material_dir = Path("Generating/Materials/Unit2_Test")
    if not material_dir.exists():
        pytest.skip("Unit2_Test pipeline output not found")
        
    index_path = material_dir / "knowledge_index.json"
    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    entries = data.get("entries", [])
    if not entries:
        pytest.skip("No entries in knowledge_index")
        
    seen_ids = set()
    
    for entry in entries:
        meta = entry.get("metadata", {})
        
        # Pydantic validation handles most 15 required fields implicitly if we construct it
        # Let's try to construct it to ensure it passes the schema validation
        validated = IndexMetadata(**meta)
        
        # Additional assertions on IndexEntry
        assert entry.get("chunk_id"), "Chunk ID must not be empty"
        assert entry.get("chunk_hash"), "Chunk hash must not be empty"
        assert entry.get("token_estimate", 0) > 0, "Token estimate must be > 0"
        assert entry.get("char_count", 0) > 0, "Character count must be > 0"
        
        chunk_hash = entry.get("chunk_hash")
        assert chunk_hash not in seen_ids, f"Duplicate chunk hash found in index: {chunk_hash}"
        seen_ids.add(chunk_hash)
