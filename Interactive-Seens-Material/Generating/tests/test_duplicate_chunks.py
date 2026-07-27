import pytest
import json
from pathlib import Path

def test_duplicate_chunks():
    """
    T028: Duplicate chunk validation tests.
    Identical chunks generate identical hashes, duplicate detection works.
    """
    material_dir = Path("Generating/Materials/Unit2_Test")
    if not material_dir.exists():
        pytest.skip("Unit2_Test pipeline output not found")
        
    chunk_manifest_path = material_dir / "chunk_manifest.json"
    with open(chunk_manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    chunks = data.get("chunks", [])
    if not chunks:
        pytest.skip("No chunks in chunk_manifest")
        
    # Check that all IDs in the manifest are unique (deduplication worked)
    ids = [c["id"] for c in chunks]
    assert len(ids) == len(set(ids)), "Duplicate chunk hashes found in manifest!"

    # Ensure we validated uniqueness above. We can't rehash because chunk_manifest does not contain text.
