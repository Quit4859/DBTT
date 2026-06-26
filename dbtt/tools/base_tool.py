"""
Base Tool class for DBTT Cognitive Operating System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class ToolResult:
    """Result of a tool execution"""

    def __init__(self, success: bool, result: Any = None, error: str = None,
                 execution_time: float = None, metadata: Dict[str, Any] = None):
        self.success = success
        self.result = result
        self.error = error
        self.execution_time = execution_time
        self.metadata = metadata or {}


class BaseTool:
    """Abstract base class for all tools"""

    def __init__(self, name: str):
        self._name = name
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any] = None) -> None:
        """Initialize the tool with configuration"""
        if config:
            self.config.update(config)
        app_logger.info(f"Initialized tool: {self.name}")

    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        """Execute the tool with given parameters"""
        pass

    def shutdown(self) -> None:
        """Shutdown the tool"""
        app_logger.info(f"Shut down tool: {self.name}")

    @property
    def name(self) -> str:
        return self._name

    def get_tool_info(self) -> Dict[str, Any]:
        """Get information about the tool"""
        return {
            "name": self.name,
            "description": self.__doc__,
            "config_schema": self._get_config_schema()
        }

    def _get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for the tool"""
        return {}
