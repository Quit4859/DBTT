"""Qwen LLM adapter (Ollama-backed).

This module is the first concrete LLM implementation, but DBTT should be able
to swap it out via configuration and adapters.
"""

from __future__ import annotations

from typing import Any

import ollama

from dbtt.core.config import settings
from dbtt.llm.base_llm import BaseLLMAdapter


class OllamaQwenAdapter(BaseLLMAdapter):
    """Ollama-backed Qwen adapter."""

    def __init__(self, *, model: str | None = None) -> None:
        self._model = model or settings.ollama_model

    async def generate(self, *, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        """Generate text by calling Ollama."""

        # ollama is synchronous; keep adapter minimal for now.
        prompt = f"{system_prompt}\n\n{user_prompt}".strip()
        resp = ollama.generate(model=self._model, prompt=prompt, **kwargs)
        return str(resp.get("response", ""))

