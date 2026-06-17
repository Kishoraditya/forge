# =============================================================================
# forge / tests / unit / test_redis_client
# =============================================================================
# Description : Unit tests for Redis client ping fallback behavior.
# Layer       : Infra
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.config import reset_settings_cache
from app.db.redis_client import InMemoryRedis, get_redis, reset_redis_client


def _set_required_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set minimum required environment variables for Settings."""
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service")
    reset_settings_cache()


@pytest.mark.asyncio
async def test_get_redis_falls_back_when_ping_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unreachable Redis falls back to in-memory client after ping failure."""
    _set_required_env(monkeypatch)
    reset_redis_client(prefer_memory=False)

    mock_client = MagicMock()
    mock_client.ping = AsyncMock(side_effect=ConnectionError("refused"))

    with patch("redis.asyncio.from_url", return_value=mock_client):
        client = await get_redis()

    assert isinstance(client, InMemoryRedis)
    await client.hset("session:test", {"status": "active"})
    assert (await client.hgetall("session:test"))["status"] == "active"
