from __future__ import annotations

from dbtt.llm.prompt_builder import PromptBuilder


def test_prompt_builder_shapes() -> None:
    pb = PromptBuilder()
    system, user = pb.build(
        system_context="system", verified_thoughts=[{"id": "t1", "content": {}}], goal="g"
    )
    assert system == "system"
    assert "Goal: g" in user
    assert "Verified Thoughts" in user

