# =============================================================================
# forge / app / models / admin
# =============================================================================
# Description : Pydantic schemas for authenticated admin identity.
# Layer       : API
# Feature     : F006 — Single Admin Authentication
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Literal

from pydantic import BaseModel


class AdminUser(BaseModel):
    """Authenticated single-admin identity from Supabase JWT claims."""

    sub: str
    email: str
    role: Literal["admin"] = "admin"
