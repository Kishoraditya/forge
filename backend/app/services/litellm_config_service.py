# =============================================================================
# forge / app / services / litellm_config_service
# =============================================================================
# Description : Sync stored BYOK keys and aliases into LiteLLM runtime env.
# Layer       : Core
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import os

from app.db.api_key_repository import ApiKeyRepository


class LiteLLMConfigService:
    """Apply database-stored provider credentials to process environment."""

    def __init__(self, keys: ApiKeyRepository | None = None) -> None:
        """
        Initialize config service.

        Args:
            keys: API key repository.
        """
        self._keys = keys or ApiKeyRepository()

    def sync_to_env(self) -> None:
        """
        Export active decrypted keys to LiteLLM-compatible environment variables.

        Notes:
            - Never logs decrypted key values.
            - Falls back to existing env when no DB key is stored.
        """
        env_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "google": "GOOGLE_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
        }
        for provider, env_name in env_map.items():
            decrypted = self._keys.decrypt_provider_key(provider)
            if decrypted:
                os.environ[env_name] = decrypted
