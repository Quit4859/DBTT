from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from dbtt.api.server import create_app


@pytest.mark.asyncio
async def test_think_endpoint_returns_text() -> None:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/v1/think", json={"text": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "hello"



