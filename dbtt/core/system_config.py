"""
System configuration for DBTT Cognitive Operating System
"""

import asyncio
from typing import Dict, Any, List
from dbtt.core.interfaces import MemoryProtocol
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class SystemConfig:
    """System configuration for DBTT"""

    def __init__(self, config_dict: Dict[str, Any]):
        self.config_dict = config_dict
        self.memory_configs: Dict[str, Dict[str, Any]] = {}
        self._initialize_memory_configs()

    def _initialize_memory_configs(self) -> None:
        """Initialize memory-specific configurations"""
        memory_defaults = {
            "working_memory": {
                "max_entries": 100,
                "ttl": 300
            },
            "short_memory": {
                "max_entries": 50,
                "ttl": 3600
            },
            "long_memory": {
                "max_entries": 200,
                "ttl": 86400
            },
            "semantic_memory": {
                "max_entries": 150,
                "ttl": 604800
            },
            "experience_memory": {
                "max_entries": 100,
                "ttl": 86400
            }
        }

        for memory_name, defaults in memory_defaults.items():
            self.memory_configs[memory_name] = {
                **defaults,
                **self.config_dict.get(memory_name, {})
            }

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config_dict.get(key, default)

    def get_memory_config(self, memory_type: str) -> Dict[str, Any]:
        """Get configuration for a specific memory type"""
        return self.memory_configs.get(memory_type, {})

    def get_all_memory_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all memory configurations"""
        return self.memory_configs

    async def update_memory_config(self, memory_type: str, new_config: Dict[str, Any]) -> None:
        """Update configuration for a specific memory type"""
        if memory_type in self.memory_configs:
            self.memory_configs[memory_type].update(new_config)
            app_logger.info(f"Updated memory configuration for {memory_type}")
        else:
            app_logger.warning(f"Memory type {memory_type} not found in configurations")

    def get_system_memory_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get system memory configurations for all memory types"""
        configs = {}
        for memory_type, memory_config in self.memory_configs.items():
            # Convert to actual config dict for memory initialization
            configs[memory_type] = {
                "max_entries": memory_config.get("max_entries", 100),
                "ttl": memory_config.get("ttl", 86400)
            }
        return configs
