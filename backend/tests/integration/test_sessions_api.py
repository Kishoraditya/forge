# =============================================================================
# forge / tests / integration / test_sessions_api
# =============================================================================
# Description : Integration tests for session REST endpoints.
# Layer       : Infra
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient

from app.db.session_repository import SessionRepository


@pytest.mark.asyncio
async def test_create_and_get_session(client: AsyncClient) -> None:
    """POST /api/sessions then GET returns session status."""
    create_resp = await client.post("/api/sessions", json={})
    assert create_resp.status_code == 201
    body = create_resp.json()
    session_id = body["id"]

    get_resp = await client.get(f"/api/sessions/{session_id}")
    assert get_resp.status_code == 200
    status = get_resp.json()
    assert status["id"] == session_id
    assert status["budget_remaining_usd"] == 0.10
    assert status["status"] == "active"


@pytest.mark.asyncio
async def test_touch_session_extends_ttl(client: AsyncClient) -> None:
    """PATCH touch returns updated session status."""
    create_resp = await client.post("/api/sessions", json={"model_alias": "fast"})
    session_id = create_resp.json()["id"]

    touch_resp = await client.patch(f"/api/sessions/{session_id}/touch")

    assert touch_resp.status_code == 200
    assert touch_resp.json()["model_alias"] == "fast"


@pytest.mark.asyncio
async def test_expired_session_returns_404(client: AsyncClient) -> None:
    """Expired session GET returns 404."""
    repo = SessionRepository()
    row = repo.create("fast", 0.10, 60)
    row.expires_at = datetime.now(UTC) - timedelta(seconds=5)
    repo.save(row)

    response = await client.get(f"/api/sessions/{row.id}")

    assert response.status_code == 404
