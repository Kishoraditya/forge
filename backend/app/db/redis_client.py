# =============================================================================
# forge / app / db / redis_client
# =============================================================================
# Description : Redis client with in-memory fallback for local dev and tests.
# Layer       : Memory
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from collections import defaultdict
from typing import Any

import structlog

from app.config import get_settings

logger = structlog.get_logger(__name__)


class InMemoryRedis:
    """Minimal Redis-like client backed by a dict (tests and offline dev)."""

    def __init__(self) -> None:
        """Initialize empty key-value and hash stores."""
        self._strings: dict[str, str] = {}
        self._hashes: dict[str, dict[str, str]] = defaultdict(dict)

    async def get(self, key: str) -> str | None:
        """
        Get a string value by key.

        Args:
            key: Redis key.

        Returns:
            str | None: Stored value or None.
        """
        return self._strings.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        """
        Set a string value (TTL ignored in memory fallback).

        Args:
            key: Redis key.
            value: String value.
            ex: Optional expiry seconds (no-op here).

        Returns:
            bool: Always True on success.
        """
        _ = ex
        self._strings[key] = value
        return True

    async def incr(self, key: str) -> int:
        """
        Increment integer counter at key.

        Args:
            key: Redis key.

        Returns:
            int: New counter value.
        """
        current = int(self._strings.get(key, "0"))
        current += 1
        self._strings[key] = str(current)
        return current

    async def hset(self, name: str, mapping: dict[str, Any]) -> int:
        """
        Set hash fields.

        Args:
            name: Hash name.
            mapping: Field/value pairs.

        Returns:
            int: Number of fields set.
        """
        for field, value in mapping.items():
            self._hashes[name][field] = str(value)
        return len(mapping)

    async def hgetall(self, name: str) -> dict[str, str]:
        """
        Get all fields from a hash.

        Args:
            name: Hash name.

        Returns:
            dict[str, str]: Field map.
        """
        return dict(self._hashes.get(name, {}))


_redis_client: InMemoryRedis | Any | None = None
_use_memory = False


async def get_redis() -> Any:
    """
    Return shared Redis client or in-memory fallback.

    Returns:
        Redis-like async client.

    Notes:
        - Falls back to InMemoryRedis when REDIS_URL is unset or connection fails.
    """
    global _redis_client, _use_memory  # noqa: PLW0603
    if _redis_client is not None:
        return _redis_client
    settings = get_settings()
    if settings.redis_url.startswith("memory://") or _use_memory:
        _redis_client = InMemoryRedis()
        return _redis_client
    try:
        import redis.asyncio as redis

        client = redis.from_url(settings.redis_url, decode_responses=True)
        await client.ping()
        _redis_client = client
        return _redis_client
    except Exception as exc:  # noqa: BLE001
        logger.warning("redis_fallback_memory", error=str(exc))
        _use_memory = True
        _redis_client = InMemoryRedis()
        return _redis_client


def reset_redis_client(*, prefer_memory: bool = True) -> None:
    """
    Reset Redis singleton (tests only).

    Args:
        prefer_memory: When True, force in-memory client on next get_redis call.

    Notes:
        - Use prefer_memory=False to exercise Redis URL + ping fallback in tests.
    """
    global _redis_client, _use_memory  # noqa: PLW0603
    _redis_client = None
    _use_memory = prefer_memory
