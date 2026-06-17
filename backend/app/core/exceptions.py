# =============================================================================
# forge / app / core / exceptions
# =============================================================================
# Description : Base application exceptions mapped to HTTP status codes.
# Layer       : Core
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import ClassVar


class ForgeError(Exception):
    """
    Base exception for all Forge application errors.

    Subclasses define ``status_code`` and ``default_message`` for API mapping.

    Args:
        message: Optional override of the default error message.

    Notes:
        - See docs/VALIDATION.md for HTTP mapping table.
        - API layer converts these to JSON responses with correlation IDs.
    """

    status_code: ClassVar[int] = 500
    default_message: ClassVar[str] = "Internal server error"

    def __init__(self, message: str | None = None) -> None:
        """
        Initialize the exception with an optional message override.

        Args:
            message: Human-readable error description.
        """
        self.message = message or self.default_message
        super().__init__(self.message)


class AppValidationError(ForgeError):
    """Business rule validation failure (HTTP 422)."""

    status_code: ClassVar[int] = 422
    default_message: ClassVar[str] = "Validation failed"


class NotFoundError(ForgeError):
    """Requested resource does not exist (HTTP 404)."""

    status_code: ClassVar[int] = 404
    default_message: ClassVar[str] = "Resource not found"


class BudgetExceededError(ForgeError):
    """Session credit budget exhausted (HTTP 402)."""

    status_code: ClassVar[int] = 402
    default_message: ClassVar[str] = "Session budget exceeded"


class UnauthorizedError(ForgeError):
    """Authentication required or invalid (HTTP 401)."""

    status_code: ClassVar[int] = 401
    default_message: ClassVar[str] = "Unauthorized"


class ForbiddenError(ForgeError):
    """Authenticated but not permitted (HTTP 403)."""

    status_code: ClassVar[int] = 403
    default_message: ClassVar[str] = "Forbidden"
