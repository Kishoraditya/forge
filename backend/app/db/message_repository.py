# =============================================================================
# forge / app / db / message_repository
# =============================================================================
# Description : Message CRUD backed by in-memory store (F008 placeholder).
# Layer       : Memory
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.db.memory_store import MessageRow, get_memory_store


class MessageRepository:
    """Persistence layer for conversation messages."""

    def list_for_session(self, session_id: UUID) -> list[MessageRow]:
        """
        List messages for a session ordered by creation time.

        Args:
            session_id: Owning session UUID.

        Returns:
            list[MessageRow]: Messages oldest-first.
        """
        rows = get_memory_store().messages.get(session_id, [])
        return sorted(rows, key=lambda m: m.created_at)

    def append(
        self,
        session_id: UUID,
        role: str,
        content: str,
        model_alias: str | None = None,
    ) -> MessageRow:
        """
        Append a message to a session.

        Args:
            session_id: Owning session UUID.
            role: Message role.
            content: Message text.
            model_alias: Optional model used for assistant messages.

        Returns:
            MessageRow: Created message.
        """
        row = MessageRow(
            id=uuid4(),
            session_id=session_id,
            role=role,
            content=content,
            model_alias=model_alias,
            created_at=datetime.now(UTC),
        )
        store = get_memory_store()
        store.messages.setdefault(session_id, []).append(row)
        return row

    def clear_session(self, session_id: UUID) -> int:
        """
        Remove all messages for a session.

        Args:
            session_id: Session UUID.

        Returns:
            int: Number of messages removed.
        """
        store = get_memory_store()
        count = len(store.messages.get(session_id, []))
        store.messages[session_id] = []
        return count

    def remove_last_assistant(self, session_id: UUID) -> MessageRow | None:
        """
        Remove the last assistant message if present.

        Args:
            session_id: Session UUID.

        Returns:
            MessageRow | None: Removed message or None.
        """
        rows = self.list_for_session(session_id)
        for idx in range(len(rows) - 1, -1, -1):
            if rows[idx].role == "assistant":
                removed = rows[idx]
                store = get_memory_store()
                store.messages[session_id] = [r for r in rows if r.id != removed.id]
                return removed
        return None
