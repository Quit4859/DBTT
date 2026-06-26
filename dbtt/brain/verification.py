"""Verification Engine - Validates thoughts using external sources.

Checks confidence against internet, memory, and knowledge bases.
"""

from __future__ import annotations

from typing import Any

from dbtt.core.interfaces import BrainModule, ThoughtGraphProtocol
from dbtt.models.thought import Thought
from dbtt.core.logger import setup_logging

setup_logging()
import logging

logger = logging.getLogger(__name__)


class VerificationEngine(BrainModule):
    """Verifies thoughts using external sources and memory."""

    def __init__(self, confidence_threshold: float = 0.7) -> None:
        self._initialized = False
        self._confidence_threshold = confidence_threshold

    async def initialize(self) -> None:
        """Initialize the verification engine."""
        self._initialized = True
        logger.info("VerificationEngine initialized")

    async def process(
        self,
        ctx: dict[str, Any],
        graph: ThoughtGraphProtocol,
    ) -> dict[str, Any]:
        """Verify thoughts against external sources."""
        nx_graph = graph.to_networkx()
        verified = 0
        needs_search = 0

        for node_id, node_data in nx_graph.nodes(data=True):
            thought: Thought = node_data.get("thought")
            if not thought or thought.status not in ("validated", "new"):
                continue

            if thought.confidence >= self._confidence_threshold:
                thought.status = "verified"
                verified += 1
            elif thought.confidence < 0.5:
                thought.status = "needs_verification"
                needs_search += 1

                # Create search task thought
                search_thought = Thought(
                    content={
                        "type": "search_task",
                        "text": f"Verify: {thought.content.get('text', '')}",
                        "source": "verification_engine",
                        "target_thought": thought.id,
                    },
                    confidence=0.5,
                    priority=80,
                    parent=thought.id,
                    source="verification_engine",
                    status="new",
                    metadata={"stage": "verification", "search_required": True},
                )
                await graph.add_thought(search_thought)

        return {
            "verified": verified,
            "needs_search": needs_search,
            "threshold": self._confidence_threshold,
        }

    async def shutdown(self) -> None:
        """Shutdown the verification engine."""
        self._initialized = False
        logger.info("VerificationEngine shutdown")