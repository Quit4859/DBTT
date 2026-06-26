"""FastAPI server for DBTT."""

from __future__ import annotations

from fastapi import FastAPI

from dbtt.api.routes import router
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app_logger.info("Initializing DBTT API server")
    app = FastAPI(title="DBTT", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()

