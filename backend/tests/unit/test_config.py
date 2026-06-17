# =============================================================================
# forge / tests / unit / test_config
# =============================================================================
# Description : Unit tests for application settings loading and validation.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from collections.abc import Generator

import pytest
from pydantic import ValidationError

from app.config import Settings, get_settings, reset_settings_cache


@pytest.fixture(autouse=True)  # type: ignore[untyped-decorator]
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear settings cache before and after each test."""
    reset_settings_cache()
    yield
    reset_settings_cache()


def _set_required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set minimum required environment variables for Settings."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test-password")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "test-anon-key")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")


def test_settings_loads_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings loads required fields from environment variables."""
    _set_required_env(monkeypatch)

    settings = Settings(_env_file=None)

    assert settings.environment == "development"
    assert settings.debug is True
    assert settings.redis_url == "redis://localhost:6379/0"
    assert settings.supabase_url == "https://example.supabase.co"


def test_get_settings_returns_cached_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    """get_settings returns the same cached Settings instance."""
    _set_required_env(monkeypatch)

    first = get_settings()
    second = get_settings()

    assert first is second


def test_settings_raises_when_required_field_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Settings validation fails when a required field is missing."""
    monkeypatch.setenv("ENVIRONMENT", "development")
    for key in (
        "REDIS_URL",
        "NEO4J_URI",
        "NEO4J_USERNAME",
        "NEO4J_PASSWORD",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
