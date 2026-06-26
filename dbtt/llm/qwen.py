"""
Qwen LLM implementation for DBTT Cognitive Operating System
"""

import aiohttp
import asyncio
import time
from typing import Dict, Any, Optional, AsyncGenerator
from dbtt.llm.base_llm import BaseLLM, LLMResponse
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class QwenLLM(BaseLLM):
    """Qwen LLM implementation using Ollama"""

    def __init__(self):
        super().__init__("qwen")

    async def generate_response(
        self, prompt: str, context: Dict[str, Any]
    ) -> LLMResponse:
        """Generate a response using Qwen via Ollama"""
        app_logger.debug(f"Generating Qwen response for prompt: {prompt[:100]}...")

        start_time = time.time()

        try:
            ollama_url = self.config.get("ollama_url", "http://localhost:11434")
            model = self.config.get("model", "qwen3-4b")
            timeout = self.config.get("timeout", 30)

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.get("temperature", 0.7),
                        "num_predict": self.config.get("max_tokens", 1000)
                    }
                }

                if context:
                    payload["context"] = context

                async with session.post(
                    f"{ollama_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_time = time.time() - start_time

                        llm_response = LLMResponse(
                            content=data.get("response", ""),
                            model=model,
                            tokens_used=data.get("eval_count", 0),
                            response_time=response_time,
                            metadata={
                                "prompt": prompt,
                                "context": context,
                                "model": model,
                                "response_length": len(data.get("response", ""))
                            }
                        )

                        app_logger.debug(f"Qwen response generated: {response_time:.2f}s, {llm_response.tokens_used} tokens")
                        return llm_response
                    else:
                        error_text = await response.text()
                        raise Exception(f"Qwen API error: {response.status} - {error_text}")

        except Exception as e:
            app_logger.error(f"Qwen generation failed: {str(e)}")
            raise

    def get_available_models(self) -> list:
        """Get available Qwen models from Ollama"""
        # This would normally make an API call to list models
        # For now, return a default set
        return ["qwen3-4b", "qwen2-7b", "qwen1.5-14b"]

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific Qwen model"""
        model_info_map = {
            "qwen3-4b": {
                "description": "Qwen3 4B parameter model",
                "parameters": 4,
                "context_length": 8192,
                "max_tokens": 1024,
                "supports_streaming": True
            },
            "qwen2-7b": {
                "description": "Qwen2 7B parameter model",
                "parameters": 7,
                "context_length": 8192,
                "max_tokens": 2048,
                "supports_streaming": True
            },
            "qwen1.5-14b": {
                "description": "Qwen1.5 14B parameter model",
                "parameters": 14,
                "context_length": 8192,
                "max_tokens": 4096,
                "supports_streaming": False
            }
        }

        return model_info_map.get(model_name, {})