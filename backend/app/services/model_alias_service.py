# =============================================================================
# forge / app / services / model_alias_service
# =============================================================================
# Description : Resolve model aliases to LiteLLM model strings (F002 minimal).
# Layer       : Core
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from app.config import get_settings
from app.constants import (
    OPENROUTER_FREE_CHEAP_MODEL,
    OPENROUTER_FREE_FAST_MODEL,
    OPENROUTER_FREE_SMART_MODEL,
    OPENROUTER_PROVIDER_PREFIX,
)
from app.core.exceptions import AppValidationError

_ANTHROPIC_ALIAS_MAP: dict[str, str] = {
    "fast": "claude-3-5-haiku-latest",
    "smart": "claude-3-5-sonnet-latest",
    "cheap": "claude-3-5-haiku-latest",
}

_OPENROUTER_ALIAS_MAP: dict[str, str] = {
    "fast": OPENROUTER_FREE_FAST_MODEL,
    "cheap": OPENROUTER_FREE_CHEAP_MODEL,
    "smart": OPENROUTER_FREE_SMART_MODEL,
}

_KNOWN_ALIASES = frozenset(_ANTHROPIC_ALIAS_MAP.keys())


def resolve_model(alias: str) -> str:
    """
    Resolve a model alias to a LiteLLM provider/model string.

    Args:
        alias: Short alias such as ``fast`` or ``smart``.

    Returns:
        str: LiteLLM model identifier (e.g. ``openrouter/meta-llama/...``).

    Raises:
        AppValidationError: If alias is unknown or no provider key is configured.

    Example:
        >>> resolve_model("fast")  # doctest: +SKIP
        'openrouter/openrouter/free'

    Notes:
        - Prefers OpenRouter when OPENROUTER_API_KEY is set (free models for dev).
        - Falls back to Anthropic when only ANTHROPIC_API_KEY is configured.
    """
    if alias not in _KNOWN_ALIASES:
        msg = f"Unknown model alias: {alias}"
        raise AppValidationError(msg)

    settings = get_settings()
    if settings.openrouter_api_key:
        model_id = _OPENROUTER_ALIAS_MAP[alias]
        return f"{OPENROUTER_PROVIDER_PREFIX}/{model_id}"
    if settings.anthropic_api_key:
        return f"anthropic/{_ANTHROPIC_ALIAS_MAP[alias]}"
    raise AppValidationError(
        "No LLM provider API key configured (set OPENROUTER_API_KEY or ANTHROPIC_API_KEY)",
    )
