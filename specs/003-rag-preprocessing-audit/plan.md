# Implementation Plan: Enterprise RAG Preprocessing & Knowledge Index Audit

**Branch**: `003-rag-preprocessing-audit`  
**Date**: 2026-07-10  
**Status**: Design Ready  
**Target**: Production-Ready RAG Pipeline

---

# Overview

This feature upgrades the current preprocessing pipeline into an enterprise-grade Retrieval-Augmented Generation (RAG) preprocessing system.

The goal is to maximize retrieval accuracy while maintaining deterministic indexing, semantic integrity, and compatibility with modern vector databases such as:

- Qdrant
- Pinecone
- Weaviate
- ChromaDB
- FAISS
- Milvus

The current implementation performs document extraction, chunking, embedding generation, and indexing. This feature redesigns those stages to produce semantically meaningful chunks enriched with metadata that significantly improves retrieval quality.

---

# Goals

The preprocessing pipeline must:

- Produce semantically meaningful chunks.
- Never split logical content.
- Preserve document hierarchy.
- Produce deterministic chunk hashes.
- Support future hybrid retrieval.
- Support metadata filtering.
- Support image-aware retrieval.
- Support hierarchical navigation.
- Produce production-ready vector metadata.
- Validate preprocessing quality before RAG ingestion.

---

# Technical Context

Language

Python 3.11+

Primary Libraries

- Pydantic v2
- hashlib
- pathlib
- regex
- json

Storage

- chunk_manifest.json
- vectors.json
- knowledge_index.json

Embedding

Gemini Embedding

Current model:
models/gemini-embedding-2
Dimension
768

Target Platform

CLI Pipeline

Future Database

Qdrant

---

# Updated Pipeline

Instead of
Extract

↓

Chunk

↓

Vector

↓

Index


The pipeline becomes


Extract

↓

Semantic Parser

↓

Hierarchy Builder

↓

Chunk Builder

↓

Metadata Enrichment

↓

Keyword Extraction

↓

Image Linking

↓

Vectorization

↓

Knowledge Index

↓

Validation

↓

Manifest


---

# Stage 1

Extraction

Responsibilities

- Extract text
- Extract images
- Preserve page numbers
- Preserve reading order

Output


text.txt

assets/

page metadata


---

# Stage 2

Semantic Parsing

Purpose

Understand document structure before chunking.

Hierarchy


Document

↓

Lecture

↓

Chapter

↓

Section

↓

Subsection

↓

Heading

↓

Paragraph

↓

Sentence


Every block receives a unique ID.

Example


Lecture 4

Section 3

Heading

Inheritance

Paragraph

...


---

# Stage 3

Hierarchy Builder

Creates an internal semantic tree.

Example


Lecture

Section

    Subsection

        Paragraph

            Sentence

No chunking occurs here.

---

# Stage 4

Semantic Chunk Builder

Replace character-based chunking with semantic chunking.

Rules

Never split

- code blocks
- mathematical derivations
- tables
- algorithms
- bullet lists
- figure descriptions
- UML diagrams
- exercises
- definitions

Preferred breakpoints

1 Heading

2 Paragraph

3 Sentence

Never

Random character count.

---

# Chunk Size

Target


800–1500 tokens


Approximately


2500–5000 characters


Maximum


≈1800 tokens


Never produce


10k character chunks


---

# Overlap

Overlap must preserve context.

Target


300–500 characters


Overlap only between neighboring chunks.

Never duplicate large sections.

---

# Semantic Boundary Rules

Priority

Lecture

↓

Chapter

↓

Section

↓

Heading

↓

Paragraph

↓

Sentence

Only if absolutely necessary may the splitter move to a lower level.

---

# Stage 5

Metadata Enrichment

Each chunk receives rich metadata.

Mandatory Metadata


chunk_id

document_id

document_hash

lecture_id

chapter_id

section_id

subsection_id

heading

page_start

page_end

char_count

token_count

language

embedding_model

embedding_dimension

created_at

chunk_hash

previous_chunk

next_chunk

contains_images

contains_tables

contains_code

contains_math


Optional


difficulty

course

semester

subject

source_file


---

# Stage 6

Keyword Extraction

Generate semantic keywords.

Example


Polymorphism

Inheritance

Constructor

Class

Object

Virtual Function


Purpose

Future Hybrid Search

Metadata Filtering

Semantic Ranking

Recommended Libraries

- YAKE
- KeyBERT
- TF-IDF

---

# Stage 7

Image Linking

Every chunk knows which images belong to it.

Example


chunk_021

images

page_41_fig_2.png

page_41_fig_3.png


