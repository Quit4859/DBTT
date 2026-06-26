"""
Creativity Brain for DBTT Cognitive Operating System
"""

from dbtt.brain.thought_generator import ThoughtGenerator
from dbtt.core.interfaces import ThoughtGraph
from dbtt.core.constants import PRIORITY_MEDIUM
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class CreativityBrain(ThoughtGenerator):
    """Creativity Brain for creative thinking and innovation"""

    def __init__(self):
        super().__init__("creativity")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts to generate creative ideas"""
        app_logger.info("Processing with Creativity Brain")

        for thought in thought_graph.thoughts.values():
            if thought.priority.value >= PRIORITY_MEDIUM:
                idea = self.generate_thought(
                    content=f"Creative idea: {thought.content} could be approached differently",
                    confidence=thought.confidence * 0.8,
                    source="creativity_brain",
                    parent=thought.id,
                    metadata={"creative": True}
                )
                thought_graph.add_thought(idea)

        app_logger.debug(f"Creativity Brain processed {len(thought_graph.thoughts)} thoughts")
        return thought_graph
