"""
KOS Security Secret Manager
===========================
Manages secure retrieval and encryption/decryption of system secrets and API credentials.
"""

import os
from typing import Optional


class SecretManager:
    """Retrieves environment secrets and handles key encryption wrappers."""

    @staticmethod
    def get_secret(key_name: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key_name, default)

    @staticmethod
    def mask_secret(secret_value: str) -> str:
        """Masks a secret string for safe logging."""
        if not secret_value or len(secret_value) < 8:
            return "********"
        return f"{secret_value[:4]}...{secret_value[-4:]}"
