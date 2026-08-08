"""
parser.py
JSON Parser & Extractor for processing raw LLM / Browser-use outputs.
Handles markdown fences, multiple comma-separated JSON objects, arrays, and partial JSON structures.
"""

import re
import json
import logging
from typing import Dict, Any, List

class JSONParser:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extract_json(self, raw_text: str) -> Dict[str, Any]:
        """
        Safely extract and parse JSON dictionary from raw LLM / Agent text.
        Handles triple-backtick markdown fences, list roots, and comma-separated JSON objects.
        """
        if not raw_text or not isinstance(raw_text, str):
            raise ValueError("Raw output is empty or non-string.")

        text = raw_text.strip()

        # 1. Extract content from markdown code fences if present
        fence_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text, re.IGNORECASE)
        if fence_match:
            text = fence_match.group(1).strip()

        # 2. Try direct json.loads
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                self.logger.info("Successfully parsed structured JSON object from agent text.")
                return data
            elif isinstance(data, list):
                self.logger.info("Parsed JSON array from agent text; wrapping in dictionary structure.")
                return {"funding_programs": data}
        except json.JSONDecodeError:
            pass

        # 3. Handle comma-separated multiple JSON objects: "{...}, {...}" by wrapping in []
        if not text.startswith('[') and not text.startswith('{'):
            # Attempt to strip leading non-json chars up to first '{' or '['
            start_idx = min([idx for idx in [text.find('{'), text.find('[')] if idx != -1] or [0])
            text = text[start_idx:].strip()

        if text.startswith('{'):
            wrapped_text = f"[{text}]"
            try:
                data = json.loads(wrapped_text)
                if isinstance(data, list):
                    self.logger.info("Successfully recovered comma-separated JSON objects by wrapping in array.")
                    return {"funding_programs": data}
            except json.JSONDecodeError:
                pass

        # 4. Fallback: Parse individual JSON objects using regex
        matches = re.findall(r'\{[^{}]*\}', text)
        if matches:
            parsed_list = []
            for m in matches:
                try:
                    obj = json.loads(m)
                    if isinstance(obj, dict):
                        parsed_list.append(obj)
                except json.JSONDecodeError:
                    continue

            if parsed_list:
                self.logger.info(f"Fallback regex parser recovered {len(parsed_list)} JSON objects.")
                return {"funding_programs": parsed_list}

        err_msg = f"Failed to parse JSON output: No valid JSON dictionary could be extracted. Text preview: {raw_text[:200]}"
        self.logger.error(err_msg)
        raise ValueError(err_msg)
