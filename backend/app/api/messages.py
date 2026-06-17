# =============================================================================
# forge / app / api / messages
# =============================================================================
# Description : Conversation message routes with SSE streaming on send.
# Layer       : API
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.message import MessageCreateRequest, MessageRecord
from app.services.message_service import MessageService

router = APIRouter(prefix="/api/sessions/{session_id}/messages", tags=["messages"])
_messages: MessageService | None = None


def _get_messages() -> MessageService:
    """Return lazily initialized message service singleton."""
    global _messages  # noqa: PLW0603
    if _messages is None:
        _messages = MessageService()
    return _messages


@router.get("", response_model=list[MessageRecord])
async def list_messages(session_id: UUID) -> list[MessageRecord]:
    """
    List all messages for a session.

    Args:
        session_id: Session UUID path parameter.

    Returns:
        list[MessageRecord]: Conversation history.
    """
    return await _get_messages().list_messages(session_id)


@router.post("")
async def send_message(session_id: UUID, body: MessageCreateRequest) -> StreamingResponse:
    """
    Send a user message and stream the assistant reply via SSE.

    Args:
        session_id: Session UUID path parameter.
        body: User message content.

    Returns:
        StreamingResponse: ``text/event-stream`` SSE body.
    """
    return StreamingResponse(
        _get_messages().send_message_stream(session_id, body.content),
        media_type="text/event-stream",
    )


@router.delete("")
async def clear_messages(session_id: UUID) -> dict[str, int]:
    """
    Clear all messages for a session.

    Args:
        session_id: Session UUID path parameter.

    Returns:
        dict[str, int]: Count of removed messages.
    """
    removed = await _get_messages().clear_messages(session_id)
    return {"removed": removed}


@router.post("/regenerate")
async def regenerate_message(session_id: UUID) -> StreamingResponse:
    """
    Regenerate the last assistant response.

    Args:
        session_id: Session UUID path parameter.

    Returns:
        StreamingResponse: ``text/event-stream`` SSE body.
    """
    return StreamingResponse(
        _get_messages().regenerate_last_stream(session_id),
        media_type="text/event-stream",
    )
