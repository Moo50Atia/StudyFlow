import pytest
from Generating.Chunking.chunk_manager import ChunkManager

def test_chunk_size_and_tokens(sample_markdown_document):
    # Test with very small target to force multiple chunks
    manager = ChunkManager(target_size=200, overlap=50, chars_per_token=4.0)
    
    # We will override min/max/limit for the test to see if it respects bounds
    manager.min_tokens = 20
    manager.max_tokens = 50
    manager.hard_limit_tokens = 60
    
    manifest = manager.chunk_text(sample_markdown_document)
    
    assert len(manifest.chunks) > 1, "Should create multiple chunks"
    
    for chunk in manifest.chunks:
        # It shouldn't exceed hard limit in any circumstance unless a single unbreakable block is larger
        token_estimate = chunk.token_estimate
        if not (chunk.contains_code or chunk.contains_math or chunk.contains_tables):
            assert token_estimate <= manager.hard_limit_tokens, f"Chunk exceeded hard limit: {token_estimate} tokens"

def test_chunk_overlap(sample_markdown_document):
    manager = ChunkManager(target_size=200, overlap=50)
    
    manifest = manager.chunk_text(sample_markdown_document)
    chunks = manifest.chunks
    
    for i in range(1, len(chunks)):
        prev_chunk = chunks[i-1]
        curr_chunk = chunks[i]
        
        # Overlap should be exactly equal to overlap size (unless constrained by text start)
        # Actually it's just checking if the start of current chunk is before the end of previous chunk
        overlap_size = prev_chunk.end_char_offset - curr_chunk.start_char_offset
        if not (curr_chunk.contains_code or curr_chunk.contains_math or curr_chunk.contains_tables):
            assert overlap_size > 0, "No overlap between chunks!"
            assert overlap_size <= manager.overlap + 50, f"Overlap too large: {overlap_size}"

def test_heading_heuristic_detection():
    manager = ChunkManager(target_size=100, overlap=20)
    manager.min_tokens = 10
    
    text = "# Main Heading\n"
    text += "Some introductory text here that is fairly long to push the boundary.\n"
    text += "## Section 1\n"
    text += "This is section 1 text.\n"
    text += "## Section 2\n"
    text += "This is section 2 text.\n"
    
    manifest = manager.chunk_text(text)
    
    # We want to ensure that chunks don't start in the middle of a paragraph if there's a heading nearby.
    # We will check if the chunks start exactly at the headings if possible.
    chunk_texts = [manager.get_chunk_text(text, c) for c in manifest.chunks]
    
    # At least one chunk (other than the first) should start with a heading
    starts_with_heading = any(t.lstrip().startswith('#') for t in chunk_texts[1:])
    assert starts_with_heading, "Heuristic failed to align chunk boundary with heading"

