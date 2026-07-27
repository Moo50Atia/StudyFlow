"""
Query Analyzer & Intent Classifier
===================================
Classifies input queries into one of 12 intent categories to drive retrieval strategy selection.
"""

from typing import Dict, Any, List


class QueryAnalyzer:
    """Analyzes text queries and assigns pedagogical intent classes."""

    INTENT_KEYWORDS = {
        "INTENT_DEF": ["define", "definition", "what is", "meaning of"],
        "INTENT_CMP": ["compare", "difference", "versus", "vs"],
        "INTENT_CALC": ["calculate", "formula", "equation", "derivation", "solve"],
        "INTENT_LAW": ["law", "principle", "rule", "theorem"],
        "INTENT_CASE": ["case study", "clinical", "patient", "engineering case"],
        "INTENT_EXAM": ["exam tip", "common error", "mistake", "trick"],
        "INTENT_ANALOGY": ["analogy", "egyptian", "example", "story"],
    }

    def classify_intent(self, query_text: str) -> str:
        text_lower = query_text.lower()
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    return intent
        return "INTENT_GENERIC"
