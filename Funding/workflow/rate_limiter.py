"""
rate_limiter.py
Rate Limiter for controlling LLM API request rates, inter-entity execution pauses,
and exponential backoff on 429/503 HTTP status errors.
"""

import time
import logging
from typing import Optional
from config import RateLimitConfig

class RateLimiter:
    def __init__(self, config: RateLimitConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.last_request_time: float = 0.0
        self.consecutive_errors: int = 0

    def wait_if_needed(self):
        """Enforce inter-entity delay and requests-per-minute rate limiting."""
        now = time.time()
        elapsed = now - self.last_request_time

        min_interval = 60.0 / max(1, self.config.requests_per_minute)
        required_delay = max(min_interval, self.config.inter_entity_delay_seconds)

        if elapsed < required_delay:
            sleep_duration = required_delay - elapsed
            self.logger.info(f"[RateLimiter] Pausing for {sleep_duration:.2f}s to respect rate limits ({self.config.requests_per_minute} RPM)...")
            time.sleep(sleep_duration)

        self.last_request_time = time.time()

    def handle_error(self, is_rate_limit_or_unavailable: bool = True):
        """Apply exponential backoff pause on 429/503 errors."""
        if is_rate_limit_or_unavailable:
            self.consecutive_errors += 1
            backoff = self.config.backoff_on_error_seconds * (2 ** (self.consecutive_errors - 1))
            backoff = min(backoff, 180.0)  # Max 3 minutes
            self.logger.warning(f"[RateLimiter] Error encountered (503/429). Applying exponential backoff pause of {backoff:.1f}s (attempt {self.consecutive_errors})...")
            time.sleep(backoff)

    def record_success(self):
        """Reset consecutive error count on successful execution."""
        self.consecutive_errors = 0
