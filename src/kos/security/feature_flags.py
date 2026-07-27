"""
KOS Security Feature Flags & Governance Engine
=============================================
Manages feature flags and capability governance across tenant environments.
"""

from typing import Dict


class FeatureFlagEngine:
    """Manages dynamic feature flag toggles and rollout rules."""

    def __init__(self):
        self._flags: Dict[str, bool] = {
            "kie_graph_rag": True,
            "kie_bm25_sparse": True,
            "kie_podcast_audio": False,
            "kie_visual_scenes": True,
        }

    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        return self._flags.get(flag_name, default)

    def set_flag(self, flag_name: str, enabled: bool) -> None:
        self._flags[flag_name] = enabled
