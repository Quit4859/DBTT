from __future__ import annotations

import pytest

from dbtt.core.thought_graph import ThoughtGraph


@pytest.mark.asyncio
async def test_add_and_get_thought() -> None:
    graph = ThoughtGraph()
    tid = await graph.add_thought({"id": "t1", "content": {"a": 1}})
    thought = await graph.get_thought(tid)
    assert thought is not None
    assert thought.id == "t1"
    assert thought.content["a"] == 1

