import pytest
from Generating.Chunking.chunk_manager import ChunkManager

def test_code_block_not_split():
    # A block that is just big enough to normally be split, but shouldn't because it's a code block
    manager = ChunkManager(target_size=100, overlap=10)
    
    text = "Here is some code:\n```python\n"
    text += "def very_long_function():\n"
    for i in range(20):
        text += f"    print('This is line {i}')\n"
    text += "```\n"
    text += "End of code."
    
    manifest = manager.chunk_text(text)
    chunks = manifest.chunks
    
    # We should ensure that the entire code block is in ONE chunk, even if it exceeds target_size
    code_in_chunks = []
    for chunk in chunks:
        chunk_text = manager.get_chunk_text(text, chunk)
        if "```python" in chunk_text:
            assert chunk_text.count("```") == 2, "Code block was split across chunks!"

def test_math_block_not_split():
    manager = ChunkManager(target_size=50, overlap=10)
    
    text = "Here is math:\n$$\n"
    text += "f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}\n"
    text += "g(x) = x^2 + 2x + 1\n"
    text += "$$\n"
    text += "End of math."
    
    manifest = manager.chunk_text(text)
    
    for chunk in manifest.chunks:
        chunk_text = manager.get_chunk_text(text, chunk)
        if "$$" in chunk_text:
            # The entire block should be present
            assert chunk_text.count("$$") == 2, "Math block was split!"

def test_table_not_split():
    manager = ChunkManager(target_size=100, overlap=10)
    
    text = "Here is a table:\n"
    text += "| Header 1 | Header 2 |\n"
    text += "|----------|----------|\n"
    for i in range(10):
        text += f"| Row {i} | Data {i} |\n"
    text += "End of table."
    
    manifest = manager.chunk_text(text)
    
    # Tables are identified by consecutive lines starting with `|`
    # We ensure that if a chunk has table rows, it shouldn't just cut the table in half unless it's huge,
    # but the requirement says never split tables.
    table_lines_in_chunks = []
    for chunk in manifest.chunks:
        chunk_text = manager.get_chunk_text(text, chunk)
        table_lines = [line for line in chunk_text.split('\n') if line.strip().startswith('|')]
        table_lines_in_chunks.append(len(table_lines))
    
    # The table has 12 lines. They should all be in the same chunk (so one chunk has 12, others have 0)
    assert any(count == 12 for count in table_lines_in_chunks), "Table was split across chunks!"

