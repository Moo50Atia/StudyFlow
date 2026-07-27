"""
Generating Pipeline — Universal Educational Content Generation System.

A scalable, JSON-first pipeline for transforming arbitrary educational PDFs
into structured, interactive learning materials with Dynamic View support.

Pipeline Stages:
    1. PDF Intake + Text Extraction
    2. OCR Detection & Processing
    3. Text Chunking
    4. Vectorization (Chunk → Embedding)
    5. Knowledge Index Construction
    6. Route Detection (AI-based domain classification)
    7. Structure Extraction (Chapter → Mini Chapter → Lesson)
    8. Knowledge Graph Construction
    9. Question Extraction & Mapping
   10. Educational Section Generation
   11. Validation (Coverage + Visualization Readiness)
   12. Dynamic View Mapping
   13. Dynamic View Prompt Generation
   14. Manifest Update
"""

__version__ = "2.0.0"
__author__ = "StudyFlow"
