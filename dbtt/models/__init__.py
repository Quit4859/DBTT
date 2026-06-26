"""
Thought models for DBTT Cognitive Operating System
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


@dataclass
class Context:
    """Represents the context of thoughts"""
    id: str
    thought_ids: List[str] = field(default_factory=list)
    user_id: str = ""
    session_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "thought_ids": self.thought_ids,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Context':
        return cls(
            id=data["id"],
            thought_ids=data.get("thought_ids", []),
            user_id=data.get("user_id", ""),
            session_id=data.get("session_id", ""),
            metadata=data.get("metadata", {})
        )


@dataclass
class MemoryEntry:
    """Represents a memory entry"""
    id: str
    content: str
    type: str
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "source": self.source,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        return cls(
            id=data["id"],
            content=data["content"],
            type=data["type"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            confidence=data.get("confidence", 0.0),
            source=data.get("source", ""),
            metadata=data.get("metadata", {})
        )


@dataclass
class Response:
    """Represents a system response"""
    id: str
    content: str
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Response':
        return cls(
            id=data["id"],
            content=data["content"],
            confidence=data.get("confidence", 0.0),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            source=data.get("source", ""),
            metadata=data.get("metadata", {})
        )


@dataclass
class GraphNode:
    """Represents a node in the thought graph"""
    id: str
    node_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    position: Optional[tuple] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "node_type": self.node_type,
            "data": self.data,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraphNode':
        return cls(
            id=data["id"],
            node_type=data["node_type"],
            data=data.get("data", {}),
            position=data.get("position")
        )


@dataclass
class GraphEdge:
    """Represents an edge in the thought graph"""
    id: str
    source_id: str
    target_id: str
    relationship: str = ""
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship,
            "weight": self.weight
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraphEdge':
        return cls(
            id=data["id"],
            source_id=data["source_id"],
            target_id=data["target_id"],
            relationship=data.get("relationship", ""),
            weight=data.get("weight", 1.0)
        )
