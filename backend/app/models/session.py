# =============================================================================
# forge / app / models / session
# =============================================================================
# Description : Pydantic schemas for anonymous session lifecycle.
# Layer       : API
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SessionCreateResponse(BaseModel):
    """Response returned when a new session is created."""

    id: UUID
    budget_remaining_usd: float
    expires_at: datetime


class SessionStatus(BaseModel):
    """Current session state for budget and activity display."""

    id: UUID
    status: Literal["active", "expired"]
    token_count: int
    budget_remaining_usd: float
    model_alias: str


class SessionCreateRequest(BaseModel):
    """Optional overrides when creating a session."""

    model_alias: str | None = None
    credit_budget_usd: float | None = Field(default=None, gt=0)
