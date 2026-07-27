"""
KOS Core Configuration Runtime & Schema Validator
=================================================
Manages environment configurations, runtime overrides, schema validation, and profiles
for the Knowledge Operating System (KOS) platform kernel.
"""

import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class KOSConfigSchema(BaseModel):
    environment: str = Field(default="development", description="Execution environment (development, staging, production)")
    debug: bool = Field(default=False, description="Enable verbose diagnostic logs")
    material_storage_path: str = Field(default="Generating/Materials", description="Path to intermediate material artifacts")
    max_retrieval_latency_ms: int = Field(default=800, description="Latency SLA for retrieval engine")
    cache_ttl_seconds: int = Field(default=3600, description="Default cache TTL")
    default_embedding_model: str = Field(default="text-embedding-3-large", description="Default dense vector model")


class ConfigurationRuntime:
    """Manages system configuration loading, validation, and dynamic runtime overrides."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._raw_config: Dict[str, Any] = {}
        self._validated_config: Optional[KOSConfigSchema] = None
        self._overrides: Dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        """Loads configuration from environment variables or JSON file."""
        config_data = {}
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

        # Merge environment variable overrides
        env_config = {
            "environment": os.getenv("KOS_ENV", config_data.get("environment", "development")),
            "debug": os.getenv("KOS_DEBUG", "false").lower() in ("true", "1", "t"),
            "material_storage_path": os.getenv("KOS_STORAGE_PATH", config_data.get("material_storage_path", "Generating/Materials")),
            "max_retrieval_latency_ms": int(os.getenv("KOS_RETRIEVAL_SLA_MS", config_data.get("max_retrieval_latency_ms", 800))),
            "cache_ttl_seconds": int(os.getenv("KOS_CACHE_TTL", config_data.get("cache_ttl_seconds", 3600))),
            "default_embedding_model": os.getenv("KOS_EMBEDDING_MODEL", config_data.get("default_embedding_model", "text-embedding-3-large")),
        }
        config_data.update(env_config)
        config_data.update(self._overrides)
        self._raw_config = config_data
        self._validated_config = KOSConfigSchema(**config_data)

    def set_override(self, key: str, value: Any) -> None:
        """Sets a dynamic runtime configuration override."""
        self._overrides[key] = value
        self.reload()

    @property
    def config(self) -> KOSConfigSchema:
        if not self._validated_config:
            self.reload()
        assert self._validated_config is not None
        return self._validated_config
