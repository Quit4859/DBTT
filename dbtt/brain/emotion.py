"""
Emotion Brain for DBTT Cognitive Operating System
"""

from dbtt.brain.thought_generator import ThoughtGenerator
from dbtt.core.interfaces import ThoughtGraph
from dbtt.core.constants import PRIORITY_MEDIUM
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class EmotionBrain(ThoughtGenerator):
    """Emotion Brain for emotional intelligence and empathy"""

    def __init__(self):
        super().__init__("emotion")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts to add emotional context and empathy"""
        app_logger.info("Processing with Emotion Brain")

        for thought in thought_graph.thoughts.values():
            if thought.priority.value >= PRIORITY_MEDIUM:
                emotional_insight = self.generate_thought(
                    content=f"From an emotional perspective: {thought.content}",
                    confidence=thought.confidence * 0.9,
                    source="emotion_brain",
                    parent=thought.id,
                    metadata={"emotional": True}
                )
                thought_graph.add_thought(emotional_insight)

        app_logger.debug(f"Emotion Brain processed {len(thought_graph.thoughts)} thoughts")
        return thought_graph
