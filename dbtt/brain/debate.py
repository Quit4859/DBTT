"""Debate Engine - Compares multiple reasoning paths and selects the strongest.

Evaluates competing arguments and discards weak reasoning paths.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dbtt.core.interfaces import BrainModule, ThoughtGraphProtocol
from dbtt.models.thought import Thought
from dbtt.core.logger import setup_logging

setup_logging()
import logging

logger = logging.getLogger(__name__)


@dataclass
class Argument:
    """A reasoning argument with supporting evidence."""

    id: str
    claim: str
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.5
    weaknesses: list[str] = field(default_factory=list)
    strength: float = 0.0


class DebateEngine(BrainModule):
    """Compares multiple reasoning paths and selects the strongest."""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the debate engine."""
        self._initialized = True
        logger.info("DebateEngine initialized")

    async def process(
        self,
        ctx: dict[str, Any],
        graph: ThoughtGraphProtocol,
    ) -> dict[str, Any]:
        """Run debate between competing reasoning paths."""
        nx_graph = graph.to_networkx()
        arguments = self._extract_arguments(nx_graph)

        if len(arguments) < 2:
            return {"debates_run": 0, "winner": None}

        # Score each argument
        for arg in arguments:
            arg.strength = self._calculate_strength(arg)

        # Find winner
        winner = max(arguments, key=lambda a: a.strength)

        # Mark loser arguments
        for arg in arguments:
            if arg.id != winner.id:
                await self._mark_weak(arg, graph)

        return {
            "debates_run": 1,
            "winner_id": winner.id,
            "winner_strength": winner.strength,
            "arguments_evaluated": len(arguments),
        }

    def _extract_arguments(self, nx_graph) -> list[Argument]:
        """Extract competing arguments from the thought graph."""
        arguments: dict[str, Argument] = {}

        for node_id, node_data in nx_graph.nodes(data=True):
            thought: Thought = node_data.get("thought")
            if not thought:
                continue

            if thought.content.get("type") in ("claim", "conclusion", "hypothesis"):
                arg_id = thought.content.get("argument_id", thought.id)
                if arg_id not in arguments:
                    arguments[arg_id] = Argument(
                        id=arg_id,
                        claim=thought.content.get("text", str(thought.content)),
                    )
                arg = arguments[arg_id]
                if thought.content.get("type") == "evidence":
                    arg.evidence.append(thought.content.get("text", ""))
                if thought.confidence > arg.confidence:
                    arg.confidence = thought.confidence

        return list(arguments.values())

    def _calculate_strength(self, arg: Argument) -> float:
        """Calculate argument strength."""
        evidence_score = min(len(arg.evidence) * 0.15, 0.6)
        confidence_score = arg.confidence * 0.4
        weakness_penalty = len(arg.weaknesses) * 0.1
        return max(0.0, evidence_score + confidence_score - weakness_penalty)

    async def _mark_weak(self, arg: Argument, graph: ThoughtGraphProtocol) -> None:
        """Mark weak arguments in the graph."""
        nx_graph = graph.to_networkx()
        for node_id, node_data in nx_graph.nodes(data=True):
            thought: Thought = node_data.get("thought")
            if not thought:
                continue
            if thought.content.get("argument_id") == arg.id:
                thought.status = "defeated"
                thought.metadata["defeated_by"] = arg.id

    async def shutdown(self) -> None:
        """Shutdown the debate engine."""
        self._initialized = False
        logger.info("DebateEngine shutdown")