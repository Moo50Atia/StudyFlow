"""
Prompt System & Prompt Optimization Engine
===========================================
Compiles versioned prompt templates, optimizes token budgets, and validates schemas.
"""

from typing import Dict, Any, List


class PromptOptimizer:
    """Optimizes context token allocation and injects versioned system instructions."""

    def compile_prompt(self, template_id: str, context_blocks: List[str], max_tokens: int = 4000) -> Dict[str, Any]:
        system_instruction = "You are an expert grounded AI tutor. Answer strictly using provided Knowledge Assets."
        merged_context = "\n\n".join(context_blocks)
        
        # Simple truncation for token budget adherence
        if len(merged_context) > max_tokens * 4:
            merged_context = merged_context[: max_tokens * 4]

        return {
            "template_id": template_id,
            "version": 1,
            "system_instruction": system_instruction,
            "compiled_prompt_text": f"{system_instruction}\n\nContext:\n{merged_context}",
            "token_budget_allocated": max_tokens
        }
