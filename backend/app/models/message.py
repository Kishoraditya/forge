# =============================================================================
# forge / app / models / message
# =============================================================================
# Description : Pydantic schemas for conversation messages.
# Layer       : API
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class MessageCreateRequest(BaseModel):
    """User message submission for a session."""

    content: str = Field(min_length=1)


class MessageRecord(BaseModel):
    """Persisted message row returned by list endpoints."""

    id: UUID
    session_id: UUID
    role: Literal["user", "assistant", "system"]
    content: str
    model_alias: str | None = None
    created_at: datetime
