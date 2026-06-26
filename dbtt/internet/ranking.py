"""
Search Results Ranking Module for DBTT Cognitive Operating System
"""

from typing import Dict, Any, List
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class SearchResultsRanker:
    """Ranking module for internet search results"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.ranking_methods = self.config.get("ranking_methods", ["relevance", "authority", "freshness"])
        self.authority_weight = self.config.get("authority_weight", 0.4)
        self.freshness_weight = self.config.get("freshness_weight", 0.3)
        self.relevance_weight = self.config.get("relevance_weight", 0.3)
        app_logger.info("SearchResultsRanker module initialized")

    def rank(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rank search results based on multiple criteria"""
        app_logger.info(f"Ranking {len(results)} search results for query: {query}")

        for result in results:
            # Calculate scores for each ranking method
            result["authority_score"] = self._calculate_authority_score(result)
            result["freshness_score"] = self._calculate_freshness_score(result)
            result["relevance_score"] = self._calculate_relevance_score(result, query)

            # Calculate weighted final score
            result["final_score"] = (
                result["authority_score"] * self.authority_weight +
                result["freshness_score"] * self.freshness_weight +
                result["relevance_score"] * self.relevance_weight
            )

        # Sort results by final score in descending order
        ranked_results = sorted(results, key=lambda x: x["final_score"], reverse=True)
        app_logger.debug(f"Ranked results, top score: {ranked_results[0]['final_score'] if ranked_results else 'N/A'}")
        return ranked_results

    def _calculate_authority_score(self, result: Dict[str, Any]) -> float:
        """Calculate authority score based on domain authority and source reputation"""
        domain = result.get("url", "").split("/")[2] if "//" in result.get("url", "") else "unknown"

        # Domain-specific authority scores
        authority_map = {
            "example.com": 0.9,
            "edu": 0.95,
            "gov": 0.98,
            "org": 0.85,
            "wikipedia.org": 0.9,
            "github.com": 0.7,
            "medium.com": 0.6,
            "blogspot.com": 0.4
        }

        base_authority = authority_map.get(domain, 0.5)

        # Adjust based on snippet length and content quality
        snippet = result.get("snippet", "")
        if len(snippet) > 200:
            base_authority += 0.1
        elif len(snippet) < 50:
            base_authority -= 0.1

        return max(0.0, min(1.0, base_authority))

    def _calculate_freshness_score(self, result: Dict[str, Any]) -> float:
        """Calculate freshness score based on publication date"""
        try:
            pub_date_str = result.get("publication_date")
            if not pub_date_str:
                return 0.5

            # Parse publication date
            from datetime import datetime
            pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            now = datetime.now(pub_date.tzinfo)

            # Calculate age in days
            age_days = (now - pub_date).days

            # Decay function: newer content gets higher scores
            freshness = max(0.0, 1.0 - (age_days / 365.0))
            return freshness
        except:
            return 0.5

    def _calculate_relevance_score(self, result: Dict[str, Any], query: str) -> float:
        """Calculate relevance score based on query term matching"""
        query_words = set(query.lower().split())
        snippet = result.get("snippet", "").lower()
        title = result.get("title", "").lower()

        snippet_words = set(snippet.split())
        title_words = set(title.split())

        # Calculate overlap
        query_snippet_overlap = len(query_words.intersection(snippet_words))
        query_title_overlap = len(query_words.intersection(title_words))

        # Normalize scores
        max_overlap = min(len(query_words), len(snippet_words))
        snippet_relevance = query_snippet_overlap / max_overlap if max_overlap > 0 else 0.0

        max_title_overlap = min(len(query_words), len(title_words))
        title_relevance = query_title_overlap / max_title_overlap if max_title_overlap > 0 else 0.0

        # Weight title more heavily
        return (snippet_relevance * 0.7) + (title_relevance * 0.3)
