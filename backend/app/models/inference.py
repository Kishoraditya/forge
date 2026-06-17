# =============================================================================
# forge / app / models / inference
# =============================================================================
# Description : Pydantic schemas for LLM inference requests and results.
# Layer       : API
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat turn for inference."""

    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class InferenceRequest(BaseModel):
    """Request body for chat completion endpoints."""

    messages: list[ChatMessage] = Field(min_length=1)
    model_alias: str = Field(default="fast")
    session_id: UUID | None = None
    stream: bool = False


class InferenceResult(BaseModel):
    """Non-streaming inference response with usage metadata."""

    content: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    model_used: str
