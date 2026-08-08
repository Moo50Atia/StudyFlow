#!/usr/bin/env python3
"""
manager.py
Main Workflow Orchestrator & Loop Controller for Funding Enrichment Browser-use Framework.
"""

import os
import sys
import json
import time
import argparse
from typing import Optional

# Ensure workflow directory is in PYTHONPATH
WORKFLOW_DIR = os.path.dirname(os.path.abspath(__file__))
if WORKFLOW_DIR not in sys.path:
    sys.path.insert(0, WORKFLOW_DIR)

from config import AppConfig
from utils import setup_logger, ensure_directories
from rate_limiter import RateLimiter
from queue_manager import QueueManager
from browser_prompt import PromptLoader
from browser_runner import BrowserRunner
from parser import JSONParser
from validator import DataValidator
from updater import DatabaseUpdater

class WorkflowManager:
    def __init__(self, config_path: Optional[str] = None):
        if config_path and os.path.exists(config_path):
            self.config = AppConfig.load_from_json(config_path)
        else:
            default_cfg = os.path.join(WORKFLOW_DIR, "config.json")
            self.config = AppConfig.load_from_json(default_cfg)

        ensure_directories([
            self.config.paths.logs_dir,
            self.config.paths.outputs_dir,
            self.config.paths.screenshots_dir
        ])

        # Initialize Loggers
        self.mgr_logger = setup_logger("manager", os.path.join(self.config.paths.logs_dir, "manager.log"))
        self.browser_logger = setup_logger("browser", os.path.join(self.config.paths.logs_dir, "browser.log"))
        self.val_logger = setup_logger("validation", os.path.join(self.config.paths.logs_dir, "validation.log"))
        self.upd_logger = setup_logger("update", os.path.join(self.config.paths.logs_dir, "update.log"))

        # Initialize Components
        self.rate_limiter = RateLimiter(self.config.rate_limit, self.mgr_logger)
        self.queue_mgr = QueueManager(self.config, self.mgr_logger)
        self.prompt_loader = PromptLoader(self.config, self.mgr_logger)
        self.browser_runner = BrowserRunner(self.config, self.browser_logger)
        self.json_parser = JSONParser(self.val_logger)
        self.validator = DataValidator(self.val_logger)
        self.updater = DatabaseUpdater(self.config, self.upd_logger)

    def run_single(self) -> bool:
        """Process one entity from queue."""
        self.rate_limiter.wait_if_needed()

        entity = self.queue_mgr.get_next_entity()
        if not entity:
            self.mgr_logger.info("No pending entities in queue.")
            return False

        self.mgr_logger.info(f"=== Starting Enrichment for Entity #{entity.id} [{entity.name}] ===")

        try:
            # 1. Generate Prompt
            prompt_text = self.prompt_loader.generate_prompt(entity)

            # 2. Launch Browser-use Agent
            runner_result = self.browser_runner.run_agent(entity, prompt_text)
            if not runner_result.success or not runner_result.raw_output:
                err_msg = runner_result.error_message or "Browser agent returned empty output."
                self.queue_mgr.mark_failed(entity.id, err_msg)
                self.rate_limiter.handle_error(is_rate_limit_or_unavailable="503" in err_msg or "429" in err_msg or "UNAVAILABLE" in err_msg)
                return True

            # Save raw output JSON file for audit
            raw_output_path = os.path.join(self.config.paths.outputs_dir, f"entity_{entity.id}.json")
            with open(raw_output_path, 'w', encoding='utf-8') as f:
                f.write(runner_result.raw_output)

            # 3. Parse JSON Output
            parsed_dict = self.json_parser.extract_json(runner_result.raw_output)

            # 4. Validate Data
            val_result = self.validator.validate_result(parsed_dict, entity.id)

            # 5. Persist to Database
            self.updater.persist_enrichment(entity, val_result)

            self.rate_limiter.record_success()
            self.mgr_logger.info(f"=== Completed Entity #{entity.id} [{entity.name}] in {runner_result.execution_time_seconds:.2f}s ===")
            return True

        except Exception as e:
            err_str = f"Workflow exception processing entity #{entity.id}: {str(e)}"
            self.mgr_logger.error(err_str)
            self.queue_mgr.mark_failed(entity.id, err_str)
            self.rate_limiter.handle_error(is_rate_limit_or_unavailable="503" in err_str or "429" in err_str or "UNAVAILABLE" in err_str)
            return True

    def run_loop(self, limit: Optional[int] = None):
        """Run continuous queue loop."""
        self.mgr_logger.info("Starting Workflow Loop Controller...")
        self.queue_mgr.reset_crashed_jobs()

        processed_count = 0
        while True:
            if limit and processed_count >= limit:
                self.mgr_logger.info(f"Reached processing limit of {limit} entities.")
                break

            has_more = self.run_single()
            if not has_more:
                self.mgr_logger.info("Queue completed or empty. Exiting loop.")
                break

            processed_count += 1
            time.sleep(self.config.queue.retry_delay_seconds)

def main():
    parser = argparse.ArgumentParser(description="Funding Enrichment Workflow Manager")
    parser.add_argument("--config", type=str, help="Path to config.json file")
    parser.add_argument("--limit", type=int, help="Maximum number of entities to process")
    args = parser.parse_args()

    mgr = WorkflowManager(config_path=args.config)
    mgr.run_loop(limit=args.limit)

if __name__ == '__main__':
    main()
