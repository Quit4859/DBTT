from __future__ import annotations

from dbtt.llm.prompt_builder import PromptBuilder
from dbtt.models.thought import ThoughtGraph as CompatibleThoughtGraph
from dbtt.core.interfaces import Thought, Priority
from dbtt.models import Context


def test_prompt_builder_shapes() -> None:
    pb = PromptBuilder()
    
    # Create a minimal thought graph - use the compatible one
    thought_graph = CompatibleThoughtGraph()
    
    # Add a simple thought
    thought = Thought(
        id="t1",
        content="Test thought content",
        confidence=0.9,
        priority=Priority.HIGH,
        source="test"
    )
    thought_graph.add_thought(thought)
    
    # Create a context
    context = Context(id="main_context", thought_ids=["t1"])
    
    # Build a prompt
    prompt = pb.build_prompt(thought_graph, context, additional_context={"user_query": "Test goal"})
    
    # Check the prompt contains expected sections
    assert "Current Goals and Reasoning:" in prompt
    assert "The goal is to provide a helpful" in prompt
    assert "Respond based" in prompt

