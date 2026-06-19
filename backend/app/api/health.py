# =============================================================================
# forge / app / api / health
# =============================================================================
# Description : Health check endpoint for load balancers and CI.
# Layer       : API
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Return service health status.

    Returns:
        dict[str, str]: Status and environment name.

    Example:
        GET /health → {"status": "ok", "environment": "development"}
    """
    settings = get_settings()
    return {"status": "ok", "environment": settings.environment}
