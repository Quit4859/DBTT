"""
Base LLM class for DBTT Cognitive Operating System
"""

import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator, List
from dataclasses import dataclass
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM generation"""
    content: str
    model: str
    tokens_used: int
    response_time: float
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseLLM(ABC):
    """Base class for all LLM implementations"""

    def __init__(self, name: str):
        self._name = name
        self.initialized = False
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the LLM with configuration"""
        self.config = config
        self.initialized = True
        app_logger.info(f"Initialized LLM: {self.name}")

    @abstractmethod
    async def generate_response(
        self, prompt: str, context: Dict[str, Any]
    ) -> LLMResponse:
        """Generate a response from the LLM"""
        pass

    async def generate_stream(
        self, prompt: str, context: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the LLM"""
        response = await self.generate_response(prompt, context)
        yield response.content

    def get_available_models(self) -> List[str]:
        """Get available models for this LLM"""
        return []

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        return {}

    def shutdown(self) -> None:
        """Shutdown the LLM"""
        self.initialized = False
        app_logger.info(f"Shut down LLM: {self.name}")

    @property
    def name(self) -> str:
        return self._name

    async def health_check(self) -> bool:
        """Check if the LLM is healthy and responsive"""
        try:
            test_response = await self.generate_response(
                "Hello, please respond with 'OK'", {}
            )
            return "OK" in test_response.content
        except Exception as e:
            app_logger.error(f"LLM health check failed: {str(e)}")
            return False
