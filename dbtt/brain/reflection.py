"""
Reflection Engine for DBTT Cognitive Operating System
"""

from datetime import datetime
from typing import Dict, Any
from dbtt.models.thought import Thought, Priority
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class ReflectionEngine(BrainModule):
    """Reflection Engine for self-improvement and error correction"""

    def __init__(self):
        self._name = "reflection"
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the reflection engine"""
        self.config = config
        self.initialized = True
        app_logger.info(f"Initialized Reflection Engine")

    def process(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Process thoughts to find and correct mistakes"""
        app_logger.info("Processing with Reflection Engine")

        conflicts = thought_graph.find_conflicts()
        if conflicts:
            app_logger.warning(f"Found {len(conflicts)} conflicts in thought graph")
            for conflict in conflicts:
                corrected_thought = self._create_correction(conflict, thought_graph)
                thought_graph.add_thought(corrected_thought)

        thought_graph_meta = thought_graph.to_dict()
        average_confidence = thought_graph.calculate_confidence()

        if average_confidence < 0.5:
            app_logger.info("Low confidence detected, triggering re-evaluation")
            thought_graph = self._trigger_re_evaluation(thought_graph)

        app_logger.debug(f"Reflection Engine processed thought graph with {len(thought_graph.thoughts)} thoughts")
        return thought_graph

    def _create_correction(self, conflict: Dict[str, Any], thought_graph: ThoughtGraph) -> Thought:
        """Create a corrected version of a conflicting thought"""
        from brain.thought_generator import ThoughtGenerator

        generator = ThoughtGenerator("reflection")
        thought_id = f"{self.name}_correction_{len(str(datetime.now()))}"

        return Thought(
            id=thought_id,
            content=f"Correction: {conflict['content']} was incorrect",
            confidence=0.6,
            priority=Priority.MEDIUM,
            parent=conflict.get("id"),
            source="reflection",
            metadata={"correction": True}
        )

    def _trigger_re_evaluation(self, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Trigger re-evaluation of critical thoughts"""
        from brain.thought_generator import ThoughtGenerator

        generator = ThoughtGenerator("reflection")
        root_thoughts = thought_graph.get_root_thoughts()

        for thought in root_thoughts:
            reevaluated = generator.generate_thought(
                content=f"Re-evaluating: {thought.content}",
                confidence=0.5,
                source="reflection",
                parent=thought.id,
                metadata={"reevaluated": True}
            )
            thought_graph.add_thought(reevaluated)

        return thought_graph

    def _create_thought(self, content: str, source: str, parent: str, confidence: float) -> Thought:
        """Helper to create a thought"""
        thought_id = f"{self.name}_{len(str(datetime.now()))}"
        return Thought(
            id=thought_id,
            content=content,
            confidence=confidence,
            priority=Priority.MEDIUM,
            parent=parent,
            source=source,
            metadata={}
        )

    def shutdown(self) -> None:
        """Shutdown the reflection engine"""
        self.initialized = False
        app_logger.info(f"Shut down Reflection Engine")

    @property
    def name(self) -> str:
        return self._name
