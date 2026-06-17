# =============================================================================
# forge / app / db / memory_store
# =============================================================================
# Description : In-memory singleton store for sessions, messages, and ledger.
# Layer       : Memory
# Feature     : F008 — Supabase Schema (placeholder until persistence lands)
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class SessionRow:
    """Internal session record stored in memory."""

    id: UUID
    model_alias: str
    budget_remaining_usd: float
    budget_total_usd: float
    token_count: int
    status: str
    created_at: datetime
    expires_at: datetime
    last_activity_at: datetime


@dataclass
class MessageRow:
    """Internal message record stored in memory."""

    id: UUID
    session_id: UUID
    role: str
    content: str
    model_alias: str | None
    created_at: datetime


@dataclass
class LedgerEntry:
    """Credit ledger entry for budget tracking."""

    id: UUID
    session_id: UUID
    amount_usd: float
    reason: str
    created_at: datetime


@dataclass
class MemoryStore:
    """Process-local in-memory data store (F008 placeholder)."""

    sessions: dict[UUID, SessionRow] = field(default_factory=dict)
    messages: dict[UUID, list[MessageRow]] = field(default_factory=dict)
    ledger: list[LedgerEntry] = field(default_factory=list)
    counters: dict[str, int] = field(default_factory=dict)


_store = MemoryStore()


def get_memory_store() -> MemoryStore:
    """
    Return the singleton in-memory store.

    Returns:
        MemoryStore: Shared store instance.

    Notes:
        - Replaced by Supabase repositories in F008.
    """
    return _store


def reset_memory_store() -> None:
    """
    Clear all in-memory data (tests only).

    Notes:
        - Do not call in production request paths.
    """
    global _store  # noqa: PLW0603 — test reset requires rebinding singleton
    _store = MemoryStore()
