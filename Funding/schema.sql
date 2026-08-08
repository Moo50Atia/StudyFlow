-- ==============================================================================
-- Funding Knowledge Database Schema (Layer 1 Scope)
-- File: Funding/schema.sql
-- Compatible with SQLite 3+, MySQL 8+, and PostgreSQL 12+
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. LOOKUP & CLASSIFICATION TABLES
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    priority VARCHAR(20) NOT NULL CHECK(priority IN ('Critical', 'High', 'Medium', 'Low', 'N/A')),
    why_reasoning TEXT,
    entity_type VARCHAR(20) NOT NULL CHECK(entity_type IN ('standard', 'government')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    code_iso2 VARCHAR(2),
    code_iso3 VARCHAR(3),
    continent VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE,
    UNIQUE(country_id, name)
);

CREATE TABLE IF NOT EXISTS company_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS funding_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS technology_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS startup_stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 2. CENTRAL ENTITY & EXTENSION TABLES
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS funding_entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_category_id INTEGER NOT NULL,
    country_id INTEGER,
    city_id INTEGER,
    name VARCHAR(255) NOT NULL,
    priority VARCHAR(20) DEFAULT 'Medium' CHECK(priority IN ('Critical', 'High', 'Medium', 'Low', 'N/A')),
    official_website VARCHAR(500),
    official_email VARCHAR(255),
    linkedin VARCHAR(500),
    phone VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE SET NULL,
    FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE SET NULL,
    UNIQUE(name, funding_category_id)
);

CREATE TABLE IF NOT EXISTS government_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL UNIQUE,
    funding_amount VARCHAR(255),
    acceptance_rate VARCHAR(100),
    expected_duration VARCHAR(100),
    last_project_link VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 3. NORMALIZED CHILD DETAIL TABLES
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS funding_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    program_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS eligibility_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    criterion TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS required_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    document_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS application_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    step_type VARCHAR(30) NOT NULL CHECK(step_type IN ('general_process', 'any_project', 'this_project')),
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS success_stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    story_description TEXT NOT NULL,
    link VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 4. MANY-TO-MANY JUNCTION BRIDGES
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS entity_company_types (
    funding_entity_id INTEGER NOT NULL,
    company_type_id INTEGER NOT NULL,
    PRIMARY KEY (funding_entity_id, company_type_id),
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE,
    FOREIGN KEY (company_type_id) REFERENCES company_types(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_technology_domains (
    funding_entity_id INTEGER NOT NULL,
    technology_domain_id INTEGER NOT NULL,
    PRIMARY KEY (funding_entity_id, technology_domain_id),
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE,
    FOREIGN KEY (technology_domain_id) REFERENCES technology_domains(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_startup_stages (
    funding_entity_id INTEGER NOT NULL,
    startup_stage_id INTEGER NOT NULL,
    PRIMARY KEY (funding_entity_id, startup_stage_id),
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE,
    FOREIGN KEY (startup_stage_id) REFERENCES startup_stages(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 5. PUBLIC KNOWLEDGE CONTACTS (NON-CRM)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS entity_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(150),
    email VARCHAR(255),
    linkedin VARCHAR(500),
    phone VARCHAR(50),
    confidence_score REAL DEFAULT 1.0,
    source_url VARCHAR(500),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 6. AUDITABILITY, VERSIONING & AI AGENT ENRICHMENT
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS entity_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    field_value TEXT,
    source_type VARCHAR(50) NOT NULL CHECK(source_type IN ('Official Website', 'Government Portal', 'AI Extraction', 'Manual Entry', 'Public Registry')),
    source_name VARCHAR(150),
    source_url VARCHAR(500),
    confidence_score REAL DEFAULT 1.0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP,
    verification_status VARCHAR(30) DEFAULT 'Unverified' CHECK(verification_status IN ('Unverified', 'Verified', 'Disputed', 'Deprecated')),
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    change_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT 'system',
    snapshot_json TEXT NOT NULL,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_research_status (
    funding_entity_id INTEGER PRIMARY KEY,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Running', 'Completed', 'Verified', 'Needs Human Review', 'Failed', 'Archived')),
    last_attempt TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    last_error TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entity_enrichment_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funding_entity_id INTEGER NOT NULL,
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Running', 'Completed', 'Failed')),
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    attempt_count INTEGER DEFAULT 0,
    error_message TEXT,
    FOREIGN KEY (funding_entity_id) REFERENCES funding_entities(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 7. PERFORMANCE INDEXES
-- ------------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_entities_category ON funding_entities(funding_category_id);
CREATE INDEX IF NOT EXISTS idx_entities_country ON funding_entities(country_id);
CREATE INDEX IF NOT EXISTS idx_entities_priority ON funding_entities(priority);
CREATE INDEX IF NOT EXISTS idx_entities_name ON funding_entities(name);
CREATE INDEX IF NOT EXISTS idx_cities_country ON cities(country_id);
CREATE INDEX IF NOT EXISTS idx_steps_entity ON application_steps(funding_entity_id, step_type);
CREATE INDEX IF NOT EXISTS idx_programs_entity ON funding_programs(funding_entity_id);
CREATE INDEX IF NOT EXISTS idx_sources_entity ON entity_sources(funding_entity_id, field_name);
CREATE INDEX IF NOT EXISTS idx_jobs_entity_status ON entity_enrichment_jobs(funding_entity_id, status);
