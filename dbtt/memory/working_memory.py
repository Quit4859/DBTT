"""
Working Memory for DBTT Cognitive Operating System
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dbtt.core.interfaces import MemoryProtocol
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class WorkingMemory(MemoryProtocol):
    """Working memory for temporary thought storage during processing"""

    def __init__(self):
        self._memory: List[Dict[str, Any]] = []
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize working memory"""
        self.config = config
        self.initialized = True
        self.max_entries = config.get("max_entries", 100)
        app_logger.info(f"Initialized Working Memory with max entries: {self.max_entries}")

    async def store(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content in working memory"""
        entry = {
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat(),
            "memory_type": "working"
        }

        self._memory.append(entry)

        if len(self._memory) > self.max_entries:
            self._memory.pop(0)

        app_logger.debug(f"Stored in working memory: {content[:50]}...")

    async def retrieve(self, query: str) -> List[str]:
        """Retrieve memory entries matching the query"""
        results = []
        query_lower = query.lower()

        for entry in self._memory:
            if query_lower in entry["content"].lower() or any(
                query_lower in str(v).lower() for v in entry["metadata"].values()
            ):
                results.append(entry["content"])

        app_logger.debug(f"Retrieved {len(results)} entries from working memory for query: {query}")
        return results

    async def clear(self) -> None:
        """Clear working memory"""
        self._memory.clear()
        app_logger.debug("Cleared working memory")

    async def shutdown(self) -> None:
        """Shutdown working memory"""
        self.initialized = False
        self._memory.clear()
        app_logger.info("Shut down Working Memory")

    def get_active_thoughts(self) -> List[Dict[str, Any]]:
        """Get active thoughts (recent entries)"""
        cutoff_time = datetime.now() - timedelta(minutes=30)
        active = []

        for entry in self._memory:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time > cutoff_time:
                active.append(entry)

        return active
