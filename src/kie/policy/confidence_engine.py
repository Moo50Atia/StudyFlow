"""
KIE Policy & Confidence Engine
=============================
Evaluates retrieval confidence scores against policy bands (VERY_HIGH, HIGH, MEDIUM, LOW, UNSUPPORTED)
and enforces safe fallback and abstention behaviors.
"""

from typing import Dict, Any, List


class PolicyConfidenceEngine:
    """Evaluates policy confidence bands and fallback rules."""

    def evaluate_confidence(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not candidates:
            return {
                "confidence_band": "UNSUPPORTED",
                "confidence_score": 0.0,
                "should_abstain": True,
                "disclaimer": "The requested topic is not covered in your course materials."
            }

        max_score = max(c.get("score", 0.0) for c in candidates)
        
        if max_score >= 0.85:
            band = "VERY_HIGH"
            should_abstain = False
            disclaimer = None
        elif max_score >= 0.70:
            band = "HIGH"
            should_abstain = False
            disclaimer = None
        elif max_score >= 0.50:
            band = "MEDIUM"
            should_abstain = False
            disclaimer = "This response is derived from partial course context. Please verify with Section X."
        elif max_score >= 0.35:
            band = "LOW"
            should_abstain = True
            disclaimer = "Weak semantic match found. Please refine your query."
        else:
            band = "UNSUPPORTED"
            should_abstain = True
            disclaimer = "The requested topic is not covered in your course materials."

        return {
            "confidence_band": band,
            "confidence_score": max_score,
            "should_abstain": should_abstain,
            "disclaimer": disclaimer
        }
