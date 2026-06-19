# =============================================================================
# forge / app / db / session
# =============================================================================
# Description : Async SQLAlchemy engine and session factory for Postgres.
# Layer       : Memory
# Feature     : F008 — Supabase Schema Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_async_engine() -> AsyncEngine | None:
    """
    Return the async engine when DATABASE_URL is configured.

    Returns:
        AsyncEngine | None: Engine instance or None for in-memory mode.
    """
    global _engine  # noqa: PLW0603
    settings = get_settings()
    if not settings.use_postgres or not settings.database_url:
        return None
    if _engine is None:
        _engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession] | None:
    """
    Return async session factory bound to the engine.

    Returns:
        async_sessionmaker[AsyncSession] | None: Factory or None without DB.
    """
    global _session_factory  # noqa: PLW0603
    engine = get_async_engine()
    if engine is None:
        return None
    if _session_factory is None:
        _session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return _session_factory


@asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:
    """
    Yield an async database session with commit/rollback handling.

    Yields:
        AsyncSession: Active SQLAlchemy session.

    Raises:
        RuntimeError: When DATABASE_URL is not configured.
    """
    factory = get_session_factory()
    if factory is None:
        msg = "DATABASE_URL is not configured"
        raise RuntimeError(msg)
    session = factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def reset_db_engine() -> None:
    """Clear cached engine (tests only)."""
    global _engine, _session_factory  # noqa: PLW0603
    _engine = None
    _session_factory = None
