# =============================================================================
# forge / app / services / session_service
# =============================================================================
# Description : Create, fetch, touch, and expire anonymous sessions.
# Layer       : Core
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime
from typing import Literal, cast
from uuid import UUID

from app.config import get_settings
from app.core.exceptions import NotFoundError
from app.db.memory_store import SessionRow
from app.db.redis_client import get_redis
from app.db.session_repository import SessionRepository
from app.models.session import SessionCreateResponse, SessionStatus


class SessionService:
    """Business logic for anonymous session lifecycle."""

    def __init__(self, repo: SessionRepository | None = None) -> None:
        """
        Initialize session service.

        Args:
            repo: Optional session repository override.
        """
        self._repo = repo or SessionRepository()

    async def create_session(
        self,
        model_alias: str | None = None,
        credit_budget_usd: float | None = None,
    ) -> SessionCreateResponse:
        """
        Create a new anonymous session with default budget and TTL.

        Args:
            model_alias: Optional model alias override.
            credit_budget_usd: Optional budget override in USD.

        Returns:
            SessionCreateResponse: New session metadata.
        """
        settings = get_settings()
        alias = model_alias or settings.default_model_alias
        budget = credit_budget_usd or settings.default_session_budget_usd
        row = self._repo.create(alias, budget, settings.session_ttl_seconds)
        redis = await get_redis()
        await redis.hset(
            f"session:{row.id}",
            {
                "budget_remaining_usd": str(row.budget_remaining_usd),
                "status": row.status,
            },
        )
        return SessionCreateResponse(
            id=row.id,
            budget_remaining_usd=row.budget_remaining_usd,
            expires_at=row.expires_at,
        )

    def _ensure_active(self, session_id: UUID) -> SessionRow:
        """
        Load session and mark expired if past TTL.

        Args:
            session_id: Session UUID.

        Returns:
            SessionRow: Active session row.

        Raises:
            NotFoundError: When session is missing or expired.
        """
        row = self._repo.get(session_id)
        if row is None:
            raise NotFoundError("Session not found")
        now = datetime.now(UTC)
        if row.expires_at < now:
            row.status = "expired"
            self._repo.save(row)
            raise NotFoundError("Session expired")
        return row

    async def get_session(self, session_id: UUID) -> SessionStatus:
        """
        Return current session status for API consumers.

        Args:
            session_id: Session UUID.

        Returns:
            SessionStatus: Budget, tokens, and alias.

        Raises:
            NotFoundError: When session is missing or expired.
        """
        row = self._ensure_active(session_id)
        return SessionStatus(
            id=row.id,
            status=cast("Literal['active', 'expired']", row.status),
            token_count=row.token_count,
            budget_remaining_usd=row.budget_remaining_usd,
            model_alias=row.model_alias,
        )

    async def touch_session(self, session_id: UUID) -> SessionStatus:
        """
        Extend session TTL on user activity.

        Args:
            session_id: Session UUID.

        Returns:
            SessionStatus: Updated session state.

        Raises:
            NotFoundError: When session is missing.
        """
        row = self._repo.get(session_id)
        if row is None:
            raise NotFoundError("Session not found")
        settings = get_settings()
        updated = self._repo.touch(session_id, settings.session_ttl_seconds)
        if updated is None:
            raise NotFoundError("Session not found")
        return await self.get_session(updated.id)

    def add_tokens(self, session_id: UUID, prompt: int, completion: int) -> None:
        """
        Increment session token counter after inference.

        Args:
            session_id: Session UUID.
            prompt: Prompt tokens used.
            completion: Completion tokens used.
        """
        row = self._repo.get(session_id)
        if row is None:
            return
        row.token_count += prompt + completion
        self._repo.save(row)
