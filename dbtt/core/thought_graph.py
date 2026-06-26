"""Thought Graph implementation.

The Thought Graph is the single system state for DBTT.
It models branching/merging via a directed graph.
"""

from __future__ import annotations

import uuid
from typing import Any

import networkx as nx

from dbtt.core.config import settings
from dbtt.models.thought import Thought


class ThoughtGraph:
    """NetworkX-backed Thought Graph."""

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    def _check_limits(self) -> None:
        if self._graph.number_of_nodes() > settings.thought_graph_max_nodes:
            raise RuntimeError("ThoughtGraph exceeded configured node limit")

    async def add_thought(self, thought: Thought | dict[str, Any]) -> str:
        """Add a Thought node and optional parent relationship."""

        if isinstance(thought, dict):
            thought = Thought(**thought)

        if not thought.id:
            thought.id = str(uuid.uuid4())

        self._check_limits()
        self._graph.add_node(thought.id, thought=thought)

        if thought.parent:
            self._graph.add_edge(thought.parent, thought.id)

        return thought.id

    async def get_thought(self, thought_id: str) -> Thought | None:
        """Get a Thought node."""

        node = self._graph.nodes.get(thought_id)
        if not node:
            return None
        return node.get("thought")

    def to_networkx(self) -> nx.DiGraph:
        """Return the underlying graph (for debugging/inspection)."""

        return self._graph

