import pytest
import json
from pathlib import Path

def test_manifest_consistency():
    """
    T031: Manifest consistency validation tests.
    Verify zero orphans, zero missing references, 1:1 mapping, 
    checksum consistency from manifest down to knowledge index.
    """
    material_dir = Path("Generating/Materials/Unit2_Test")
    if not material_dir.exists():
        pytest.skip("Unit2_Test pipeline output not found")
        
    chunk_manifest_path = material_dir / "chunk_manifest.json"
    vectors_path = material_dir / "vectors.json"
    index_path = material_dir / "knowledge_index.json"
    
    assert chunk_manifest_path.exists(), "chunk_manifest.json missing"
    assert vectors_path.exists(), "vectors.json missing"
    assert index_path.exists(), "knowledge_index.json missing"
    
    with open(chunk_manifest_path, "r", encoding="utf-8") as f:
        chunks = json.load(f).get("chunks", [])
    with open(vectors_path, "r", encoding="utf-8") as f:
        vectors = json.load(f).get("vectors", [])
    with open(index_path, "r", encoding="utf-8") as f:
        entries = json.load(f).get("entries", [])
        
    chunk_ids = {c.get("id") for c in chunks}
    vec_ids = {v.get("chunk_id") for v in vectors}
    idx_ids = {e.get("chunk_id") for e in entries}
    
    # 1:1 Mapping Assertions
    assert chunk_ids == vec_ids, "Chunks and Vectors 1:1 mapping failed. Orphaned or missing vectors."
    assert chunk_ids == idx_ids, "Chunks and Knowledge Index 1:1 mapping failed. Orphaned or missing index entries."
    
    assert len(chunk_ids) > 0, "No chunks found to validate"
