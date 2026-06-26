"""Decision Engine - Makes final decisions from verified thoughts.

Synthesizes all reasoning into a final decision or answer.
"""

from __future__ import annotations

from typing import Any

from dbtt.core.interfaces import BrainModule, ThoughtGraphProtocol
from dbtt.models.thought import Thought
from dbtt.core.logger import setup_logging

setup_logging()
import logging

logger = logging.getLogger(__name__)


class DecisionEngine(BrainModule):
    """Makes final decisions from the verified Thought Graph."""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the decision engine."""
        self._initialized = True
        logger.info("DecisionEngine initialized")

    async def process(
        self,
        ctx: dict[str, Any],
        graph: ThoughtGraphProtocol,
    ) -> dict[str, Any]:
        """Make final decision from verified thoughts."""
        nx_graph = graph.to_networkx()
        decisions = []

        # Collect all verified thoughts
        verified_thoughts = []
        for node_id, node_data in nx_graph.nodes(data=True):
            thought: Thought = node_data.get("thought")
            if thought and thought.status == "verified":
                verified_thoughts.append(thought)

        if not verified_thoughts:
            return {"decisions_made": 0, "decision": None}

        # Synthesize decision
        decision = await self._synthesize_decision(verified_thoughts)
        if decision:
            decision_thought = Thought(
                content={
                    "type": "decision",
                    "text": decision["text"],
                    "reasoning": decision["reasoning"],
                    "confidence": decision["confidence"],
                    "source": "decision_engine",
                    "supporting_thoughts": [t.id for t in verified_thoughts],
                },
                confidence=decision["confidence"],
                priority=100,
                source="decision_engine",
                status="final",
                metadata={"stage": "decision", "final": True},
            )
            await graph.add_thought(decision_thought)
            decisions.append(decision)

        return {
            "decisions_made": len(decisions),
            "decision": decisions[0] if decisions else None,
        }

    async def _synthesize_decision(self, verified_thoughts: list[Thought]) -> dict[str, Any] | None:
        """Synthesize a final decision from verified thoughts."""
        if not verified_thoughts:
            return None

        # Weight by confidence and priority
        total_weight = sum(t.confidence * (t.priority + 1) for t in verified_thoughts)
        if total_weight == 0:
            return None

        # Combine reasoning
        reasoning_parts = []
        for thought in verified_thoughts:
            weight = (thought.confidence * (thought.priority + 1)) / total_weight
            reasoning_parts.append(f"[{weight:.2f}] {thought.content.get('text', '')}")

        combined_confidence = sum(t.confidence for t in verified_thoughts) / len(verified_thoughts)

        return {
            "text": "Based on verified reasoning, the decision is: " + verified_thoughts[0].content.get("text", "proceed"),
            "reasoning": "\n".join(reasoning_parts),
            "confidence": combined_confidence,
        }

    async def shutdown(self) -> None:
        """Shutdown the decision engine."""
        self._initialized = False
        logger.info("DecisionEngine shutdown")