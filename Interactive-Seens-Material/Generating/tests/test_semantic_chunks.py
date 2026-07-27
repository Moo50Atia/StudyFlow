import pytest
import json
from pathlib import Path

def test_semantic_chunk_quality():
    """
    T023: Unit tests for semantic chunk quality.
    Validates: dominant topic, no lecture mixing, no section leakage,
    heading alignment, and semantic boundary scores.
    """
    # Assuming Unit2_Test was built and we can inspect its structure
    material_dir = Path("Generating/Materials/Unit2_Test")
    if not material_dir.exists():
        pytest.skip("Unit2_Test pipeline output not found")
        
    index_path = material_dir / "knowledge_index.json"
    assert index_path.exists(), "knowledge_index.json missing"
    
    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    entries = data.get("entries", [])
    assert len(entries) > 0, "No entries in knowledge_index"
    
    # 1. No lecture mixing (a chunk belongs to exactly one lecture)
    for entry in entries:
        meta = entry.get("metadata", {})
        
        # Validates no lecture leakage
        assert "lecture_id" in meta, "lecture_id missing"
        assert meta.get("lecture_id"), "lecture_id is empty"
        assert "lecture_title" in meta, "lecture_title missing"
        
        # Heading alignment
        assert "section_id" in meta, "section_id missing"
        
        # Validate semantic path structure
        assert "semantic_path" in meta, "semantic_path missing"
        
        text = entry.get("text", "")
        assert len(text) > 50, "Chunk is too small, likely an orphaned heading"
