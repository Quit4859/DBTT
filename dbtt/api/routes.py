"""API routes for DBTT."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from dbtt.core.thought_graph import ThoughtGraph

router = APIRouter()


class UserInput(BaseModel):
    """User input payload."""

    text: str


class UserOutput(BaseModel):
    """API output payload."""

    text: str
    thought_graph_nodes: int


@router.post("/v1/think", response_model=UserOutput)
async def think(payload: UserInput) -> UserOutput:
    """Submit user text to DBTT.

    This is a skeleton endpoint; the full pipeline will be implemented next.
    """

    graph = ThoughtGraph()
    # Placeholder behavior: create no thoughts yet.
    return UserOutput(text=payload.text, thought_graph_nodes=graph.to_networkx().number_of_nodes())

