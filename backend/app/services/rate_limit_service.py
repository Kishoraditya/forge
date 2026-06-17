# =============================================================================
# forge / app / services / rate_limit_service
# =============================================================================
# Description : Per-provider request counters in Redis or memory fallback.
# Layer       : Core
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from app.db.redis_client import get_redis

PROVIDER_COUNTER_PREFIX = "forge:rate:provider:"


class RateLimitService:
    """Increment and read per-provider inference counters."""

    async def increment_provider(self, provider: str) -> int:
        """
        Increment request counter for a provider.

        Args:
            provider: Provider slug (e.g. ``anthropic``).

        Returns:
            int: New counter value after increment.
        """
        redis = await get_redis()
        key = f"{PROVIDER_COUNTER_PREFIX}{provider}"
        return int(await redis.incr(key))

    async def get_provider_count(self, provider: str) -> int:
        """
        Read current provider request count.

        Args:
            provider: Provider slug.

        Returns:
            int: Current counter value (0 if unset).
        """
        redis = await get_redis()
        key = f"{PROVIDER_COUNTER_PREFIX}{provider}"
        value = await redis.get(key)
        return int(value or 0)
