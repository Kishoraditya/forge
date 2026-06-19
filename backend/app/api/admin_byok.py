# =============================================================================
# forge / app / api / admin_byok
# =============================================================================
# Description : Admin BYOK key and model alias configuration routes.
# Layer       : API
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auth import require_admin
from app.db.api_key_repository import ApiKeyRepository
from app.models.admin import AdminUser
from app.models.byok import (
    KeyValidationResponse,
    ModelAlias,
    ModelAliasUpdate,
    ProviderKeyCreate,
    ProviderKeyResponse,
)
from app.services.byok_service import BYOKService
from app.services.litellm_config_service import LiteLLMConfigService

router = APIRouter(prefix="/api/admin/byok", tags=["admin-byok"])

AdminUserDep = Annotated[AdminUser, Depends(require_admin)]

_byok: BYOKService | None = None
_keys: ApiKeyRepository | None = None


def _get_byok() -> BYOKService:
    global _byok  # noqa: PLW0603
    if _byok is None:
        _byok = BYOKService()
    return _byok


def _get_keys() -> ApiKeyRepository:
    global _keys  # noqa: PLW0603
    if _keys is None:
        _keys = ApiKeyRepository()
    return _keys


@router.get("/keys", response_model=list[ProviderKeyResponse])
async def list_keys(_admin: AdminUserDep) -> list[ProviderKeyResponse]:
    """List configured provider keys (no secret values)."""
    _ = _admin
    return _get_byok().list_keys()


@router.post("/keys", response_model=ProviderKeyResponse, status_code=status.HTTP_201_CREATED)
async def store_key(
    payload: ProviderKeyCreate,
    _admin: AdminUserDep,
) -> ProviderKeyResponse:
    """Validate and store a provider API key."""
    _ = _admin
    result = await _get_byok().store_key(payload)
    LiteLLMConfigService(_get_keys()).sync_to_env()
    return result


@router.post("/keys/{provider}/validate", response_model=KeyValidationResponse)
async def validate_key(
    provider: str,
    payload: ProviderKeyCreate,
    _admin: AdminUserDep,
) -> KeyValidationResponse:
    """Validate a provider key without persisting it."""
    _ = _admin
    valid = await _get_byok().validate_provider_key(provider, payload.api_key)
    return KeyValidationResponse(valid=valid)


@router.get("/aliases", response_model=list[ModelAlias])
async def list_aliases(_admin: AdminUserDep) -> list[ModelAlias]:
    """List configured model aliases."""
    _ = _admin
    return [
        ModelAlias(
            alias=row.alias,
            provider=row.provider,
            model_name=row.model_name,
            is_default=row.is_default,
        )
        for row in _get_keys().list_aliases()
    ]


@router.put("/aliases/{alias}", response_model=ModelAlias)
async def upsert_alias(
    alias: str,
    payload: ModelAliasUpdate,
    _admin: AdminUserDep,
) -> ModelAlias:
    """Create or update a model alias mapping."""
    _ = _admin
    row = _get_keys().upsert_alias(
        alias,
        payload.provider,
        payload.model_name,
        is_default=payload.is_default,
    )
    return ModelAlias(
        alias=row.alias,
        provider=row.provider,
        model_name=row.model_name,
        is_default=row.is_default,
    )
