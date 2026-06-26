"""Thought model.

Thoughts are structured objects stored inside the Thought Graph.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from pydantic import BaseModel, Field


class Thought(BaseModel):
    """A structured thought node."""

    id: str
    parent: str | None = None
    children: list[str] = Field(default_factory=list)

    content: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    priority: int = Field(default=0)

    source: str | None = None
    status: str = Field(default="new")

    dependencies: list[str] = Field(default_factory=list)
    created_time: dt.datetime = Field(default_factory=dt.datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)

