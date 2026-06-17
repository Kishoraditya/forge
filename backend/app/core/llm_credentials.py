# =============================================================================
# forge / app / core / llm_credentials
# =============================================================================
# Description : Sync provider API keys from Settings into os.environ for LiteLLM.
# Layer       : Core
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import logging
import os

import litellm

from app.config import Settings


def configure_litellm_runtime() -> None:
    """
    Reduce LiteLLM console noise and disable verbose provider debug logs.

    Notes:
        - Forge uses structlog for application logs.
        - LiteLLM cost warnings for unmapped free models are handled in llm_router.
    """
    litellm.suppress_debug_info = True
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)


def sync_provider_keys_to_env(settings: Settings) -> None:
    """
    Export configured provider keys to os.environ for LiteLLM.

    Args:
        settings: Validated application settings.

    Notes:
        - Values are never logged.
        - LiteLLM reads standard env vars (e.g. OPENROUTER_API_KEY).
    """
    if settings.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = settings.openrouter_api_key
    if settings.anthropic_api_key:
        os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
