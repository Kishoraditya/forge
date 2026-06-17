# =============================================================================
# forge / tests / unit / test_model_alias_service
# =============================================================================
# Description : Unit tests for model alias resolution and provider selection.
# Layer       : Infra
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest

from app.config import reset_settings_cache
from app.core.exceptions import AppValidationError
from app.services.model_alias_service import resolve_model


def _set_env(monkeypatch: pytest.MonkeyPatch, **kwargs: str | None) -> None:
    """Set minimum env vars and optional provider keys."""
    monkeypatch.setenv("REDIS_URL", "memory://local")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service")
    for key, value in kwargs.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    reset_settings_cache()


def test_resolve_model_uses_openrouter_free_models(monkeypatch: pytest.MonkeyPatch) -> None:
    """OpenRouter key selects free-tier model strings."""
    _set_env(monkeypatch, OPENROUTER_API_KEY="sk-or-test", ANTHROPIC_API_KEY=None)
    assert resolve_model("fast") == "openrouter/openrouter/free"
    assert resolve_model("smart") == "openrouter/meta-llama/llama-3.3-70b-instruct:free"


def test_resolve_model_uses_anthropic_when_no_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Anthropic is used when OpenRouter key is absent."""
    _set_env(monkeypatch, OPENROUTER_API_KEY="", ANTHROPIC_API_KEY="sk-ant-test")
    assert resolve_model("fast") == "anthropic/claude-3-5-haiku-latest"


def test_resolve_model_raises_without_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing provider keys raise validation error."""
    _set_env(monkeypatch, OPENROUTER_API_KEY="", ANTHROPIC_API_KEY="")
    with pytest.raises(AppValidationError, match="No LLM provider"):
        resolve_model("fast")
