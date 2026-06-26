"""Planning Brain - Creates execution plans from thoughts.

Breaks down goals into steps, creates dependency chains, estimates resources.
"""

from __future__ import annotations

from typing import Any

from dbtt.core.interfaces import BrainModule, ThoughtGraphProtocol
from dbtt.models.thought import Thought
from dbtt.core.logger import setup_logging

setup_logging()
import logging

logger = logging.getLogger(__name__)


class PlanningBrain(BrainModule):
    """Creates execution plans from validated thoughts."""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the planning brain."""
        self._initialized = True
        logger.info("PlanningBrain initialized")

    async def process(
        self,
        ctx: dict[str, Any],
        graph: ThoughtGraphProtocol,
    ) -> dict[str, Any]:
        """Create plans from validated thoughts."""
        nx_graph = graph.to_networkx()
        plans_created = 0

        for node_id, node_data in nx_graph.nodes(data=True):
            thought: Thought = node_data.get("thought")
            if not thought or thought.status != "validated":
                continue

            if thought.content.get("type") in ("understanding", "intent", "goal"):
                plan = await self._create_plan(thought, graph)
                if plan:
                    plan_thought = Thought(
                        content={
                            "type": "plan",
                            "text": f"Plan: {plan}",
                            "steps": plan,
                            "source": "planning_brain",
                        },
                        confidence=0.75,
                        priority=70,
                        parent=thought.id,
                        source="planning_brain",
                        status="new",
                        metadata={"stage": "planning"},
                    )
                    await graph.add_thought(plan_thought)
                    plans_created += 1

        return {"plans_created": plans_created}

    async def _create_plan(self, thought: Thought, graph: ThoughtGraphProtocol) -> list[str] | None:
        """Create a plan from a thought."""
        text = thought.content.get("text", "")

        # Simple plan generation based on intent
        if "understand" in text.lower() or "explain" in text.lower():
            return ["analyze_concepts", "structure_explanation", "verify_accuracy"]
        elif "solve" in text.lower() or "calculate" in text.lower():
            return ["identify_problem", "select_method", "execute", "verify_result"]
        elif "create" in text.lower() or "write" in text.lower():
            return ["gather_requirements", "draft", "review", "finalize"]
        elif "research" in text.lower() or "search" in text.lower():
            return ["formulate_query", "search_sources", "evaluate_sources", "synthesize"]

        return ["analyze", "plan", "execute", "verify"]

    async def shutdown(self) -> None:
        """Shutdown the planning brain."""
        self._initialized = False
        logger.info("PlanningBrain shutdown")