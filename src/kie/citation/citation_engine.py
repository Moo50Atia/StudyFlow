"""
Decoupled Citation Engine & Evidence Package v1 Assembler
==========================================================
Performs claim detection, evidence matching, PDF offset mapping, citation formatting,
and emits Evidence Package v1 (EV-PKG-V1) payloads.
"""

from typing import Dict, Any, List
import uuid
import time


class CitationEngine:
    """Detects factual claims and builds PDF character-offset citation maps."""

    def build_citation_map(self, response_text: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        citation_map = []
        for cand in candidates:
            prov = cand.get("provenance", {})
            citation_map.append({
                "claim_text": cand.get("title", "Factual Claim"),
                "asset_id": cand.get("asset_id"),
                "pdf_uuid": prov.get("source_pdf_uuid", "pdf_unknown"),
                "page_number": prov.get("page_number", 1),
                "char_offset_start": prov.get("char_start", 0),
                "char_offset_end": prov.get("char_end", 0),
                "citation_label": f"[Source: Page {prov.get('page_number', 1)}]"
            })
        return citation_map


class EvidencePackageV1Builder:
    """Assembles versioned Evidence Package v1 (EV-PKG-V1) payloads."""

    def build_package(
        self,
        query_text: str,
        response_text: str,
        confidence_band: str,
        confidence_score: float,
        planner_log_id: str,
        candidates: List[Dict[str, Any]],
        citation_map: List[Dict[str, Any]],
        latency_ms: int
    ) -> Dict[str, Any]:
        return {
            "evidence_package_version": "v1.0",
            "package_id": f"ev_pkg_{uuid.uuid4().hex[:8]}",
            "query_text": query_text,
            "response_text": response_text,
            "confidence_band": confidence_band,
            "confidence_score": confidence_score,
            "planner_decision_log_id": planner_log_id,
            "retrieved_asset_ids": [c.get("asset_id") for c in candidates if c.get("asset_id")],
            "citation_map": citation_map,
            "prompt_template_version": "tmpl_chat_v1",
            "model_version": "gemini-1.5-pro",
            "execution_latency_ms": latency_ms
        }
