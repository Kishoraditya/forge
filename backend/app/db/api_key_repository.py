# =============================================================================
# forge / app / db / api_key_repository
# =============================================================================
# Description : Encrypted provider API key persistence (memory placeholder).
# Layer       : Memory
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime
from uuid import uuid4

from app.core.encryption import decrypt_secret, encrypt_secret
from app.db.memory_store import ApiKeyRow, ModelAliasRow, get_memory_store


class ApiKeyRepository:
    """Store and retrieve encrypted provider API keys."""

    def upsert_key(self, provider: str, api_key: str, *, validated: bool = False) -> ApiKeyRow:
        """
        Insert or update an encrypted provider key.

        Args:
            provider: Provider slug.
            api_key: Plaintext API key.
            validated: Whether key passed validation.

        Returns:
            ApiKeyRow: Stored key metadata.
        """
        now = datetime.now(UTC)
        encrypted = encrypt_secret(api_key)
        store = get_memory_store()
        existing = store.api_keys.get(provider)
        row = ApiKeyRow(
            id=existing.id if existing else uuid4(),
            provider=provider,
            encrypted_key=encrypted,
            is_active=True,
            last_validated_at=(
                now if validated else (existing.last_validated_at if existing else None)
            ),
            created_at=existing.created_at if existing else now,
            updated_at=now,
        )
        store.api_keys[provider] = row
        return row

    def list_keys(self) -> list[ApiKeyRow]:
        """
        List stored provider keys.

        Returns:
            list[ApiKeyRow]: Key metadata rows.
        """
        return list(get_memory_store().api_keys.values())

    def get_key(self, provider: str) -> ApiKeyRow | None:
        """
        Fetch key row by provider.

        Args:
            provider: Provider slug.

        Returns:
            ApiKeyRow | None: Row if present.
        """
        return get_memory_store().api_keys.get(provider)

    def decrypt_provider_key(self, provider: str) -> str | None:
        """
        Decrypt stored API key for a provider.

        Args:
            provider: Provider slug.

        Returns:
            str | None: Plaintext key or None.
        """
        row = self.get_key(provider)
        if row is None or not row.is_active:
            return None
        return decrypt_secret(row.encrypted_key)

    def upsert_alias(
        self,
        alias: str,
        provider: str,
        model_name: str,
        *,
        is_default: bool = False,
    ) -> ModelAliasRow:
        """
        Insert or update a model alias mapping.

        Args:
            alias: Short alias name.
            provider: Provider slug.
            model_name: Provider model identifier.
            is_default: Whether alias is default.

        Returns:
            ModelAliasRow: Stored alias row.
        """
        row = ModelAliasRow(
            alias=alias,
            provider=provider,
            model_name=model_name,
            is_default=is_default,
        )
        get_memory_store().model_aliases[alias] = row
        return row

    def list_aliases(self) -> list[ModelAliasRow]:
        """
        List configured model aliases.

        Returns:
            list[ModelAliasRow]: Alias rows.
        """
        return list(get_memory_store().model_aliases.values())

    def get_alias(self, alias: str) -> ModelAliasRow | None:
        """
        Fetch alias mapping.

        Args:
            alias: Alias name.

        Returns:
            ModelAliasRow | None: Mapping if configured.
        """
        return get_memory_store().model_aliases.get(alias)
