"""Parse LLM responses."""

from __future__ import annotations


class ResponseParser:
    """Extract final text from LLM output."""

    def parse_final(self, raw: str) -> str:
        """Return cleaned final response."""

        return raw.strip()

