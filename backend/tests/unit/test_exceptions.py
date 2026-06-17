# =============================================================================
# forge / tests / unit / test_exceptions
# =============================================================================
# Description : Unit tests for application exception classes and HTTP mapping.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest

from app.core.exceptions import (
    AppValidationError,
    BudgetExceededError,
    ForbiddenError,
    ForgeError,
    NotFoundError,
    UnauthorizedError,
)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("exc_cls", "status_code", "default_message"),
    [
        (AppValidationError, 422, "Validation failed"),
        (NotFoundError, 404, "Resource not found"),
        (BudgetExceededError, 402, "Session budget exceeded"),
        (UnauthorizedError, 401, "Unauthorized"),
        (ForbiddenError, 403, "Forbidden"),
    ],
)
def test_exception_status_and_default_message(
    exc_cls: type[ForgeError],
    status_code: int,
    default_message: str,
) -> None:
    """Each exception exposes the HTTP status and default message from VALIDATION.md."""
    exc = exc_cls()

    assert exc.status_code == status_code
    assert exc.message == default_message
    assert str(exc) == default_message


def test_custom_message_overrides_default() -> None:
    """Callers can supply a custom error message."""
    exc = NotFoundError("Session not found")

    assert exc.message == "Session not found"
    assert exc.status_code == 404


def test_forge_error_subclass_is_caught_as_forge_error() -> None:
    """All app exceptions are catchable as ForgeError."""
    with pytest.raises(ForgeError):
        raise BudgetExceededError
