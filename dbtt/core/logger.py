"""Central logging setup for DBTT."""

from __future__ import annotations

import logging

from dbtt.core.config import settings


def setup_logging() -> None:
    """Configure Python logging using DBTT_LOG_LEVEL."""

    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

