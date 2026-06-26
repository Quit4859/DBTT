"""
Planning Brain for DBTT Cognitive Operating System
"""

from dbtt.brain.thought_generator import ThoughtGenerator
from dbtt.core.interfaces import ThoughtGraph
from dbtt.core.constants import PRIORITY_HIGH
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class PlanningBrain(ThoughtGenerator):
    """Planning Brain for strategic planning and goal setting"""

    def __init__(self):
        super().__init__("planning")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts to generate plans and strategies"""
        app_logger.info("Processing with Planning Brain")

        for thought in thought_graph.thoughts.values():
            if thought.priority.value >= PRIORITY_HIGH:
                plan = self.generate_thought(
                    content=f"Plan: How to achieve {thought.content}",
                    confidence=thought.confidence * 0.9,
                    source="planning_brain",
                    parent=thought.id,
                    metadata={"plan": True}
                )
                thought_graph.add_thought(plan)

        app_logger.debug(f"Planning Brain processed {len(thought_graph.thoughts)} thoughts")
        return thought_graph
