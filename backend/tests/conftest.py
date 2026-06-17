# =============================================================================
# forge / tests / conftest
# =============================================================================
# Description : Shared pytest fixtures for backend API and service tests.
# Layer       : Infra
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from collections.abc import AsyncIterator, Generator
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import reset_settings_cache
from app.db.memory_store import reset_memory_store
from app.db.redis_client import reset_redis_client


def _set_required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Set minimum required environment variables for Settings.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("REDIS_URL", "memory://local")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test-password")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "test-anon-key")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-key")


def _mock_completion_response(content: str = "Hello from mock") -> Any:
    """
    Build a LiteLLM-like completion response object.

    Args:
        content: Assistant message text.

    Returns:
        Any: Object with choices and usage attributes.
    """
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
    )


async def _mock_stream_chunks(content: str = "Hi there") -> AsyncIterator[Any]:
    """
    Yield LiteLLM-like streaming chunks.

    Args:
        content: Full assistant text split into one chunk.

    Yields:
        Any: Stream chunk objects.
    """
    yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=content))])


def _reset_api_singletons() -> None:
    """Clear lazy API service singletons between tests."""
    from app.api import inference, messages, sessions

    inference._inference = None  # noqa: SLF001
    messages._messages = None  # noqa: SLF001
    sessions._sessions = None  # noqa: SLF001


@pytest.fixture(autouse=True)  # type: ignore[untyped-decorator]
def reset_stores(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """
    Reset settings, memory store, and redis before each test.

    Args:
        monkeypatch: Pytest monkeypatch fixture.

    Yields:
        None: Control returns to test body.
    """
    _set_required_env(monkeypatch)
    reset_settings_cache()
    reset_memory_store()
    reset_redis_client()
    _reset_api_singletons()
    yield
    reset_settings_cache()
    reset_memory_store()
    reset_redis_client()
    _reset_api_singletons()


@pytest.fixture(autouse=True)  # type: ignore[untyped-decorator]
def mock_litellm() -> Generator[AsyncMock, None, None]:
    """
    Patch litellm.acompletion with deterministic mock responses.

    Yields:
        AsyncMock: Patched completion callable.
    """

    async def _acompletion(*_args: Any, stream: bool = False, **_kwargs: Any) -> Any:
        if stream:
            return _mock_stream_chunks("Streamed reply")
        return _mock_completion_response("Mock reply")

    with patch("litellm.acompletion", new_callable=AsyncMock) as mocked:
        mocked.side_effect = _acompletion
        with (
            patch(
                "app.core.llm_router.litellm.acompletion",
                new_callable=AsyncMock,
                side_effect=_acompletion,
            ),
            patch("app.core.llm_router.litellm.completion_cost", return_value=0.001),
        ):
            yield mocked


@pytest.fixture  # type: ignore[untyped-decorator]
async def client(mock_litellm: AsyncMock) -> AsyncIterator[AsyncClient]:
    """
    Async HTTP test client against the Forge FastAPI app.

    Args:
        mock_litellm: Ensures LiteLLM is mocked for API tests.

    Yields:
        AsyncClient: Configured test client.
    """
    _ = mock_litellm
    from app.main import create_app

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
