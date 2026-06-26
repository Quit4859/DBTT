"""Configuration for DBTT.

All runtime configuration must be provided via environment variables or config files.
No model/provider names should be hardcoded in application logic.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_provider: str = Field(default="ollama", description="LLM provider backend")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama URL")
    ollama_model: str = Field(default="qwen3:4b", description="Default Ollama model name")

    sqlite_path: str = Field(default="./dbtt.sqlite", description="Path to SQLite DB")

    log_level: str = Field(default="INFO", description="Python logging level")

    thought_graph_max_nodes: int = Field(default=10000, description="Safety bound")

    model_config = SettingsConfigDict(env_prefix="DBTT_", case_sensitive=False)


settings = Settings()

