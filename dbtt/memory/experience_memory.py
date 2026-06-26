"""
Experience Memory for DBTT Cognitive Operating System
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from dbtt.core.interfaces import MemoryProtocol
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class ExperienceMemory(MemoryProtocol):
    """Experience memory for storing learned behaviors and solutions"""

    def __init__(self):
        self._memory: List[Dict[str, Any]] = []
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize experience memory"""
        self.config = config
        self.initialized = True
        self.max_entries = config.get("max_entries", 100)
        app_logger.info(f"Initialized Experience Memory with max entries: {self.max_entries}")

    async def store(self, content: str, metadata: Dict[str, Any]) -> None:
        """Store content in experience memory"""
        entry = {
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now(),
            "memory_type": "experience"
        }

        self._memory.append(entry)

        if len(self._memory) > self.max_entries:
            old_entries = self._memory[:len(self._memory) - self.max_entries]
            self._memory = self._memory[len(self._memory) - self.max_entries:]

        app_logger.debug(f"Stored in experience memory: {content[:50]}...")

    async def retrieve(self, query: str) -> List[str]:
        """Retrieve experience memory entries matching the query"""
        results = []
        query_lower = query.lower()

        for entry in self._memory:
            if query_lower in entry["content"].lower() or any(
                query_lower in str(v).lower() for v in entry["metadata"].values()
            ):
                results.append(entry["content"])

        app_logger.debug(f"Retrieved {len(results)} entries from experience memory for query: {query}")
        return results

    async def clear(self) -> None:
        """Clear experience memory"""
        self._memory.clear()
        app_logger.debug("Cleared experience memory")

    async def shutdown(self) -> None:
        """Shutdown experience memory"""
        self.initialized = False
        self._memory.clear()
        app_logger.info("Shut down Experience Memory")

    def get_strategies(self, problem: str) -> List[str]:
        """Get strategies for solving a specific problem"""
        strategies = []
        problem_lower = problem.lower()

        for entry in self._memory:
            if "strategy" in str(entry.get("metadata", {})).lower():
                strategies.append(entry["content"])

        app_logger.debug(f"Retrieved {len(strategies)} strategies for problem: {problem}")
        return strategies

    def get_learned_behaviors(self, context: str) -> List[Dict[str, Any]]:
        """Get learned behaviors for a specific context"""
        behaviors = []
        context_lower = context.lower()

        for entry in self._memory:
            if context_lower in str(entry.get("metadata", {})).get("context", "").lower():
                behaviors.append(entry)

        app_logger.debug(f"Retrieved {len(behaviors)} learned behaviors for context: {context}")
        return behaviors
