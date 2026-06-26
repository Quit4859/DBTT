"""
Core interfaces and abstractions for DBTT Cognitive Operating System
"""

import networkx as nx
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class BrainModule(ABC):
    """Base class for all Brain modules"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module"""
        pass

    @abstractmethod
    def process(self, thought_graph: 'ThoughtGraph') -> 'ThoughtGraph':
        """Process the thought graph and return updated thought graph"""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the module"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get module name"""
        pass


class BrainModuleProtocol(Protocol):
    """Protocol defining brain module interface"""

    def initialize(self, config: Dict[str, Any]) -> None: ...

    def process(self, thought_graph: 'ThoughtGraph') -> 'ThoughtGraph': ...

    def shutdown(self) -> None: ...

    @property
    def name(self) -> str: ...


@dataclass
class Thought:
    id: str
    content: str
    confidence: float
    priority: Priority
    status: Status = Status.PENDING
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    created_time: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "confidence": self.confidence,
            "priority": self.priority.value,
            "status": self.status.value,
            "parent": self.parent,
            "children": self.children,
            "source": self.source,
            "metadata": self.metadata,
            "dependencies": self.dependencies,
            "created_time": self.created_time.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Thought':
        return cls(
            id=data["id"],
            content=data["content"],
            confidence=data["confidence"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            parent=data.get("parent"),
            children=data.get("children", []),
            source=data.get("source", ""),
            metadata=data.get("metadata", {}),
            dependencies=data.get("dependencies", []),
            created_time=datetime.fromisoformat(data["created_time"])
        )


class BrainModule(ABC):
    """Base class for all Brain modules"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the module"""
        pass

    @abstractmethod
    def process(self, thought_graph: 'ThoughtGraph') -> 'ThoughtGraph':
        """Process the thought graph and return updated thought graph"""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the module"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get module name"""
        pass


class BrainModuleProtocol(Protocol):
    """Protocol defining brain module interface"""

    def initialize(self, config: Dict[str, Any]) -> None: ...

    def process(self, thought_graph: 'ThoughtGraph') -> 'ThoughtGraph': ...

    def shutdown(self) -> None: ...

    @property
    def name(self) -> str: ...


class ThoughtGraph:
    """Represents the cognitive state of the system"""

    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.graph_structure = nx.Graph()

    def add_thought(self, thought: Thought) -> None:
        self.thoughts[thought.id] = thought
        if thought.parent:
            self.graph_structure.add_edge(thought.parent, thought.id)

    def get_thought(self, thought_id: str) -> Optional[Thought]:
        return self.thoughts.get(thought_id)

    def get_root_thoughts(self) -> List[Thought]:
        return [t for t in self.thoughts.values() if t.parent is None]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thoughts": {id: t.to_dict() for id, t in self.thoughts.items()}
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        for thought_data in data["thoughts"].values():
            self.thoughts[thought_data["id"]] = Thought.from_dict(thought_data)
        self._rebuild_graph_structure()

    def _rebuild_graph_structure(self) -> None:
        """Rebuild the graph structure from the thoughts dictionary"""
        self.graph_structure.clear()
        for thought in self.thoughts.values():
            if thought.parent and thought.parent in self.thoughts:
                self.graph_structure.add_edge(thought.parent, thought.id)


class LLMProtocol(Protocol):
    """Protocol defining LLM interface"""

    async def generate_response(self, prompt: str, context: Dict[str, Any]) -> str: ...

    async def initialize(self, config: Dict[str, Any]) -> None: ...

    async def shutdown(self) -> None: ...


class MemoryProtocol(Protocol):
    """Protocol defining memory interface"""

    async def store(self, content: str, metadata: Dict[str, Any]) -> None: ...

    async def retrieve(self, query: str) -> List[str]: ...

    async def clear(self) -> None: ...

    async def initialize(self, config: Dict[str, Any]) -> None: ...

    async def shutdown(self) -> None: ...
