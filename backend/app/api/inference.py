# =============================================================================
# forge / app / api / inference
# =============================================================================
# Description : HTTP routes for direct LLM inference (chat and stream).
# Layer       : API
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.inference import InferenceRequest, InferenceResult
from app.services.inference_service import InferenceService

router = APIRouter(prefix="/api/inference", tags=["inference"])
_inference: InferenceService | None = None


def _get_inference() -> InferenceService:
    """Return lazily initialized inference service singleton."""
    global _inference  # noqa: PLW0603
    if _inference is None:
        _inference = InferenceService()
    return _inference


@router.post("/chat", response_model=InferenceResult)
async def chat_completion(request: InferenceRequest) -> InferenceResult:
    """
    Run non-streaming chat completion.

    Args:
        request: Inference request body.

    Returns:
        InferenceResult: Assistant text and token usage.
    """
    return await _get_inference().chat(request)


@router.post("/chat/stream")
async def chat_completion_stream(request: InferenceRequest) -> StreamingResponse:
    """
    Run streaming chat completion as Server-Sent Events.

    Args:
        request: Inference request body (stream flag ignored; always streams).

    Returns:
        StreamingResponse: ``text/event-stream`` SSE body.
    """
    return StreamingResponse(
        _get_inference().stream_events(request),
        media_type="text/event-stream",
    )
