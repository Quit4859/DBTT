"""FastAPI server for DBTT."""

from __future__ import annotations

from fastapi import FastAPI

from dbtt.api.routes import router
from dbtt.core.logger import setup_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""

    setup_logging()
    app = FastAPI(title="DBTT", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()

