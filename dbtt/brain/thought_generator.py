"""
Base class for thought generation modules
"""

from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any
from dbtt.models.thought import ThoughtGraph, BrainModule
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class ThoughtGenerator(BrainModule):
    """Base class for all thought generators"""

    def __init__(self, name: str):
        self._name = name
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the thought generator"""
        self.config = config
        self.initialized = True
        app_logger.info(f"Initialized thought generator: {self.name}")

    @abstractmethod
    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Generate thoughts and update thought graph"""
        pass

    def shutdown(self) -> None:
        """Shutdown the thought generator"""
        self.initialized = False
        app_logger.info(f"Shut down thought generator: {self.name}")

    @property
    def name(self) -> str:
        return self._name

    def generate_thought(self, content: str, priority: str = "medium", confidence: float = 0.5,
                         source: str = "", parent: str = None, metadata: Dict[str, Any] = None) -> 'Thought':
        """Generate a thought object"""
        if metadata is None:
            metadata = {}

        thought_id = f"{self.name}_{priority}_{len(str(datetime.now()))}"
        status = Priority.HIGH if priority == "high" else Priority.MEDIUM if priority == "medium" else Priority.LOW

        return Thought(
            id=thought_id,
            content=content,
            confidence=confidence,
            priority=status,
            parent=parent,
            source=source,
            metadata=metadata
        )
