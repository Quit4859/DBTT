"""
Semantic Memory for DBTT Cognitive Operating System
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from dbtt.core.interfaces import MemoryProtocol
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class SemanticMemory(MemoryProtocol):
    """Semantic memory for storing knowledge and facts about the world"""

    def __init__(self):
        self._memory: List[Dict[str, Any]] = []
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize semantic memory"""
        self.config = config
        self.initialized = True
        self.max_entries = config.get("max_entries", 150)
        app_logger.info(f"Initialized Semantic Memory with max entries: {self.max_entries}")

    async def store(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content in semantic memory"""
        entry = {
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now(),
            "memory_type": "semantic"
        }

        self._memory.append(entry)

        if len(self._memory) > self.max_entries:
            old_entries = self._memory[:len(self._memory) - self.max_entries]
            self._memory = self._memory[len(self._memory) - self.max_entries:]

        app_logger.debug(f"Stored in semantic memory: {content[:50]}...")

    async def retrieve(self, query: str) -> List[str]:
        """Retrieve semantic memory entries matching the query"""
        results = []
        query_lower = query.lower()

        for entry in self._memory:
            if query_lower in entry["content"].lower() or any(
                query_lower in str(v).lower() for v in entry["metadata"].values()
            ):
                results.append(entry["content"])

        app_logger.debug(f"Retrieved {len(results)} entries from semantic memory for query: {query}")
        return results

    async def clear(self) -> None:
        """Clear semantic memory"""
        self._memory.clear()
        app_logger.debug("Cleared semantic memory")

    async def shutdown(self) -> None:
        """Shutdown semantic memory"""
        self.initialized = False
        self._memory.clear()
        app_logger.info("Shut down Semantic Memory")

    def build_knowledge_graph(self) -> Dict[str, Any]:
        """Build a knowledge graph from semantic memory entries"""
        graph = {}
        for entry in self._memory:
            content_words = entry["content"].split()
            for word in content_words:
                if word not in graph:
                    graph[word] = []
                graph[word].extend(content_words)
                graph[word] = list(set(graph[word]))

        app_logger.debug(f"Built knowledge graph with {len(graph)} nodes")
        return graph
