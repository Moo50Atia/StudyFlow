import pytest
from pydantic import ValidationError
from Generating.Indexing.schema import IndexEntry, KnowledgeIndex

def test_metadata_completeness():
    # We should have all required 15 fields
    entry = IndexEntry(
        entry_id="test-1",
        chunk_id="chunk-1",
        chunk_hash="hash",
        text="Sample text",
        start_page=1,
        end_page=1,
        char_count=11,
        token_estimate=2,
        embedding=[0.1, 0.2, 0.3],
        metadata={
            "semantic_path": "Lecture 1 > Intro",
            "lecture_id": "L1",
            "lecture_title": "Intro",
            "chapter_id": "C1",
            "section_id": "S1",
            "subsection_id": "SS1",
            "heading": "Intro",
            "language": "en",
            "created_at": "2026-07-10T00:00:00Z",
            "previous_chunk": None,
            "next_chunk": "chunk-2",
            "contains_images": False,
            "contains_tables": False,
            "contains_code": False,
            "contains_math": False
        }
    )
    
    required_fields = [
        "semantic_path", "lecture_id", "lecture_title",
        "chapter_id", "section_id", "subsection_id", "heading",
        "language", "created_at", "previous_chunk", "next_chunk",
        "contains_images", "contains_tables", "contains_code", "contains_math"
    ]
    
    for field in required_fields:
        assert hasattr(entry.metadata, field), f"Missing required metadata field: {field}"

def test_query_filtering():
    def make_meta(l_id, path):
        return {
            "semantic_path": path,
            "lecture_id": l_id,
            "lecture_title": "T",
            "chapter_id": "C",
            "section_id": "S",
            "subsection_id": "SS",
            "heading": "H",
            "language": "en",
            "created_at": "2026-07-10T00:00:00Z",
            "previous_chunk": None,
            "next_chunk": None,
            "contains_images": False,
            "contains_tables": False,
            "contains_code": False,
            "contains_math": False
        }

    entries = [
        IndexEntry(
            entry_id="test-1", chunk_id="c1", text="t1",
            metadata=make_meta("L1", "path1")
        ),
        IndexEntry(
            entry_id="test-2", chunk_id="c2", text="t2",
            metadata=make_meta("L1", "path2")
        ),
        IndexEntry(
            entry_id="test-3", chunk_id="c3", text="t3",
            metadata=make_meta("L2", "path3")
        ),
    ]
    
    index = KnowledgeIndex(
        index_id="idx-1",
        document_id="doc-1",
        source_file="test.pdf",
        embedding_model="test-model",
        created_at="2026-07-10T00:00:00Z",
        entries=entries
    )
    
    # Filter by lecture_id
    l1_entries = [e for e in index.entries if e.metadata.lecture_id == "L1"]
    assert len(l1_entries) == 2
    assert all(e.metadata.lecture_id == "L1" for e in l1_entries)