Never leave orphan images.

---

# Stage 8

Vectorization

One embedding

↓

One chunk

Rules


1 Chunk

↓

1 Vector


Never


Multiple vectors per chunk


unless future MultiVector mode is enabled.

---

# Stage 9

Knowledge Index

Hierarchy


Document

↓

Lecture

↓

Section

↓

Chunk


Every chunk indexed with metadata.

Future compatible with

- Qdrant Payload
- Pinecone Metadata
- Weaviate Properties

---

# Referential Integrity

Must always satisfy


Chunk

↓

Vector

↓

Index


One-to-One mapping

Validation


No orphan chunk

No orphan vector

No orphan index


---

# Hashing

Hash generated from


normalized_text

metadata

page range


Algorithm


SHA256


Deterministic.

---

# Validation Stage

Run before pipeline completion.

Checks

## Chunk Validation

- No empty chunks
- No duplicate IDs
- No duplicate hashes
- Correct ordering
- Valid page ranges
- Valid token count
- Valid overlap
- Heading preserved

---

## Vector Validation

- One vector per chunk
- Dimension == 768
- No empty embeddings
- No duplicate vectors

---

## Index Validation

- All chunks indexed
- Metadata complete
- No broken references

---

## Image Validation

Every image belongs to exactly one chunk.

No orphan assets.

---

## Metadata Validation

Every metadata field exists.

No placeholder values.

No NULL values.

---

# Chunk Quality Score

Every chunk receives a quality score.

Example


Chunk 17

Quality

96%

Checks

✔ Heading complete

✔ Section complete

✔ No code split

✔ Valid overlap

✔ Images attached

✔ Metadata complete


Chunks below


85%


should generate warnings.

---

# Retrieval Optimization

Each chunk stores


keywords

summary

page range

heading

parent section

neighbor ids


Allows

- semantic search
- metadata filtering
- hybrid retrieval
- reranking

---

# Future Hybrid Search

Metadata prepared for


Vector Search

BM25

Keyword Search


No schema changes required later.

---

# Performance Goals

114-page PDF

Processing


< 60 seconds


Memory


< 2 GB RAM


Embedding

Batch whenever supported.

---

# Output Files

## chunk_manifest.json

Contains

- chunk list
- metadata
- hierarchy
- overlap
- hashes

---

## vectors.json

Contains

- embeddings
- metadata
- hashes
- vector dimensions

---

## knowledge_index.json

Contains

Hierarchical searchable index.

---

# Testing

Unit Tests

- Semantic splitter
- Hash generation
- Metadata generation
- Image mapping
- Validation engine

Integration Tests

- End-to-end pipeline
- Retrieval compatibility
- Index consistency

Regression Tests

Ensure old PDFs continue to work.

---

# Success Criteria

The feature is complete when:

✅ Every chunk respects semantic boundaries.

✅ No code block is split.

✅ No table is split.

✅ No mathematical proof is split.

✅ Chunk size remains within target limits.

✅ Overlap is consistent.

✅ Metadata is complete.

✅ Every chunk owns one vector.

✅ Every vector owns one index entry.

✅ Every image belongs to a chunk.

✅ Hashes are deterministic.

✅ Validation passes without errors.

✅ Output is fully compatible with Qdrant, Pinecone, ChromaDB, Weaviate, Milvus, and FAISS.

---

# Production Readiness Checklist

- Semantic Chunking
- Hierarchical Parsing
- Metadata Enrichment
- Keyword Extraction
- Image Linking
- Deterministic Hashing
- Validation Engine
- Chunk Quality Score
- Hybrid Search Ready
- Qdrant Ready
- FAISS Ready
- Chroma Ready
- Pinecone Ready
- Weaviate Ready
- Enterprise Metadata
- Production Logging
- Referential Integrity
- Future Multi-Vector Support
- Future Re-ranking Support
- Future Agentic RAG Compatibility

---

# Final Architecture


PDF

↓

Extraction

↓

Semantic Parsing

↓

Hierarchy Builder

↓

Semantic Chunking

↓

Metadata Enrichment

↓

Keyword Extraction

↓

Image Linking

↓

Vectorization

↓

Knowledge Index

↓

Validation

↓

Manifest

↓

RAG Database (Qdrant / FAISS / Chroma / Pinecone)

↓

Retriever

↓

Re-ranker (Future)

↓

LLM


---

# Overall Objective

Transform the preprocessing pipeline from a basic document chunker into an enterprise-grade RAG preprocessing engine capable of supporting high-quality retrieval, scalable vector databases, hybrid search, multimodal extensions, and future agentic workflows without requiring schema redesign.