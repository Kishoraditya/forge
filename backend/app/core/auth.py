# =============================================================================
# forge / app / core / auth
# =============================================================================
# Description : Supabase JWT verification and require_admin FastAPI dependency.
# Layer       : Core
# Feature     : F006 — Single Admin Authentication
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings
from app.constants import JWT_AUDIENCE_AUTHENTICATED
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.models.admin import AdminUser

_bearer = HTTPBearer(auto_error=False)
BearerCredentialsDep = Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)]


def _extract_email(payload: dict[str, Any]) -> str | None:
    """
    Extract email from Supabase JWT payload.

    Args:
        payload: Decoded JWT claims.

    Returns:
        str | None: Email address when present.
    """
    email = payload.get("email")
    if isinstance(email, str) and email:
        return email
    user_metadata = payload.get("user_metadata")
    if isinstance(user_metadata, dict):
        meta_email = user_metadata.get("email")
        if isinstance(meta_email, str) and meta_email:
            return meta_email
    return None


def verify_supabase_admin_token(token: str) -> AdminUser:
    """
    Decode and validate a Supabase access token for single-admin access.

    Args:
        token: Bearer JWT from Supabase Auth.

    Returns:
        AdminUser: Verified admin identity.

    Raises:
        UnauthorizedError: When token is missing, invalid, or auth is not configured.
        ForbiddenError: When the user is not the configured admin account.

    Notes:
        - See specs/phase-0/F006-admin-auth.spec.md
    """
    settings = get_settings()
    if not settings.supabase_jwt_secret:
        raise UnauthorizedError("Admin authentication is not configured")
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience=JWT_AUDIENCE_AUTHENTICATED,
        )
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc

    sub = payload.get("sub")
    email = _extract_email(payload)
    if not isinstance(sub, str) or not sub or not email:
        raise UnauthorizedError("Invalid token claims")

    app_metadata = payload.get("app_metadata")
    role = app_metadata.get("role") if isinstance(app_metadata, dict) else None
    if settings.admin_email and email != settings.admin_email:
        raise ForbiddenError("Not an admin account")
    if not settings.admin_email and role != "admin":
        raise ForbiddenError("Not an admin account")

    return AdminUser(sub=sub, email=email)


async def require_admin(
    credentials: BearerCredentialsDep,
) -> AdminUser:
    """
    FastAPI dependency requiring a valid admin Supabase JWT.

    Args:
        credentials: Authorization bearer credentials.

    Returns:
        AdminUser: Authenticated admin user.

    Raises:
        UnauthorizedError: When the Authorization header is missing or invalid.
        ForbiddenError: When the user is not an admin.
    """
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("Missing authorization token")
    return verify_supabase_admin_token(credentials.credentials)
