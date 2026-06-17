# =============================================================================
# forge / tests / integration / test_health_api
# =============================================================================
# Description : Integration tests for the health check endpoint.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient) -> None:
    """GET /health returns status ok."""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
