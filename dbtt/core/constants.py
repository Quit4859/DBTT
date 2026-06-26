"""
Constants module for DBTT Cognitive Operating System
"""

# Application constants
APP_NAME = "DBTT"
VERSION = "0.1.0"

# Module names
MODULE_NAMES = [
    "logic",
    "planning",
    "creativity",
    "curiosity",
    "simulation",
    "emotion",
    "reflection",
    "debate",
    "verification",
    "decision"
]

# Thought Graph constants
MAX_THOUGHTS = 1000
THOUGHT_ID_PREFIX = "thought_"
ROOT_THOUGHT_ID = "root"

# Confidence thresholds
CONFIDENCE_HIGH = 0.8
CONFIDENCE_MEDIUM = 0.5
CONFIDENCE_LOW = 0.2

# Status constants
STATUS_ACTIVE = "active"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_PENDING = "pending"

# Priority constants
PRIORITY_LOW = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3

# Logging levels
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Memory constants
MEMORY_TTL_DEFAULT = 86400

# Tool constants
TOOL_TIMEOUT = 30

# Internet constants
SEARCH_TIMEOUT = 10

# LLM constants
LLM_TIMEOUT_DEFAULT = 30
LLM_TEMPERATURE_DEFAULT = 0.7

# Social Media Constants
GITHUB_API_BASE_URL = "https://api.github.com"
