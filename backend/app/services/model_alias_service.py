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
from app.core.exceptions import AppValidationError

_ALIAS_MAP: dict[str, str] = {
    "fast": "claude-3-5-haiku-latest",
    "smart": "claude-3-5-sonnet-latest",
    "cheap": "claude-3-5-haiku-latest",
}


def resolve_model(alias: str) -> str:
    """
    Resolve a model alias to a LiteLLM provider/model string.

    Args:
        alias: Short alias such as ``fast`` or ``smart``.

    Returns:
        str: LiteLLM model identifier (e.g. ``anthropic/claude-...``).

    Raises:
        AppValidationError: If alias is unknown or Anthropic key is missing.

    Example:
        >>> resolve_model("fast")  # doctest: +SKIP
        'anthropic/claude-3-5-haiku-latest'

    Notes:
        - Dev fallback uses ANTHROPIC_API_KEY from environment until F002 admin BYOK.
    """
    model_name = _ALIAS_MAP.get(alias)
    if model_name is None:
        msg = f"Unknown model alias: {alias}"
        raise AppValidationError(msg)
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise AppValidationError("Anthropic API key not configured")
    return f"anthropic/{model_name}"
