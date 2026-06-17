# =============================================================================
# forge / tests / integration / test_admin_auth_api
# =============================================================================
# Description : Integration tests for admin authentication API.
# Layer       : Infra
# Feature     : F006 — Single Admin Authentication
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from httpx import AsyncClient

from app.constants import JWT_AUDIENCE_AUTHENTICATED

_TEST_JWT_SIGNING_KEY = "test-jwt-secret-for-forge-tests-32bytes"  # noqa: S105
_ADMIN_EMAIL = "admin@forge.test"


def _auth_header(email: str = _ADMIN_EMAIL) -> dict[str, str]:
    """Build Authorization header with a valid test JWT."""
    exp = datetime.now(UTC) + timedelta(hours=1)
    token = jwt.encode(
        {
            "sub": "user-123",
            "email": email,
            "aud": JWT_AUDIENCE_AUTHENTICATED,
            "exp": int(exp.timestamp()),
        },
        _TEST_JWT_SIGNING_KEY,
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)  # type: ignore[untyped-decorator]
def _auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Enable admin JWT verification for admin API tests."""
    monkeypatch.setenv("SUPABASE_JWT_SECRET", _TEST_JWT_SIGNING_KEY)
    monkeypatch.setenv("ADMIN_EMAIL", _ADMIN_EMAIL)
    from app.config import reset_settings_cache

    reset_settings_cache()


@pytest.mark.asyncio
async def test_admin_me_requires_auth(client: AsyncClient) -> None:
    """GET /api/admin/me without token returns 401."""
    response = await client.get("/api/admin/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_admin_me_returns_identity(client: AsyncClient) -> None:
    """Valid admin JWT returns email and role."""
    response = await client.get("/api/admin/me", headers=_auth_header())
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == _ADMIN_EMAIL
    assert body["role"] == "admin"


@pytest.mark.asyncio
async def test_admin_me_rejects_non_admin(client: AsyncClient) -> None:
    """Non-admin email returns 403."""
    response = await client.get("/api/admin/me", headers=_auth_header(email="other@forge.test"))
    assert response.status_code == 403
