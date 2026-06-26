"""
Logic Brain for DBTT Cognitive Operating System
"""

from dbtt.brain.thought_generator import ThoughtGenerator
from dbtt.core.interfaces import ThoughtGraph
from dbtt.core.constants import PRIORITY_HIGH
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class LogicBrain(ThoughtGenerator):
    """Logic Brain for reasoning and analytical thinking"""

    def __init__(self):
        super().__init__("logic")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts with logic and reasoning"""
        app_logger.info("Processing with Logic Brain")

        for thought in thought_graph.thoughts.values():
            if thought.priority.value >= PRIORITY_HIGH:
                think = self.generate_thought(
                    content=f"Analysis: {thought.content}",
                    confidence=thought.confidence * 1.1,
                    source="logic_brain",
                    parent=thought.id,
                    metadata={"analysis": True}
                )
                thought_graph.add_thought(think)

        app_logger.debug(f"Logic Brain processed {len(thought_graph.thoughts)} thoughts")
        return thought_graph
