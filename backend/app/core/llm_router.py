# =============================================================================
# forge / app / core / llm_router
# =============================================================================
# Description : LiteLLM async completion wrapper with retry and fallback.
# Layer       : Core
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any

import litellm
import structlog

from app.constants import LLM_FALLBACK_ALIASES, LLM_MAX_RETRIES, LLM_RETRY_BASE_DELAY_SECONDS
from app.models.inference import ChatMessage, InferenceResult

logger = structlog.get_logger(__name__)

CompletionFn = Callable[..., Awaitable[Any]]


def _safe_completion_cost(response: Any, model_used: str) -> float:
    """
    Return completion cost in USD, defaulting to zero when unmapped.

    Args:
        response: LiteLLM completion response.
        model_used: Resolved LiteLLM model string.

    Returns:
        float: Cost in USD (0.0 for free or unmapped models).
    """
    try:
        cost = litellm.completion_cost(completion_response=response)
        return float(cost or 0.0)
    except Exception:
        logger.debug("completion_cost_unmapped", model=model_used)
        return 0.0


def _extract_usage(response: Any, model_used: str) -> InferenceResult:
    """
    Build InferenceResult from a LiteLLM response object.

    Args:
        response: LiteLLM completion response.
        model_used: Resolved LiteLLM model string.

    Returns:
        InferenceResult: Parsed content and token usage.
    """
    content = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    cost_usd = _safe_completion_cost(response, model_used)
    return InferenceResult(
        content=content,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cost_usd=cost_usd,
        model_used=model_used,
    )


def _build_alias_chain(primary_alias: str) -> list[str]:
    """
    Build ordered fallback alias list with primary first.

    Args:
        primary_alias: Requested model alias.

    Returns:
        list[str]: Unique aliases to try in order.
    """
    chain = [primary_alias, *LLM_FALLBACK_ALIASES]
    seen: set[str] = set()
    ordered: list[str] = []
    for alias in chain:
        if alias not in seen:
            seen.add(alias)
            ordered.append(alias)
    return ordered


class LLMRouter:
    """LiteLLM router with retries, fallback, and injectable completion for tests."""

    def __init__(self, completion_fn: CompletionFn | None = None) -> None:
        """
        Initialize router with optional completion override.

        Args:
            completion_fn: Optional async completion callable (defaults to litellm).
        """
        self._completion_fn = completion_fn or litellm.acompletion

    async def complete(
        self,
        messages: list[ChatMessage],
        model_alias: str,
    ) -> InferenceResult:
        """
        Run non-streaming chat completion with retry and fallback.

        Args:
            messages: Conversation messages.
            model_alias: Primary model alias to resolve.

        Returns:
            InferenceResult: Assistant content and usage metadata.

        Raises:
            RuntimeError: When all aliases and retries are exhausted.
        """
        last_error: Exception | None = None
        payload = [m.model_dump() for m in messages]
        from app.services.model_alias_service import resolve_model

        for alias in _build_alias_chain(model_alias):
            model = resolve_model(alias)
            for attempt in range(LLM_MAX_RETRIES):
                try:
                    response = await self._completion_fn(
                        model=model,
                        messages=payload,
                        stream=False,
                    )
                    return _extract_usage(response, model)
                except Exception as exc:  # noqa: BLE001 — transient provider errors
                    last_error = exc
                    delay = LLM_RETRY_BASE_DELAY_SECONDS * (2**attempt)
                    logger.warning(
                        "llm_complete_retry",
                        alias=alias,
                        attempt=attempt + 1,
                        error=str(exc),
                    )
                    await asyncio.sleep(delay)
        msg = f"LLM completion failed after retries: {last_error}"
        raise RuntimeError(msg)

    async def stream(
        self,
        messages: list[ChatMessage],
        model_alias: str,
    ) -> AsyncIterator[tuple[str, InferenceResult | None]]:
        """
        Stream chat completion deltas; final tuple includes usage result.

        Args:
            messages: Conversation messages.
            model_alias: Primary model alias to resolve.

        Yields:
            tuple[str, InferenceResult | None]: Delta text and optional final usage.

        Raises:
            RuntimeError: When streaming fails after retries.
        """
        last_error: Exception | None = None
        payload = [m.model_dump() for m in messages]
        from app.services.model_alias_service import resolve_model

        for alias in _build_alias_chain(model_alias):
            model = resolve_model(alias)
            for attempt in range(LLM_MAX_RETRIES):
                try:
                    response = await self._completion_fn(
                        model=model,
                        messages=payload,
                        stream=True,
                    )
                    content_parts: list[str] = []
                    async for chunk in response:
                        delta = chunk.choices[0].delta.content or ""
                        if delta:
                            content_parts.append(delta)
                            yield delta, None
                    full_content = "".join(content_parts)
                    usage_result = InferenceResult(
                        content=full_content,
                        prompt_tokens=0,
                        completion_tokens=0,
                        cost_usd=0.0,
                        model_used=model,
                    )
                    yield "", usage_result
                    return
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    delay = LLM_RETRY_BASE_DELAY_SECONDS * (2**attempt)
                    logger.warning(
                        "llm_stream_retry",
                        alias=alias,
                        attempt=attempt + 1,
                        error=str(exc),
                    )
                    await asyncio.sleep(delay)
        msg = f"LLM stream failed after retries: {last_error}"
        raise RuntimeError(msg)
