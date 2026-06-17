# =============================================================================
# forge / app / services / inference_service
# =============================================================================
# Description : Orchestrate LLM router, rate limits, and optional budget hooks.
# Layer       : Core
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import json
from collections.abc import AsyncIterator
from uuid import UUID

from app.core.llm_router import LLMRouter
from app.models.inference import ChatMessage, InferenceRequest, InferenceResult
from app.services.budget_service import BudgetService
from app.services.rate_limit_service import RateLimitService
from app.services.session_service import SessionService


def _provider_from_model(model_used: str) -> str:
    """
    Extract provider slug from LiteLLM model string.

    Args:
        model_used: Model identifier (e.g. ``anthropic/claude-...``).

    Returns:
        str: Provider slug.
    """
    return model_used.split("/", 1)[0] if "/" in model_used else "unknown"


class InferenceService:
    """High-level inference orchestration for API and message services."""

    def __init__(
        self,
        router: LLMRouter | None = None,
        rate_limit: RateLimitService | None = None,
        budget: BudgetService | None = None,
        sessions: SessionService | None = None,
    ) -> None:
        """
        Initialize inference service with optional dependency overrides.

        Args:
            router: LLM router instance.
            rate_limit: Rate limit counter service.
            budget: Budget enforcement service.
            sessions: Session service for token accounting.
        """
        self._router = router or LLMRouter()
        self._rate_limit = rate_limit or RateLimitService()
        self._budget = budget or BudgetService()
        self._sessions = sessions or SessionService()

    async def _pre_call(self, session_id: UUID | None) -> None:
        """
        Run pre-inference checks for session budget.

        Args:
            session_id: Optional session UUID.

        Raises:
            BudgetExceededError: When session budget is exhausted.
        """
        if session_id is not None:
            self._budget.check_budget(session_id)

    async def _post_call(self, session_id: UUID | None, result: InferenceResult) -> None:
        """
        Apply post-inference accounting.

        Args:
            session_id: Optional session UUID.
            result: Inference result with usage.
        """
        provider = _provider_from_model(result.model_used)
        await self._rate_limit.increment_provider(provider)
        if session_id is not None:
            self._budget.decrement_budget(session_id, result.cost_usd)
            self._sessions.add_tokens(
                session_id,
                result.prompt_tokens,
                result.completion_tokens,
            )

    async def chat(self, request: InferenceRequest) -> InferenceResult:
        """
        Run non-streaming chat completion.

        Args:
            request: Inference request payload.

        Returns:
            InferenceResult: Assistant response and usage.
        """
        await self._pre_call(request.session_id)
        result = await self._router.complete(request.messages, request.model_alias)
        await self._post_call(request.session_id, result)
        return result

    async def stream_events(self, request: InferenceRequest) -> AsyncIterator[str]:
        """
        Yield SSE-formatted events for streaming chat.

        Args:
            request: Inference request with stream enabled.

        Yields:
            str: SSE lines ``data: {...}\\n\\n``.
        """
        await self._pre_call(request.session_id)
        final_result: InferenceResult | None = None
        async for delta, usage in self._router.stream(request.messages, request.model_alias):
            if delta:
                payload = json.dumps({"delta": delta})
                yield f"data: {payload}\n\n"
            if usage is not None:
                final_result = usage
        if final_result is not None:
            await self._post_call(request.session_id, final_result)
            usage_payload = json.dumps(
                {
                    "done": True,
                    "usage": {
                        "prompt_tokens": final_result.prompt_tokens,
                        "completion_tokens": final_result.completion_tokens,
                        "cost_usd": final_result.cost_usd,
                        "model_used": final_result.model_used,
                    },
                },
            )
            yield f"data: {usage_payload}\n\n"

    async def stream_messages(
        self,
        messages: list[ChatMessage],
        model_alias: str,
        session_id: UUID | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream SSE events for a raw message list (message service helper).

        Args:
            messages: Conversation messages.
            model_alias: Model alias to use.
            session_id: Optional session for budget hooks.

        Yields:
            str: SSE event lines.
        """
        request = InferenceRequest(
            messages=messages,
            model_alias=model_alias,
            session_id=session_id,
            stream=True,
        )
        async for event in self.stream_events(request):
            yield event
