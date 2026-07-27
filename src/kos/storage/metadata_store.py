"""
KOS Metadata, Version, Attachment & Embedding Stores
===================================================
Manages material metadata, version histories, static attachments, and raw embedding arrays.
"""

from typing import Dict, Any, List
import json
import os


class MetadataStore:
    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir

    def save_metadata(self, material_id: str, metadata: Dict[str, Any]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "material_config.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        return file_path


class VersionStore:
    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir

    def save_version_history(self, material_id: str, version_data: List[Dict[str, Any]]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "version_history.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(version_data, f, indent=2, ensure_ascii=False)
        return file_path
