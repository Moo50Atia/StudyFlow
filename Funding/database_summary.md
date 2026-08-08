# Funding Knowledge Database - Architecture & Technical Summary

## 📌 Executive Overview

The **Funding Knowledge Database** is a production-ready, fully normalized (3NF) relational database built from the `ContentForFunding_Expanded.json` dataset. It is strictly scoped to **Layer 1: Factual Knowledge & Organization Data**, serving as the source-of-truth knowledge layer for funding entities, categories, geographic distributions, application rules, and automated enrichment metadata.

CRM and outreach workflows (such as emails, calls, sales pipelines, tasks, internal notes, and attachments) are strictly excluded from Layer 1 and reserved for the future Layer 2 CRM module.

---

## 🗄️ Database Files & Deliverables

All generated database files reside inside the [`Funding/`](file:///media/moahmmed/01DB65D8A02C22F0/projects/laravel_projects/college_project/Funding) directory:

* **[`Funding/Funding.sqlite`](file:///media/moahmmed/01DB65D8A02C22F0/projects/laravel_projects/college_project/Funding/Funding.sqlite)** — Operational SQLite database file containing 261 normalized entities and 1,970+ relational child records.
* **[`Funding/schema.sql`](file:///media/moahmmed/01DB65D8A02C22F0/projects/laravel_projects/college_project/Funding/schema.sql)** — Production-ready SQL DDL script defining tables, foreign keys, constraints, and indexes.
* **[`Funding/import_json.py`](file:///media/moahmmed/01DB65D8A02C22F0/projects/laravel_projects/college_project/Funding/import_json.py)** — Automated Python ETL importer script with data cleansing, deduplication, and verification validation routines.
* **[`Funding/database_summary.md`](file:///media/moahmmed/01DB65D8A02C22F0/projects/laravel_projects/college_project/Funding/database_summary.md)** — Architectural summary and documentation.

---

## 📊 Database Record Metrics & Parity Report

| Table Name | Entity Scope / Type | Record Count | Description |
| :--- | :--- | :---: | :--- |
| **`categories`** | Lookup | **18** | 18 funding categories (Universities, Venture Capital, Government, Accelerators, etc.) |
| **`countries`** | Lookup / Geography | **25** | Unique normalized countries (Egypt, USA, UAE, KSA, UK, etc.) |
| **`cities`** | Lookup / Geography | **77** | Unique normalized cities linked to countries |
| **`company_types`** | Lookup / Tags | **17** | Unique company target audience tags (EdTech, AI Startup, DeepTech, Scale-up, etc.) |
| **`funding_entities`** | Core Knowledge | **261** | Primary funding entities and institutions |
| **`government_details`** | 1-to-1 Extension | **21** | Specialized metrics for government entities (amount, acceptance rate, duration, etc.) |
| **`funding_programs`** | Child Records | **58** | Specific funding programs offered by entities |
| **`eligibility_requirements`** | Child Records | **52** | Normalized eligibility criteria items |
| **`required_documents`** | Child Records | **85** | Required application documents |
| **`application_steps`** | Child Records | **192** | Step-by-step application instructions (general, any project, specific project) |
| **`success_stories`** | Child Records | **50** | Past funded project success stories |
| **`entity_company_types`** | Junction Bridge | **641** | Many-to-Many entity tag associations |
| **`entity_contacts`** | Public Knowledge | **0** | Discovered public contacts (initialized, non-CRM) |
| **`entity_sources`** | Provenance Log | **501** | Field-level data provenance and website/email verification audit entries |
| **`entity_versions`** | Audit / Snapshots | **0** | Historical version snapshots (initialized for future updates) |
| **`entity_research_status`**| Enrichment State | **261** | Enrichment lifecycle status tracking per entity (`Completed`) |
| **`entity_enrichment_jobs`**| Agent Queue | **0** | Autonomous AI agent enrichment task queue (initialized) |

---

## 🏗️ Architectural Schema Design

### 1. Core Entity & Classification Tables
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    priority VARCHAR(20) NOT NULL,
    why_reasoning TEXT,
    entity_type VARCHAR(20) NOT NULL
);

CREATE TABLE funding_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_category_id INTEGER NOT NULL,
    country_id INTEGER,
    city_id INTEGER,
    name VARCHAR(255) NOT NULL,
    priority VARCHAR(20) DEFAULT 'Medium',
    official_website VARCHAR(500),
    official_email VARCHAR(255),
    linkedin VARCHAR(500),
    phone VARCHAR(50),
    description TEXT,
    FOREIGN KEY (funding_category_id) REFERENCES categories(id),
    FOREIGN KEY (country_id) REFERENCES countries(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);
```

### 2. Government 1-to-1 Extension Table
```sql
CREATE TABLE government_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL UNIQUE,
    funding_amount VARCHAR(255),
    acceptance_rate VARCHAR(100),
    expected_duration VARCHAR(100),
    last_project_link VARCHAR(500),
    notes TEXT,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);
```

### 3. Data Auditability & AI Agent Enrichment Tables
```sql
CREATE TABLE entity_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    field_value TEXT,
    source_type VARCHAR(50) NOT NULL,
    source_name VARCHAR(150),
    source_url VARCHAR(500),
    confidence_score REAL DEFAULT 1.0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status VARCHAR(30) DEFAULT 'Unverified',
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE entity_research_status (
    funding_entity_id INTEGER PRIMARY KEY,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    last_attempt TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    last_error TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);
```

---

## 🔒 Verification & Quality Assurance

1. **Foreign Key Enforcement**: `PRAGMA foreign_keys = ON;` is enabled. Verification check returned **0 constraint violations**.
2. **Normalized Child Arrays**: No comma-separated strings or JSON blob arrays exist in database rows. All lists are decomposed into 3NF child/junction rows.
3. **Data Preservation**: 100% of entity names, websites, emails, descriptions, eligibility criteria, programs, steps, and success stories from `ContentForFunding_Expanded.json` are preserved.
4. **PostgreSQL & Laravel Compatibility**: Table names, foreign keys, column names, and indices follow standard Eloquent conventions for migration to PostgreSQL/Laravel.
