"""
Exceptions for DBTT Cognitive Operating System
"""


class DBTTError(Exception):
    """Base exception for DBTT"""

    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {super().__str__()}"
        return super().__str__()


class ModuleInitializationError(DBTTError):
    """Exception raised when a module fails to initialize"""

    def __init__(self, module_name: str, message: str):
        super().__init__(f"Module '{module_name}' failed to initialize: {message}", "MODULE_INIT_ERROR")


class ThoughtGraphError(DBTTError):
    """Exception raised when thought graph operations fail"""

    def __init__(self, message: str, thought_id: str = None):
        super().__init__(f"ThoughtGraph error: {message}", "THOUGHT_GRAPH_ERROR")
        self.thought_id = thought_id


class MemoryError(DBTTError):
    """Exception raised when memory operations fail"""

    def __init__(self, message: str, memory_type: str = None):
        super().__init__(f"Memory error: {message}", "MEMORY_ERROR")
        self.memory_type = memory_type


class LLMError(DBTTError):
    """Exception raised when LLM operations fail"""

    def __init__(self, message: str, model_name: str = None):
        super().__init__(f"LLM error: {message}", "LLM_ERROR")
        self.model_name = model_name
