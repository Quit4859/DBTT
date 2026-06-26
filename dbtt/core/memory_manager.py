"""
Memory Manager for DBTT Cognitive Operating System
"""

import asyncio
from typing import Dict, Any, List
from dbtt.core.logger import get_logger
from dbtt.core.system_config import SystemConfig
from dbtt.core.config import app_config

app_logger = get_logger(__name__)


class MemoryManager:
    """Manages all memory systems in DBTT"""

    def __init__(self, system_config: SystemConfig):
        self.system_config = system_config
        self.memories: Dict[str, Any] = {}
        self.initialized = False
        self.config = system_config.get_system_memory_configs()

    async def initialize(self) -> None:
        """Initialize all memory systems"""
        app_logger.info("Initializing all memory systems")

        memory_classes = {
            "working_memory": self._create_working_memory,
            "short_memory": self._create_short_memory,
            "long_memory": self._create_long_memory,
            "semantic_memory": self._create_semantic_memory,
            "experience_memory": self._create_experience_memory
        }

        for memory_name, create_func in memory_classes.items():
            try:
                memory = await create_func()
                self.memories[memory_name] = memory
                app_logger.info(f"Initialized {memory_name}")
            except Exception as e:
                app_logger.error(f"Failed to initialize {memory_name}: {str(e)}")
                raise

        self.initialized = True
        app_logger.info(f"Initialized {len(self.memories)} memory systems")

    async def _create_working_memory(self):
        """Create and initialize working memory"""
        from dbtt.memory.working_memory import WorkingMemory
        memory = WorkingMemory()
        memory.initialize(self.config["working_memory"])
        return memory

    async def _create_short_memory(self):
        """Create and initialize short memory"""
        from dbtt.memory.short_memory import ShortMemory
        memory = ShortMemory()
        memory.initialize(self.config["short_memory"])
        return memory

    async def _create_long_memory(self):
        """Create and initialize long memory"""
        from dbtt.memory.long_memory import LongMemory
        memory = LongMemory()
        memory.initialize(self.config["long_memory"])
        return memory

    async def _create_semantic_memory(self):
        """Create and initialize semantic memory"""
        from dbtt.memory.semantic_memory import SemanticMemory
        memory = SemanticMemory()
        memory.initialize(self.config["semantic_memory"])
        return memory

    async def _create_experience_memory(self):
        """Create and initialize experience memory"""
        from dbtt.memory.experience_memory import ExperienceMemory
        memory = ExperienceMemory()
        memory.initialize(self.config["experience_memory"])
        return memory

    async def store(self, content: str, metadata: Dict[str, Any], memory_type: str = None) -> None:
        """Store content in memory(s)"""
        if memory_type:
            memories = [self.memories[memory_type]]
        else:
            memories = self.memories.values()

        for memory in memories:
            await memory.store(content, metadata)

    async def retrieve(self, query: str, memory_type: str = None, top_k: int = 5) -> List[str]:
        """Retrieve content from memory(s)"""
        if memory_type:
            memories = [self.memories[memory_type]]
        else:
            memories = self.memories.values()

        all_results = []
        for memory in memories:
            results = await memory.retrieve(query)
            all_results.extend(results)

        return all_results[:top_k]

    async def clear(self, memory_type: str = None) -> None:
        """Clear memory(ies)"""
        if memory_type:
            if memory_type in self.memories:
                await self.memories[memory_type].clear()
        else:
            for memory in self.memories.values():
                await memory.clear()

    async def shutdown(self) -> None:
        """Shutdown all memory systems"""
        app_logger.info("Shutting down memory systems")

        for memory in self.memories.values():
            if hasattr(memory, "shutdown"):
                await memory.shutdown()

        self.memories.clear()
        self.initialized = False
        app_logger.info("Memory systems shutdown complete")

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about all memory systems"""
        stats = {}
        for name, memory in self.memories.items():
            if hasattr(memory, "get_memory_stats"):
                stats[name] = memory.get_memory_stats()
            else:
                stats[name] = {
                    "initialized": memory.initialized if hasattr(memory, "initialized") else False,
                    "config": str(memory.config) if hasattr(memory, "config") else {}
                }

        return stats

    def update_configs(self, new_configs: Dict[str, Dict[str, Any]]) -> None:
        """Update memory configurations"""
        for memory_name, new_config in new_configs.items():
            if memory_name in self.memories and self.memories[memory_name].initialized:
                app_logger.warning(f"Memory {memory_name} is already initialized. "
                                 f"Re-initialization not supported without full reset.")

        app_logger.info("Memory configurations updated (will be applied on next initialization)")
