"""
Curiosity Brain for DBTT Cognitive Operating System
"""

from dbtt.brain.thought_generator import ThoughtGenerator
from dbtt.core.interfaces import ThoughtGraph
from dbtt.core.constants import PRIORITY_LOW
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class CuriosityBrain(ThoughtGenerator):
    """Curiosity Brain for asking questions and exploring possibilities"""

    def __init__(self):
        super().__init__("curiosity")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts to generate questions and explore possibilities"""
        app_logger.info("Processing with Curiosity Brain")

        for thought in thought_graph.thoughts.values():
            if thought.priority.value <= PRIORITY_LOW:
                question = self.generate_thought(
                    content=f"What if we tried something different with: {thought.content}?",
                    confidence=thought.confidence * 0.7,
                    source="curiosity_brain",
                    parent=thought.id,
                    metadata={"question": True}
                )
                thought_graph.add_thought(question)

        app_logger.debug(f"Curiosity Brain processed {len(thought_graph.thoughts)} thoughts")
        return thought_graph
