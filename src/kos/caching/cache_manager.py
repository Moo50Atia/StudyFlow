"""
KOS 6-Tier Multi-Layer Cache Manager
====================================
Manages Embedding, Retrieval, Prompt, Citation, Response, and Session cache tiers.
"""

from typing import Dict, Any, Optional
import hashlib


class MultiTierCacheManager:
    """Implements 6 distinct memory and key-value cache tiers."""

    def __init__(self):
        self._embedding_cache: Dict[str, Any] = {}
        self._retrieval_cache: Dict[str, Any] = {}
        self._prompt_cache: Dict[str, Any] = {}
        self._citation_cache: Dict[str, Any] = {}
        self._response_cache: Dict[str, Any] = {}
        self._session_cache: Dict[str, Any] = {}

    @staticmethod
    def hash_key(key_text: str) -> str:
        return hashlib.sha256(key_text.encode("utf-8")).hexdigest()

    def get_response(self, query_key: str) -> Optional[Any]:
        hk = self.hash_key(query_key)
        return self._response_cache.get(hk)

    def set_response(self, query_key: str, response_payload: Any) -> None:
        hk = self.hash_key(query_key)
        self._response_cache[hk] = response_payload

    def clear_all(self) -> None:
        self._embedding_cache.clear()
        self._retrieval_cache.clear()
        self._prompt_cache.clear()
        self._citation_cache.clear()
        self._response_cache.clear()
        self._session_cache.clear()
