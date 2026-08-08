"""
config.py
Configuration system for the Funding Enrichment Workflow.
Supports loading from environment variables or external config.json.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW_DIR = os.path.join(BASE_DIR, "workflow")

@dataclass
class BrowserConfig:
    headless: bool = False
    max_steps: int = 250
    timeout_seconds: int = 120
    viewport_width: int = 1280
    viewport_height: int = 800
    capture_screenshots: bool = True
    wait_for_network_idle_page_load_time: float = 2.5
    maximum_wait_page_load_time: float = 15.0

@dataclass
class LLMConfig:
    provider: str = "gemini"  # gemini, openai, anthropic, ollama
    model_name: str = "gemini-2.5-flash"
    fallback_model_name: str = "gemini-1.5-pro"
    max_retries: int = 5
    temperature: float = 0.1
    api_key: Optional[str] = None

@dataclass
class RateLimitConfig:
    requests_per_minute: int = 15
    inter_entity_delay_seconds: float = 5.0
    backoff_on_error_seconds: float = 15.0

@dataclass
class QueueConfig:
    max_retries: int = 3
    batch_size: int = 10
    retry_delay_seconds: int = 5

@dataclass
class PathsConfig:
    db_path: str = os.path.join(BASE_DIR, "Funding.db")
    prompt_template_path: str = os.path.join(WORKFLOW_DIR, "prompts", "browser_prompt.txt")
    logs_dir: str = os.path.join(WORKFLOW_DIR, "logs")
    outputs_dir: str = os.path.join(WORKFLOW_DIR, "outputs")
    screenshots_dir: str = os.path.join(WORKFLOW_DIR, "screenshots")

@dataclass
class AppConfig:
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    queue: QueueConfig = field(default_factory=QueueConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)

    @classmethod
    def load_from_json(cls, json_path: str) -> "AppConfig":
        """Load configuration from a JSON file."""
        if not os.path.exists(json_path):
            return cls()

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        b_data = data.get("browser", {})
        l_data = data.get("llm", {})
        q_data = data.get("queue", {})
        p_data = data.get("paths", {})

        r_data = data.get("rate_limit", {})

        browser_cfg = BrowserConfig(
            headless=b_data.get("headless", False),
            max_steps=b_data.get("max_steps", 250),
            timeout_seconds=b_data.get("timeout_seconds", 120),
            viewport_width=b_data.get("viewport_width", 1280),
            viewport_height=b_data.get("viewport_height", 800),
            capture_screenshots=b_data.get("capture_screenshots", True),
            wait_for_network_idle_page_load_time=b_data.get("wait_for_network_idle_page_load_time", 2.5),
            maximum_wait_page_load_time=b_data.get("maximum_wait_page_load_time", 15.0)
        )

        llm_cfg = LLMConfig(
            provider=l_data.get("provider", "gemini"),
            model_name=l_data.get("model_name", "gemini-2.5-flash"),
            fallback_model_name=l_data.get("fallback_model_name", "gemini-1.5-pro"),
            max_retries=l_data.get("max_retries", 5),
            temperature=l_data.get("temperature", 0.1),
            api_key=l_data.get("api_key") or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        )

        rate_limit_cfg = RateLimitConfig(
            requests_per_minute=r_data.get("requests_per_minute", 15),
            inter_entity_delay_seconds=r_data.get("inter_entity_delay_seconds", 5.0),
            backoff_on_error_seconds=r_data.get("backoff_on_error_seconds", 15.0)
        )

        queue_cfg = QueueConfig(
            max_retries=q_data.get("max_retries", 3),
            batch_size=q_data.get("batch_size", 10),
            retry_delay_seconds=q_data.get("retry_delay_seconds", 5)
        )

        db_path_val = p_data.get("db_path")
        if not db_path_val:
            db_path = os.path.join(BASE_DIR, "Funding.sqlite")
        else:
            db_path = os.path.abspath(os.path.join(WORKFLOW_DIR, db_path_val))

        pt_val = p_data.get("prompt_template_path") or "prompts/browser_prompt.txt"
        prompt_template_path = os.path.abspath(os.path.join(WORKFLOW_DIR, pt_val))

        logs_val = p_data.get("logs_dir") or "logs"
        logs_dir = os.path.abspath(os.path.join(WORKFLOW_DIR, logs_val))

        outputs_val = p_data.get("outputs_dir") or "outputs"
        outputs_dir = os.path.abspath(os.path.join(WORKFLOW_DIR, outputs_val))

        screenshots_val = p_data.get("screenshots_dir") or "screenshots"
        screenshots_dir = os.path.abspath(os.path.join(WORKFLOW_DIR, screenshots_val))

        paths_cfg = PathsConfig(
            db_path=db_path,
            prompt_template_path=prompt_template_path,
            logs_dir=logs_dir,
            outputs_dir=outputs_dir,
            screenshots_dir=screenshots_dir
        )

        return cls(browser=browser_cfg, llm=llm_cfg, rate_limit=rate_limit_cfg, queue=queue_cfg, paths=paths_cfg)
