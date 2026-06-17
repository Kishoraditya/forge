# =============================================================================
# forge / tests / unit / test_auth
# =============================================================================
# Description : Unit tests for Supabase JWT admin verification.
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

from app.config import reset_settings_cache
from app.constants import JWT_AUDIENCE_AUTHENTICATED
from app.core.auth import verify_supabase_admin_token
from app.core.exceptions import ForbiddenError, UnauthorizedError

_TEST_JWT_SIGNING_KEY = "test-jwt-secret-for-forge-tests-32bytes"  # noqa: S105
_ADMIN_EMAIL = "admin@forge.test"


def _set_auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set Supabase auth env vars for JWT tests."""
    monkeypatch.setenv("REDIS_URL", "memory://local")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", _TEST_JWT_SIGNING_KEY)
    monkeypatch.setenv("ADMIN_EMAIL", _ADMIN_EMAIL)
    reset_settings_cache()


def _make_token(
    *,
    email: str = _ADMIN_EMAIL,
    secret: str = _TEST_JWT_SIGNING_KEY,
    expired: bool = False,
    role: str | None = None,
) -> str:
    """Build a Supabase-shaped JWT for tests."""
    now = datetime.now(UTC)
    exp = now - timedelta(hours=1) if expired else now + timedelta(hours=1)
    payload: dict[str, str | int | dict[str, str]] = {
        "sub": "user-123",
        "email": email,
        "aud": JWT_AUDIENCE_AUTHENTICATED,
        "exp": int(exp.timestamp()),
    }
    if role:
        payload["app_metadata"] = {"role": role}
    return jwt.encode(payload, secret, algorithm="HS256")


def test_verify_token_returns_admin_user(monkeypatch: pytest.MonkeyPatch) -> None:
    """Valid admin JWT decodes to AdminUser."""
    _set_auth_env(monkeypatch)
    token = _make_token()
    admin = verify_supabase_admin_token(token)
    assert admin.email == _ADMIN_EMAIL
    assert admin.role == "admin"


def test_verify_token_rejects_wrong_email(monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-admin email is forbidden."""
    _set_auth_env(monkeypatch)
    token = _make_token(email="other@forge.test")
    with pytest.raises(ForbiddenError):
        verify_supabase_admin_token(token)


def test_verify_token_rejects_expired(monkeypatch: pytest.MonkeyPatch) -> None:
    """Expired JWT raises unauthorized."""
    _set_auth_env(monkeypatch)
    token = _make_token(expired=True)
    with pytest.raises(UnauthorizedError):
        verify_supabase_admin_token(token)


def test_verify_token_requires_jwt_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing JWT secret configuration raises unauthorized."""
    _set_auth_env(monkeypatch)
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "")
    reset_settings_cache()
    token = _make_token()
    with pytest.raises(UnauthorizedError, match="not configured"):
        verify_supabase_admin_token(token)
