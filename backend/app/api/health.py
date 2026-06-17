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

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Return service health status.

    Returns:
        dict[str, str]: Simple ok payload.

    Example:
        GET /health → {"status": "ok"}
    """
    return {"status": "ok"}
