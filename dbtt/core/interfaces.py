"""Core interfaces.

These interfaces define the stable contracts between modules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol


class ThoughtGraphProtocol(Protocol):
    """Minimal protocol for the Thought Graph state."""

    async def add_thought(self, thought: Any) -> None:  # pragma: no cover
        """Add a Thought node."""

    async def get_thought(self, thought_id: str) -> Any | None:  # pragma: no cover
        """
        Get a Thought by id.
        """


class BrainModule(ABC):
    """Base class for all brain modules."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize module resources."""

    @abstractmethod
    async def process(self, ctx: dict[str, Any], graph: ThoughtGraphProtocol) -> dict[str, Any]:
        """Process the current context and update graph."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Release module resources."""


class BaseLLM(ABC):
    """Stable contract for LLM adapters."""

    @abstractmethod
    async def generate(self, *, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        """Generate a natural-language response."""

