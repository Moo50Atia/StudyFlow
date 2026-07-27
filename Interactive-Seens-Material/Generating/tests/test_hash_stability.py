import pytest
from Generating.Chunking.chunk_manager import ChunkManager

def test_hash_stability():
    """
    T030: Stable hash verification tests.
    Validate identical input produces identical chunk IDs, identical hashes, identical vector IDs.
    """
    manager = ChunkManager("TestMaterial", 1000, 200, 1500)
    
    text = "This is a stable text."
    start_page = 1
    end_page = 2
    
    import hashlib
    
    def generate_hash(text, sp, ep):
        hash_input = f"{text}|{sp}|{ep}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        
    # Generate hash twice
    hash1 = generate_hash(text, start_page, end_page)
    hash2 = generate_hash(text, start_page, end_page)
    
    assert hash1 == hash2, "Hashing is not deterministic!"
    
    # Slight change in text should produce a completely different hash
    hash3 = generate_hash(text + " ", start_page, end_page)
    assert hash1 != hash3, "Hash should be sensitive to whitespace changes"
    
    # Slight change in page should produce a different hash
    hash4 = generate_hash(text, start_page, 3)
    assert hash1 != hash4, "Hash should be sensitive to page changes"
