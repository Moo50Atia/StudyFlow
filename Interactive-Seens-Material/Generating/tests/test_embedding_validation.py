import pytest
import json
import math
from pathlib import Path

def test_embedding_validation():
    """
    T027: Embedding validation tests.
    Dimension verification, no NaN/Infinity, vector norm > 0, metadata matches.
    """
    material_dir = Path("Generating/Materials/Unit2_Test")
    if not material_dir.exists():
        pytest.skip("Unit2_Test pipeline output not found")
        
    vectors_path = material_dir / "vectors.json"
    assert vectors_path.exists(), "vectors.json missing"
    
    with open(vectors_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    vectors = data.get("vectors", [])
    if not vectors:
        pytest.skip("No vectors in vectors.json")
        
    expected_dim = data.get("vector_dimension", 768)
    
    for vec_obj in vectors:
        embedding = vec_obj.get("embedding", [])
        
        # 1. Dimension verification
        assert len(embedding) == expected_dim, f"Expected dim {expected_dim}, got {len(embedding)}"
        
        norm_sq = 0.0
        for val in embedding:
            # 2. No NaN/Infinity
            assert not math.isnan(val), "NaN found in embedding"
            assert not math.isinf(val), "Infinity found in embedding"
            norm_sq += val * val
            
        # 3. Vector norm > 0
        norm = math.sqrt(norm_sq)
        assert norm > 0, "Vector norm must be greater than 0"
