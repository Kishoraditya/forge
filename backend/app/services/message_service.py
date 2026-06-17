# =============================================================================
# forge / app / services / message_service
# =============================================================================
# Description : Conversation message CRUD with inference and SSE streaming.
# Layer       : Core
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import json
from collections.abc import AsyncIterator
from typing import Literal, cast
from uuid import UUID

from app.core.exceptions import AppValidationError, NotFoundError
from app.db.memory_store import MessageRow
from app.db.message_repository import MessageRepository
from app.models.inference import ChatMessage
from app.models.message import MessageRecord
from app.services.inference_service import InferenceService
from app.services.session_service import SessionService


class MessageService:
    """Send, list, clear, and regenerate conversation messages."""

    def __init__(
        self,
        messages: MessageRepository | None = None,
        sessions: SessionService | None = None,
        inference: InferenceService | None = None,
    ) -> None:
        """
        Initialize message service.

        Args:
            messages: Message repository.
            sessions: Session service.
            inference: Inference orchestration service.
        """
        self._messages = messages or MessageRepository()
        self._sessions = sessions or SessionService()
        self._inference = inference or InferenceService()

    def _to_record(self, row: MessageRow) -> MessageRecord:
        """
        Convert internal row to API model.

        Args:
            row: MessageRow from repository.

        Returns:
            MessageRecord: Public message schema.
        """
        return MessageRecord(
            id=row.id,
            session_id=row.session_id,
            role=cast("Literal['user', 'assistant', 'system']", row.role),
            content=row.content,
            model_alias=row.model_alias,
            created_at=row.created_at,
        )

    async def list_messages(self, session_id: UUID) -> list[MessageRecord]:
        """
        List all messages for a session.

        Args:
            session_id: Session UUID.

        Returns:
            list[MessageRecord]: Ordered messages.

        Raises:
            NotFoundError: When session is missing or expired.
        """
        await self._sessions.get_session(session_id)
        return [self._to_record(r) for r in self._messages.list_for_session(session_id)]

    async def clear_messages(self, session_id: UUID) -> int:
        """
        Clear conversation history for a session.

        Args:
            session_id: Session UUID.

        Returns:
            int: Number of messages removed.

        Raises:
            NotFoundError: When session is missing or expired.
        """
        await self._sessions.get_session(session_id)
        return self._messages.clear_session(session_id)

    def _history_as_chat(self, session_id: UUID) -> list[ChatMessage]:
        """
        Build ChatMessage list from stored session messages.

        Args:
            session_id: Session UUID.

        Returns:
            list[ChatMessage]: Messages for inference.
        """
        rows = self._messages.list_for_session(session_id)
        return [
            ChatMessage(role=r.role, content=r.content)  # type: ignore[arg-type]
            for r in rows
            if r.role in ("user", "assistant", "system")
        ]

    async def send_message_stream(
        self,
        session_id: UUID,
        content: str,
    ) -> AsyncIterator[str]:
        """
        Persist user message and stream assistant reply via SSE.

        Args:
            session_id: Session UUID.
            content: User message text.

        Yields:
            str: SSE event lines.

        Raises:
            NotFoundError: When session is missing or expired.
            AppValidationError: When content is empty.
        """
        if not content.strip():
            raise AppValidationError("Message content cannot be empty")
        status = await self._sessions.get_session(session_id)
        self._messages.append(session_id, "user", content)
        history = self._history_as_chat(session_id)
        assistant_parts: list[str] = []
        async for event in self._inference.stream_messages(
            history,
            status.model_alias,
            session_id,
        ):
            yield event
            if event.startswith("data: ") and '"delta"' in event:
                payload = json.loads(event.removeprefix("data: ").strip())
                assistant_parts.append(payload.get("delta", ""))
        if assistant_parts:
            self._messages.append(
                session_id,
                "assistant",
                "".join(assistant_parts),
                status.model_alias,
            )

    async def regenerate_last_stream(self, session_id: UUID) -> AsyncIterator[str]:
        """
        Regenerate the last assistant response for a session.

        Args:
            session_id: Session UUID.

        Yields:
            str: SSE event lines.

        Raises:
            NotFoundError: When session or prior user turn is missing.
            AppValidationError: When no assistant message to replace.
        """
        status = await self._sessions.get_session(session_id)
        removed = self._messages.remove_last_assistant(session_id)
        if removed is None:
            raise AppValidationError("No assistant message to regenerate")
        history = self._history_as_chat(session_id)
        if not history or history[-1].role != "user":
            raise NotFoundError("No user message to regenerate from")
        assistant_parts: list[str] = []
        async for event in self._inference.stream_messages(
            history,
            status.model_alias,
            session_id,
        ):
            yield event
            if event.startswith("data: ") and '"delta"' in event:
                payload = json.loads(event.removeprefix("data: ").strip())
                assistant_parts.append(payload.get("delta", ""))
        if assistant_parts:
            self._messages.append(
                session_id,
                "assistant",
                "".join(assistant_parts),
                status.model_alias,
            )
