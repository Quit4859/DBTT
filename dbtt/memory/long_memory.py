"""
Long-term Memory for DBTT Cognitive Operating System
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from dbtt.core.interfaces import MemoryProtocol
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class LongMemory(MemoryProtocol):
    """Long-term memory for persistent storage of important experiences"""

    def __init__(self):
        self._memory: List[Dict[str, Any]] = []
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize long memory"""
        self.config = config
        self.initialized = True
        self.max_entries = config.get("max_entries", 200)
        self.ttl = config.get("ttl", 86400)
        app_logger.info(f"Initialized Long Memory with max entries: {self.max_entries}, TTL: {self.ttl}")

    async def store(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content in long memory"""
        entry = {
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now(),
            "memory_type": "long"
        }

        self._memory.append(entry)

        if len(self._memory) > self.max_entries:
            old_entries = self._memory[:len(self._memory) - self.max_entries]
            self._memory = self._memory[len(self._memory) - self.max_entries:]

        self._cleanup_expired()

        app_logger.debug(f"Stored in long memory: {content[:50]}...")

    async def retrieve(self, query: str) -> List[str]:
        """Retrieve memory entries matching the query"""
        results = []
        query_lower = query.lower()
        now = datetime.now()

        for entry in self._memory:
            if query_lower in entry["content"].lower() or any(
                query_lower in str(v).lower() for v in entry["metadata"].values()
            ):
                if now.timestamp() - entry["timestamp"].timestamp() < self.ttl:
                    results.append(entry["content"])
                else:
                    self._memory.remove(entry)

        app_logger.debug(f"Retrieved {len(results)} entries from long memory for query: {query}")
        return results

    async def clear(self) -> None:
        """Clear long memory"""
        self._memory.clear()
        app_logger.debug("Cleared long memory")

    async def shutdown(self) -> None:
        """Shutdown long memory"""
        self.initialized = False
        self._memory.clear()
        app_logger.info("Shut down Long Memory")

    def _cleanup_expired(self) -> None:
        """Remove expired entries"""
        now = datetime.now()
        self._memory = [
            entry for entry in self._memory
            if (now.timestamp() - entry["timestamp"].timestamp()) < self.ttl
        ]
