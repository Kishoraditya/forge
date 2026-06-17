# =============================================================================
# forge / app / core / exception_handlers
# =============================================================================
# Description : FastAPI exception handlers mapping ForgeError to JSON responses.
# Layer       : Core
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.constants import CORRELATION_ID_HEADER
from app.core.exceptions import ForgeError


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global handlers for ForgeError subclasses.

    Args:
        app: FastAPI application instance.

    Notes:
        - Responses include correlation ID when available on request state.
        - See: specs/phase-0/F003-llm-routing.spec.md
    """

    @app.exception_handler(ForgeError)
    async def forge_error_handler(request: Request, exc: ForgeError) -> JSONResponse:
        """
        Convert ForgeError to a JSON error payload.

        Args:
            request: Incoming HTTP request.
            exc: Raised ForgeError subclass.

        Returns:
            JSONResponse: Error body with status and correlation ID.
        """
        correlation_id = getattr(request.state, "correlation_id", None)
        body: dict[str, str] = {"error": exc.message}
        if correlation_id:
            body["correlation_id"] = correlation_id
        headers = {CORRELATION_ID_HEADER: correlation_id} if correlation_id else None
        return JSONResponse(
            status_code=exc.status_code,
            content=body,
            headers=headers,
        )
