"""Base LLM adapter contract."""

from __future__ import annotations

from typing import Any

from dbtt.core.interfaces import BaseLLM


class BaseLLMAdapter(BaseLLM):
    """Alias/compatibility for the abstract LLM contract."""

    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        **kwargs: Any,
    ) -> str:  # pragma: no cover
        """Generate a natural-language response."""

        raise NotImplementedError


