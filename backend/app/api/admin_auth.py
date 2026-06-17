# =============================================================================
# forge / app / api / admin_auth
# =============================================================================
# Description : Admin authentication endpoints (me/profile).
# Layer       : API
# Feature     : F006 — Single Admin Authentication
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auth import require_admin
from app.models.admin import AdminUser

router = APIRouter(prefix="/api/admin", tags=["admin"])

AdminUserDep = Annotated[AdminUser, Depends(require_admin)]


@router.get("/me", response_model=AdminUser)
async def admin_me(admin: AdminUserDep) -> AdminUser:
    """
    Return the authenticated admin identity.

    Args:
        admin: Injected admin user from JWT.

    Returns:
        AdminUser: Email and role for the current admin session.
    """
    return admin
