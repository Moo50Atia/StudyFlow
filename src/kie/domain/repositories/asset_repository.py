"""
Single-Aggregate Repositories
=============================
Repositories for Knowledge Assets, Fragments, Relationships, Versions, Evidence, and Sessions.
"""

from typing import Dict, Any, Optional, List
from src.kos.storage.asset_store import AssetStore, FragmentStore
from src.kos.storage.relationship_store import RelationshipStore, GraphStore
from src.kie.domain.models.domain_models import KnowledgeAssetDomainModel, KnowledgeFragmentDomainModel


class AssetRepository:
    def __init__(self, material_id: str):
        self.material_id = material_id
        self.store = AssetStore()

    def get_all(self) -> List[KnowledgeAssetDomainModel]:
        raw_assets = self.store.load_assets(self.material_id)
        return [KnowledgeAssetDomainModel(**a) for a in raw_assets]

    def save_all(self, assets: List[KnowledgeAssetDomainModel]) -> str:
        raw_assets = [a.dict() for a in assets]
        return self.store.save_assets(self.material_id, raw_assets)


class FragmentRepository:
    def __init__(self, material_id: str):
        self.material_id = material_id
        self.store = FragmentStore()

    def get_all(self) -> List[KnowledgeFragmentDomainModel]:
        raw_frags = self.store.load_fragments(self.material_id)
        return [KnowledgeFragmentDomainModel(**f) for f in raw_frags]

    def save_all(self, fragments: List[KnowledgeFragmentDomainModel]) -> str:
        raw_frags = [f.dict() for f in fragments]
        return self.store.save_fragments(self.material_id, raw_frags)


class RelationshipRepository:
    def __init__(self, material_id: str):
        self.material_id = material_id
        self.store = RelationshipStore()

    def save_relationships(self, rels: List[Dict[str, Any]]) -> str:
        return self.store.save_relationships(self.material_id, rels)
