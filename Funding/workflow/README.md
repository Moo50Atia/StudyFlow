# Funding Enrichment Browser-use Framework (Layer 1 Scope)

## 📌 Architecture Overview

The **Funding Enrichment Framework** is a modular, production-ready autonomous research agent framework designed to enrich existing funding entities in **`Funding/Funding.sqlite`**.

### ⚠️ Strict Scope Boundaries
* **Layer 1 Knowledge Enrichment Only**: Focuses strictly on discovering factual web information (official websites, emails, LinkedIn URLs, phone numbers, funding programs, eligibility rules, application steps, and public contact directories).
* **Non-CRM**: Does **NOT** manage emails, meetings, calls, tasks, sales pipelines, or internal user notes.
* **Strict Decoupling**: The Browser-use Agent has **ZERO direct access** to SQLite. Browser-use receives a plain text research prompt, executes browser automation via Playwright/LLM, and returns structured JSON text. The Python Manager owns all database transactions and updates.

---

## 🗂️ Component Directory (`Funding/workflow/`)

```
Funding/workflow/
├── __init__.py           # Package initializer
├── config.py             # Dataclass settings loader (JSON & environment variables)
├── models.py             # Typed dataclasses (FundingEntityItem, SourceRecord, ContactRecord, ValidationResult)
├── utils.py              # Modular logging handlers & URL/Email/Phone/LinkedIn regex validation
├── queue.py              # SQLite queue manager & job state recovery controller
├── browser_prompt.py     # Prompt template loader & placeholder interpolator
├── browser_runner.py     # Browser-use Playwright execution wrapper
├── parser.py             # Safe JSON extractor & markdown fence stripper
├── validator.py          # Strict data quality & confidence score validation engine
├── updater.py            # SQLite transactional updater (appends sources, versions & contacts)
├── manager.py            # Main workflow CLI orchestrator & queue loop controller
├── config.json           # Runtime configuration settings
├── README.md             # Architecture manual
├── prompts/
│   └── browser_prompt.txt # Prompt template with placeholders
├── logs/                 # Isolated log files (manager.log, browser.log, validation.log, update.log)
├── outputs/              # Saved raw JSON agent outputs per entity
└── screenshots/          # Saved browser capture screenshots
```

---

## ⚙️ Configuration & LLM Providers

The framework supports multiple LLM providers via `config.json` or environment variables:

```json
{
  "browser": {
    "headless": true,
    "timeout_seconds": 120,
    "viewport_width": 1280,
    "viewport_height": 800,
    "capture_screenshots": true
  },
  "llm": {
    "provider": "gemini",
    "model_name": "gemini-2.5-flash",
    "temperature": 0.1
  },
  "queue": {
    "max_retries": 3,
    "batch_size": 10,
    "retry_delay_seconds": 5
  }
}
```

---

## 🚀 Running the Workflow Manager

### 1. Test Run (Single Entity Batch)
To run a batch of 5 entities:
```bash
python3 Funding/workflow/manager.py --limit 5
```

### 2. Full Queue Loop
To process all pending entities in `Funding.db`:
```bash
python3 Funding/workflow/manager.py
```

---

## 🔒 Error Handling & Crash Recovery

1. **Automatic Job Recovery**: If power fails or the process is interrupted mid-execution, `QueueManager.reset_crashed_jobs()` automatically resets stuck `'Running'` entities back to `'Pending'` on startup.
2. **Provenance Logging**: All enriched fields are logged into `entity_sources` with a confidence score (`0.0` - `1.0`), source URL, and timestamp.
3. **Snapshot Versioning**: Every successful enrichment updates `entity_versions` with a JSON snapshot of the changes.
