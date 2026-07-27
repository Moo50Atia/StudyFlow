"""
Canonical Knowledge Store Subsystems
====================================
Master canonical source of truth for Knowledge Assets, Fragments, Relationships, and Metadata.
"""

from typing import Dict, Any, Optional, List
import json
import os
from pydantic import BaseModel


class AssetStore:
    """Canonical store for Knowledge Assets."""

    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

    def save_assets(self, material_id: str, assets: List[Dict[str, Any]]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "knowledge_assets.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(assets, f, indent=2, ensure_ascii=False)
        self._memory_cache[material_id] = {a["asset_id"]: a for a in assets}
        return file_path

    def load_assets(self, material_id: str) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.storage_dir, material_id, "knowledge_assets.json")
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)


class FragmentStore:
    """Canonical store for Knowledge Fragments."""

    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir

    def save_fragments(self, material_id: str, fragments: List[Dict[str, Any]]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "knowledge_fragments.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(fragments, f, indent=2, ensure_ascii=False)
        return file_path

    def load_fragments(self, material_id: str) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.storage_dir, material_id, "knowledge_fragments.json")
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
