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
class DocumentRow:
    """Uploaded document metadata."""

    id: UUID
    filename: str
    mime_type: str
    size_bytes: int
    created_at: datetime


@dataclass
class DocumentChunkRow:
    """Document chunk with optional embedding vector."""

    id: UUID
    document_id: UUID
    content: str
    embedding: list[float] | None
    chunk_index: int


@dataclass
class ApiKeyRow:
    """Encrypted provider API key."""

    id: UUID
    provider: str
    encrypted_key: str
    is_active: bool
    last_validated_at: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass
class ModelAliasRow:
    """Model alias mapping."""

    alias: str
    provider: str
    model_name: str
    is_default: bool


@dataclass
class MemoryStore:
    """Process-local in-memory data store (F008 placeholder)."""

    sessions: dict[UUID, SessionRow] = field(default_factory=dict)
    messages: dict[UUID, list[MessageRow]] = field(default_factory=dict)
    ledger: list[LedgerEntry] = field(default_factory=list)
    documents: dict[UUID, DocumentRow] = field(default_factory=dict)
    document_chunks: dict[UUID, list[DocumentChunkRow]] = field(default_factory=dict)
    api_keys: dict[str, ApiKeyRow] = field(default_factory=dict)
    model_aliases: dict[str, ModelAliasRow] = field(default_factory=dict)
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
