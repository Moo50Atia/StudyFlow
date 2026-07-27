"""
KOS Capability, Worker, Plugin, Prompt Registries
================================================
Manages dynamic registration of educational capabilities, workers, plugins, and prompt templates.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class PromptRegistryEntry(BaseModel):
    template_id: str
    service_name: str
    version: int
    system_instruction: str
    output_schema_json: Dict[str, Any] = Field(default_factory=dict)
    required_asset_types: List[str] = Field(default_factory=list)


class PluginRegistryEntry(BaseModel):
    plugin_id: str
    plugin_name: str
    version: str
    enabled: bool = True
    capabilities: List[str] = Field(default_factory=list)


class WorkerRegistryEntry(BaseModel):
    worker_id: str
    worker_type: str
    status: str = "IDLE"  # IDLE, BUSY, FAILED
    total_jobs_processed: int = 0


class CapabilityRegistryEntry(BaseModel):
    capability_id: str
    capability_name: str
    providing_plugin_id: str
    status: str = "ENABLED"
    required_asset_types: List[str] = Field(default_factory=list)


class PromptRegistry:
    def __init__(self):
        self._prompts: Dict[str, PromptRegistryEntry] = {}

    def register(self, entry: PromptRegistryEntry) -> None:
        self._prompts[entry.template_id] = entry

    def get(self, template_id: str) -> Optional[PromptRegistryEntry]:
        return self._prompts.get(template_id)


class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, CapabilityRegistryEntry] = {}

    def register(self, entry: CapabilityRegistryEntry) -> None:
        self._capabilities[entry.capability_id] = entry

    def list_capabilities(self) -> List[CapabilityRegistryEntry]:
        return list(self._capabilities.values())
