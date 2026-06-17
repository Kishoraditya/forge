# =============================================================================
# forge / app / core / middleware
# =============================================================================
# Description : ASGI middleware for correlation IDs on requests and responses.
# Layer       : Core
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.constants import CORRELATION_ID_HEADER


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID to each request and response."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Process request with correlation ID context.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or route handler.

        Returns:
            Response: HTTP response with correlation header.
        """
        correlation_id = request.headers.get(CORRELATION_ID_HEADER, str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers[CORRELATION_ID_HEADER] = correlation_id
        structlog.contextvars.unbind_contextvars("correlation_id")
        return response
