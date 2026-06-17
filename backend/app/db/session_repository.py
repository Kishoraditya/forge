# =============================================================================
# forge / app / db / session_repository
# =============================================================================
# Description : Session CRUD backed by in-memory store (F008 placeholder).
# Layer       : Memory
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.db.memory_store import SessionRow, get_memory_store


class SessionRepository:
    """Persistence layer for anonymous sessions."""

    def create(
        self,
        model_alias: str,
        budget_usd: float,
        ttl_seconds: int,
    ) -> SessionRow:
        """
        Insert a new session row.

        Args:
            model_alias: Default model alias for the session.
            budget_usd: Initial credit budget in USD.
            ttl_seconds: Session TTL from creation/activity.

        Returns:
            SessionRow: Newly created session.
        """
        now = datetime.now(UTC)
        session_id = uuid4()
        row = SessionRow(
            id=session_id,
            model_alias=model_alias,
            budget_remaining_usd=budget_usd,
            budget_total_usd=budget_usd,
            token_count=0,
            status="active",
            created_at=now,
            expires_at=now.replace(microsecond=0) + timedelta(seconds=ttl_seconds),
            last_activity_at=now,
        )
        get_memory_store().sessions[session_id] = row
        return row

    def get(self, session_id: UUID) -> SessionRow | None:
        """
        Fetch session by ID.

        Args:
            session_id: Session UUID.

        Returns:
            SessionRow | None: Session if found.
        """
        return get_memory_store().sessions.get(session_id)

    def save(self, row: SessionRow) -> SessionRow:
        """
        Persist session updates.

        Args:
            row: Session row to save.

        Returns:
            SessionRow: Saved session.
        """
        get_memory_store().sessions[row.id] = row
        return row

    def touch(self, session_id: UUID, ttl_seconds: int) -> SessionRow | None:
        """
        Extend session expiry on activity.

        Args:
            session_id: Session UUID.
            ttl_seconds: New TTL from now.

        Returns:
            SessionRow | None: Updated session or None if missing.
        """
        row = self.get(session_id)
        if row is None:
            return None
        now = datetime.now(UTC)
        row.last_activity_at = now
        row.expires_at = now + timedelta(seconds=ttl_seconds)
        if row.status == "expired":
            row.status = "active"
        return self.save(row)
