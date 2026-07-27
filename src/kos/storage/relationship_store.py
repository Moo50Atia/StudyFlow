"""
KOS Relationship & Graph Store
==============================
Manages canonical relationship links and derived graph structure persistence.
"""

from typing import Dict, Any, List
import json
import os


class RelationshipStore:
    """Canonical store for typed asset relationships."""

    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir

    def save_relationships(self, material_id: str, relationships: List[Dict[str, Any]]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "relationships.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(relationships, f, indent=2, ensure_ascii=False)
        return file_path


class GraphStore:
    """Store for derived Knowledge Graph structure."""

    def __init__(self, storage_dir: str = "Generating/Materials"):
        self.storage_dir = storage_dir

    def save_graph(self, material_id: str, graph_data: Dict[str, Any]) -> str:
        material_dir = os.path.join(self.storage_dir, material_id)
        os.makedirs(material_dir, exist_ok=True)
        file_path = os.path.join(material_dir, "knowledge_graph.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        return file_path
