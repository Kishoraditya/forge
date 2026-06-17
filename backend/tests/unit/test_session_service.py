# =============================================================================
# forge / tests / unit / test_session_service
# =============================================================================
# Description : Unit tests for anonymous session create, get, and touch.
# Layer       : Infra
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime, timedelta

import pytest

from app.core.exceptions import NotFoundError
from app.db.session_repository import SessionRepository
from app.services.session_service import SessionService


@pytest.mark.asyncio
async def test_create_session_returns_defaults() -> None:
    """New session uses configured budget and model alias."""
    service = SessionService()
    created = await service.create_session()

    assert created.budget_remaining_usd == 0.10
    assert created.expires_at > datetime.now(UTC)


@pytest.mark.asyncio
async def test_get_session_returns_status() -> None:
    """Active session can be fetched by id."""
    service = SessionService()
    created = await service.create_session(model_alias="smart")

    status = await service.get_session(created.id)

    assert status.model_alias == "smart"
    assert status.status == "active"
    assert status.token_count == 0


@pytest.mark.asyncio
async def test_expired_session_raises_not_found() -> None:
    """Expired sessions are rejected with NotFoundError."""
    repo = SessionRepository()
    row = repo.create("fast", 0.10, 60)
    row.expires_at = datetime.now(UTC) - timedelta(seconds=1)
    repo.save(row)
    service = SessionService(repo=repo)

    with pytest.raises(NotFoundError):
        await service.get_session(row.id)


@pytest.mark.asyncio
async def test_touch_extends_expiry() -> None:
    """Touch updates last activity and keeps session active."""
    service = SessionService()
    created = await service.create_session()
    touched = await service.touch_session(created.id)

    assert touched.status == "active"
    assert touched.id == created.id
