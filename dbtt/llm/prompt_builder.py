"""Build LLM prompts from verified brain state."""

from __future__ import annotations

from typing import Any


class PromptBuilder:
    """Create structured prompts for the LLM."""

    def build(
        self,
        *,
        system_context: str,
        verified_thoughts: list[dict[str, Any]],
        goal: str,
    ) -> tuple[str, str]:

        """Return (system_prompt, user_prompt)."""

        system_prompt = system_context.strip()
        thought_text = "\n".join([str(t) for t in verified_thoughts])
        user_prompt = f"Goal: {goal}\n\nVerified Thoughts:\n{thought_text}"
        return system_prompt, user_prompt

