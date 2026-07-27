"""
KOS Model, Tokenizer, Prompt, Plugin Registries
==============================================
Manages model specs, tokenizer encodings, prompt templates, and plugin manifests.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ModelRegistryEntry(BaseModel):
    model_id: str
    provider: str  # Google, OpenAI, Anthropic
    context_window: int
    cost_per_1k_input_tokens_usd: float
    cost_per_1k_output_tokens_usd: float


class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, ModelRegistryEntry] = {
            "gemini-1.5-pro": ModelRegistryEntry(
                model_id="gemini-1.5-pro",
                provider="Google",
                context_window=1000000,
                cost_per_1k_input_tokens_usd=0.00125,
                cost_per_1k_output_tokens_usd=0.00500,
            )
        }

    def get_model(self, model_id: str) -> Optional[ModelRegistryEntry]:
        return self._models.get(model_id)


class TokenizerRegistry:
    """Manages token encoders and character-to-token ratio estimates."""

    @staticmethod
    def estimate_token_count(text: str) -> int:
        return len(text) // 4 + 1
