# =============================================================================
# forge / app / models / document
# =============================================================================
# Description : Pydantic schemas for RAG documents and retrieval results.
# Layer       : API
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    """Uploaded document metadata returned by admin APIs."""

    id: UUID
    filename: str
    mime_type: str
    size_bytes: int
    created_at: datetime


class RetrievalResult(BaseModel):
    """Top-k semantic retrieval output."""

    chunks: list[str] = Field(default_factory=list)
    scores: list[float] = Field(default_factory=list)
