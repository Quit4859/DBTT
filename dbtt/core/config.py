"""
Configuration module for DBTT Cognitive Operating System
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
import json
import os
from pathlib import Path


@dataclass
class AppConfig:
    """Application configuration"""
    app_name: str = "DBTT"
    version: str = "0.1.0"
    log_level: str = "INFO"
    log_file: str = "dbtt.log"
    data_dir: str = "./data"
    max_thoughts: int = 1000
    llm_timeout: int = 30
    llm_temperature: float = 0.7
    llm_model: str = "qwen3-4b"
    ollama_url: str = "http://localhost:11434"
    enable_internet: bool = False
    enable_tools: bool = True
    max_concurrent_modules: int = 4
    module_timeout: int = 60
    enable_reflection: bool = True
    enable_debate: bool = True
    enable_verification: bool = True
    memory_ttl: int = 86400

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})

    def to_dict(self) -> Dict[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def save(self, path: str) -> None:
        """Save configuration to file"""
        config_dir = Path(path).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> 'AppConfig':
        """Load configuration from file"""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class ConfigManager:
    """Manages application configuration"""

    def __init__(self, default_path: str = "./config.json"):
        self._config_path = default_path
        self._config: AppConfig = AppConfig()

    def load(self, path: Optional[str] = None) -> AppConfig:
        """Load configuration from file"""
        config_path = path or self._config_path
        if os.path.exists(config_path):
            self._config = AppConfig.load(config_path)
        return self._config

    def save(self, path: Optional[str] = None) -> None:
        """Save current configuration"""
        config_path = path or self._config_path
        self._config.save(config_path)

    def get(self, key: str) -> Any:
        """Get configuration value"""
        return getattr(self._config, key, None)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        if hasattr(self._config, key):
            setattr(self._config, key, value)

    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary"""
        for key, value in config_dict.items():
            self.set(key, value)

    @property
    def config(self) -> AppConfig:
        return self._config


app_config = ConfigManager()
