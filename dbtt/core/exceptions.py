"""DBTT exceptions."""

from __future__ import annotations


class DBTTError(Exception):
    """Base error for DBTT."""


class ValidationError(DBTTError):
    """Raised when a module or input fails validation."""


class LLMError(DBTTError):
    """Raised for LLM adapter failures."""


class ToolError(DBTTError):
    """Raised for tool execution failures."""

