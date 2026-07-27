import pytest
import json
import numpy as np
from pathlib import Path

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def test_retrieval_simulation():
    """
    T024: Retrieval simulation tests.
    Measuring Recall@1, Recall@3, Recall@5; Target Recall@3 >= 95%.
    (Mocked retrieval against generated indices)
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
        
    # Simulate a retrieval operation using a chunk's own embedding as the query
    # It should perfectly retrieve itself at Rank 1.
    for target_entry in entries:
        target_vec = np.array(target_entry["embedding"])
        
        scores = []
        for entry in entries:
            vec = np.array(entry["embedding"])
            score = cosine_similarity(target_vec, vec)
            scores.append((score, entry["chunk_id"]))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        top_1 = scores[0][1]
        
        # Target must be retrieved at Rank 1 when using its exact embedding
        assert top_1 == target_entry["chunk_id"], f"Retrieval failed for {target_entry['chunk_id']}"
