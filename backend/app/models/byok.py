# =============================================================================
# forge / app / models / byok
# =============================================================================
# Description : Pydantic schemas for BYOK admin configuration APIs.
# Layer       : API
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import datetime

from pydantic import BaseModel, Field


class ProviderKeyCreate(BaseModel):
    """Write-only provider key payload."""

    provider: str = Field(min_length=1, max_length=64)
    api_key: str = Field(min_length=8)


class ProviderKeyResponse(BaseModel):
    """Provider key metadata without secret material."""

    provider: str
    is_active: bool
    last_validated_at: datetime | None = None


class KeyValidationResponse(BaseModel):
    """Result of a provider key validation check."""

    valid: bool


class ModelAlias(BaseModel):
    """Model alias mapping for LiteLLM routing."""

    alias: str
    provider: str
    model_name: str
    is_default: bool = False


class ModelAliasUpdate(BaseModel):
    """Update payload for a model alias."""

    provider: str = Field(min_length=1)
    model_name: str = Field(min_length=1)
    is_default: bool = False
