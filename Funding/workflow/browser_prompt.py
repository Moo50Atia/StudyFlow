"""
browser_prompt.py
Prompt Loader & Placeholder Interpolator for Browser-use Agent research tasks.
"""

import os
import logging
from models import FundingEntityItem
from config import AppConfig

class PromptLoader:
    def __init__(self, config: AppConfig, logger: logging.Logger):
        self.config = config
        self.prompt_template_path = config.paths.prompt_template_path
        self.logger = logger
        self._template_cache: str = ""

    def load_template(self) -> str:
        """Load prompt template from file system."""
        if not os.path.exists(self.prompt_template_path):
            err = f"Prompt template not found at path: {self.prompt_template_path}"
            self.logger.error(err)
            raise FileNotFoundError(err)

        with open(self.prompt_template_path, 'r', encoding='utf-8') as f:
            self._template_cache = f.read()
        return self._template_cache

    def generate_prompt(self, entity: FundingEntityItem) -> str:
        """Interpolate placeholders in the prompt template with entity details."""
        if not self._template_cache:
            self.load_template()

        replacements = {
            "{{ENTITY_NAME}}": entity.name or "N/A",
            "{{CATEGORY}}": entity.category_name or "N/A",
            "{{COUNTRY}}": entity.country or "Unspecified",
            "{{CITY}}": entity.city or "Unspecified",
            "{{OFFICIAL_WEBSITE}}": entity.official_website or "N/A",
            "{{DESCRIPTION}}": entity.description or "N/A",
            "{{PRIORITY}}": entity.priority or "Medium"
        }

        prompt_text = self._template_cache
        for placeholder, value in replacements.items():
            prompt_text = prompt_text.replace(placeholder, str(value))

        self.logger.info(f"Generated research prompt for entity #{entity.id} [{entity.name}]")
        return prompt_text
