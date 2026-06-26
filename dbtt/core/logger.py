"""
Logging module for DBTT Cognitive Operating System
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from .config import app_config


@dataclass
class LogEntry:
    """Represents a log entry"""
    timestamp: datetime
    level: str
    module: str
    message: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Logger:
    """Centralized logging system for DBTT"""

    def __init__(self, name: str = "DBTT"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, app_config.config.log_level.upper()))
        self._setup_handlers()
        self.log_entries: list = []

    def _setup_handlers(self) -> None:
        """Setup logging handlers"""
        clear_handlers()

        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, app_config.config.log_level.upper()))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        if app_config.config.log_file:
            log_file_path = Path(app_config.config.log_file)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(getattr(logging, app_config.config.log_level.upper()))
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, module: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message"""
        mod = module or self.name
        self.logger.debug(message, extra={'metadata': metadata or {}})
        self.log_entries.append(LogEntry(datetime.now(), 'DEBUG', mod, message, metadata))

    def info(self, message: str, module: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log info message"""
        mod = module or self.name
        self.logger.info(message, extra={'metadata': metadata or {}})
        self.log_entries.append(LogEntry(datetime.now(), 'INFO', mod, message, metadata))

    def warning(self, message: str, module: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message"""
        mod = module or self.name
        self.logger.warning(message, extra={'metadata': metadata or {}})
        self.log_entries.append(LogEntry(datetime.now(), 'WARNING', mod, message, metadata))

    def error(self, message: str, module: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log error message"""
        mod = module or self.name
        self.logger.error(message, extra={'metadata': metadata or {}})
        self.log_entries.append(LogEntry(datetime.now(), 'ERROR', mod, message, metadata))

    def critical(self, message: str, module: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log critical message"""
        mod = module or self.name
        self.logger.critical(message, extra={'metadata': metadata or {}})
        self.log_entries.append(LogEntry(datetime.now(), 'CRITICAL', mod, message, metadata))

    def get_logs(self, level: Optional[str] = None, module: Optional[str] = None,
                 limit: Optional[int] = None) -> List[LogEntry]:
        """Retrieve logs with optional filters"""
        logs = self.log_entries

        if level:
            logs = [l for l in logs if l.level.upper() == level.upper()]

        if module:
            logs = [l for l in logs if l.module == module]

        if limit:
            logs = logs[-limit:]

        return logs


def clear_handlers() -> None:
    """Clear all logging handlers"""
    logger = logging.getLogger("DBTT")
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def get_logger(name: str = "DBTT") -> Logger:
    """Get a logger instance"""
    return Logger(name)


app_logger = get_logger()
