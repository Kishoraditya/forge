# =============================================================================
# forge / app / main
# =============================================================================
# Description : FastAPI application factory with middleware and routers.
# Layer       : API
# Feature     : F003 — LLM Routing & Inference Core
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin_auth, health, inference, messages, sessions
from app.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.llm_credentials import configure_litellm_runtime, sync_provider_keys_to_env
from app.core.logging import configure_logging
from app.core.middleware import CorrelationIdMiddleware


def create_app() -> FastAPI:
    """
    Build and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.

    Notes:
        - Registers CORS, correlation middleware, routers, and error handlers.
        - See: specs/phase-0/F003-llm-routing.spec.md
    """
    configure_logging()
    configure_litellm_runtime()
    settings = get_settings()
    sync_provider_keys_to_env(settings)
    app = FastAPI(title="Forge", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationIdMiddleware)
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(admin_auth.router)
    app.include_router(inference.router)
    app.include_router(sessions.router)
    app.include_router(messages.router)
    return app


app = create_app()
