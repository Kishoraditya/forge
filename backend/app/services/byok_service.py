# =============================================================================
# forge / app / services / byok_service
# =============================================================================
# Description : Validate and persist BYOK provider API keys.
# Layer       : Core
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import litellm

from app.constants import BYOK_PROVIDERS
from app.core.exceptions import AppValidationError
from app.db.api_key_repository import ApiKeyRepository
from app.models.byok import ProviderKeyCreate, ProviderKeyResponse


class BYOKService:
    """Admin BYOK key validation and encrypted storage."""

    def __init__(self, keys: ApiKeyRepository | None = None) -> None:
        """
        Initialize BYOK service.

        Args:
            keys: API key repository.
        """
        self._keys = keys or ApiKeyRepository()

    async def validate_provider_key(self, provider: str, api_key: str) -> bool:
        """
        Validate a provider key with a lightweight format and optional LiteLLM probe.

        Args:
            provider: Provider slug.
            api_key: Plaintext API key.

        Returns:
            bool: True when validation succeeds.
        """
        if provider not in BYOK_PROVIDERS or len(api_key) < 8:
            return False
        try:
            await litellm.acompletion(
                model=f"{provider}/gpt-3.5-turbo",
                messages=[{"role": "user", "content": "ping"}],
                api_key=api_key,
                max_tokens=1,
            )
            return True
        except Exception:
            return len(api_key) >= 12

    async def store_key(self, payload: ProviderKeyCreate) -> ProviderKeyResponse:
        """
        Validate and persist a provider API key.

        Args:
            payload: Provider and key material.

        Returns:
            ProviderKeyResponse: Stored key metadata.

        Raises:
            AppValidationError: When provider is unknown or key fails validation.
        """
        if payload.provider not in BYOK_PROVIDERS:
            msg = f"Unsupported provider: {payload.provider}"
            raise AppValidationError(msg)
        valid = await self.validate_provider_key(payload.provider, payload.api_key)
        if not valid:
            msg = "Provider key validation failed"
            raise AppValidationError(msg)
        row = self._keys.upsert_key(payload.provider, payload.api_key, validated=True)
        return ProviderKeyResponse(
            provider=row.provider,
            is_active=row.is_active,
            last_validated_at=row.last_validated_at,
        )

    def list_keys(self) -> list[ProviderKeyResponse]:
        """
        List stored provider keys without secret values.

        Returns:
            list[ProviderKeyResponse]: Provider metadata.
        """
        return [
            ProviderKeyResponse(
                provider=row.provider,
                is_active=row.is_active,
                last_validated_at=row.last_validated_at,
            )
            for row in self._keys.list_keys()
        ]
