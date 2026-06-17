# =============================================================================
# forge / tests / unit / test_llm_router
# =============================================================================
# Description : Unit tests for LiteLLM router retry and fallback behavior.
# Layer       : Infra
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from collections.abc import AsyncIterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from app.core.llm_router import LLMRouter, _safe_completion_cost
from app.models.inference import ChatMessage


def _response(content: str) -> Any:
    """Build mock LiteLLM response."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=3, completion_tokens=2),
    )


@pytest.mark.asyncio
async def test_safe_completion_cost_returns_zero_when_unmapped() -> None:
    """Unmapped free models return zero cost instead of raising."""
    response = _response("ok")

    with patch(
        "app.core.llm_router.litellm.completion_cost",
        side_effect=Exception("model isn't mapped yet"),
    ):
        assert _safe_completion_cost(response, "openrouter/openrouter/free") == 0.0


@pytest.mark.asyncio
async def test_complete_returns_usage_fields() -> None:
    """Successful completion returns content and token counts."""
    completion = AsyncMock(return_value=_response("ok"))
    router = LLMRouter(completion_fn=completion)
    messages = [ChatMessage(role="user", content="hi")]

    with patch("app.core.llm_router.litellm.completion_cost", return_value=0.002):
        result = await router.complete(messages, "fast")

    assert result.content == "ok"
    assert result.prompt_tokens == 3
    assert result.completion_tokens == 2
    assert result.cost_usd == 0.002
    assert "anthropic" in result.model_used


@pytest.mark.asyncio
async def test_complete_falls_back_on_failure() -> None:
    """Router tries fallback alias when primary fails all retries."""
    calls: list[str] = []

    async def flaky(*_args: Any, **_kwargs: Any) -> Any:
        model = _kwargs.get("model", "")
        calls.append(model)
        if "haiku" in model:
            raise RuntimeError("primary down")
        return _response("fallback ok")

    router = LLMRouter(completion_fn=flaky)
    messages = [ChatMessage(role="user", content="test")]

    with patch("app.core.llm_router.litellm.completion_cost", return_value=0.001):
        result = await router.complete(messages, "fast")

    assert result.content == "fallback ok"
    assert len(calls) >= 2


@pytest.mark.asyncio
async def test_stream_yields_deltas_and_final() -> None:
    """Streaming yields text deltas then a final usage tuple."""

    async def stream_fn(*_args: Any, stream: bool = False, **_kwargs: Any) -> Any:
        assert stream is True

        async def chunks() -> AsyncIterator[Any]:
            yield SimpleNamespace(
                choices=[SimpleNamespace(delta=SimpleNamespace(content="Hel"))],
            )
            yield SimpleNamespace(
                choices=[SimpleNamespace(delta=SimpleNamespace(content="lo"))],
            )

        return chunks()

    router = LLMRouter(completion_fn=stream_fn)
    messages = [ChatMessage(role="user", content="stream me")]
    deltas: list[str] = []
    final_content = ""

    async for delta, usage in router.stream(messages, "fast"):
        if delta:
            deltas.append(delta)
        if usage is not None:
            final_content = usage.content

    assert deltas == ["Hel", "lo"]
    assert final_content == "Hello"
