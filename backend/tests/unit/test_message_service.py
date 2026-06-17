# =============================================================================
# forge / tests / unit / test_message_service
# =============================================================================
# Description : Unit tests for message send, list, clear, and regenerate.
# Layer       : Infra
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import AppValidationError
from app.services.message_service import MessageService
from app.services.session_service import SessionService


@pytest.mark.asyncio
async def test_send_message_stream_persists_messages(mock_litellm: AsyncMock) -> None:
    """Sending a message stores user and assistant rows."""
    _ = mock_litellm
    sessions = SessionService()
    created = await sessions.create_session()
    service = MessageService()

    events: list[str] = []
    async for event in service.send_message_stream(created.id, "Hello"):
        events.append(event)

    messages = await service.list_messages(created.id)
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"
    assert any('"delta"' in e for e in events)
    assert any('"done"' in e for e in events)


@pytest.mark.asyncio
async def test_clear_messages_removes_history(mock_litellm: AsyncMock) -> None:
    """Clear removes all messages for a session."""
    _ = mock_litellm
    sessions = SessionService()
    created = await sessions.create_session()
    service = MessageService()
    async for _ in service.send_message_stream(created.id, "Hi"):
        pass

    removed = await service.clear_messages(created.id)

    assert removed == 2
    assert await service.list_messages(created.id) == []


@pytest.mark.asyncio
async def test_regenerate_replaces_last_assistant(mock_litellm: AsyncMock) -> None:
    """Regenerate removes prior assistant and streams a new one."""
    _ = mock_litellm
    sessions = SessionService()
    created = await sessions.create_session()
    service = MessageService()
    async for _ in service.send_message_stream(created.id, "Question"):
        pass

    async for _ in service.regenerate_last_stream(created.id):
        pass

    messages = await service.list_messages(created.id)
    assert len(messages) == 2
    assert messages[-1].role == "assistant"


@pytest.mark.asyncio
async def test_empty_message_raises_validation() -> None:
    """Blank user content is rejected."""
    sessions = SessionService()
    created = await sessions.create_session()
    service = MessageService()

    with pytest.raises(AppValidationError):
        async for _ in service.send_message_stream(created.id, "   "):
            pass
