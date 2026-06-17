# =============================================================================
# forge / app / api / sessions
# =============================================================================
# Description : HTTP routes for anonymous session lifecycle.
# Layer       : API
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from uuid import UUID

from fastapi import APIRouter, status

from app.models.session import SessionCreateRequest, SessionCreateResponse, SessionStatus
from app.services.session_service import SessionService

router = APIRouter(prefix="/api/sessions", tags=["sessions"])
_sessions: SessionService | None = None


def _get_sessions() -> SessionService:
    """Return lazily initialized session service singleton."""
    global _sessions  # noqa: PLW0603
    if _sessions is None:
        _sessions = SessionService()
    return _sessions


@router.post("", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session(body: SessionCreateRequest | None = None) -> SessionCreateResponse:
    """
    Create a new anonymous session.

    Args:
        body: Optional model alias and budget overrides.

    Returns:
        SessionCreateResponse: New session id, budget, and expiry.
    """
    payload = body or SessionCreateRequest()
    return await _get_sessions().create_session(
        model_alias=payload.model_alias,
        credit_budget_usd=payload.credit_budget_usd,
    )


@router.get("/{session_id}", response_model=SessionStatus)
async def get_session(session_id: UUID) -> SessionStatus:
    """
    Fetch session status including budget and token count.

    Args:
        session_id: Session UUID path parameter.

    Returns:
        SessionStatus: Current session state.
    """
    return await _get_sessions().get_session(session_id)


@router.patch("/{session_id}/touch", response_model=SessionStatus)
async def touch_session(session_id: UUID) -> SessionStatus:
    """
    Extend session TTL on user activity.

    Args:
        session_id: Session UUID path parameter.

    Returns:
        SessionStatus: Updated session state.
    """
    return await _get_sessions().touch_session(session_id)
