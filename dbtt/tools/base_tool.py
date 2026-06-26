"""Tool abstraction.

DBTT tools are independent capabilities that modules can call.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Base contract for tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name."""

    @abstractmethod
    async def run(self, **kwargs: Any) -> Any:
        """Execute the tool."""

