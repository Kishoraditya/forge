# =============================================================================
# forge / tests / unit / test_budget_service
# =============================================================================
# Description : Unit tests for session credit budget enforcement.
# Layer       : Infra
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest

from app.core.exceptions import BudgetExceededError
from app.db.session_repository import SessionRepository
from app.services.budget_service import BudgetService


def test_check_budget_passes_with_balance() -> None:
    """Sessions with remaining budget pass check."""
    repo = SessionRepository()
    row = repo.create("fast", 0.10, 3600)
    service = BudgetService(session_repo=repo)

    remaining = service.check_budget(row.id)

    assert remaining == 0.10


def test_decrement_reduces_budget_and_writes_ledger() -> None:
    """Inference cost decrements budget and records ledger entry."""
    repo = SessionRepository()
    row = repo.create("fast", 0.10, 3600)
    service = BudgetService(session_repo=repo)

    remaining = service.decrement_budget(row.id, 0.04)

    assert remaining == pytest.approx(0.06)
    assert service.credit_ledger_count(row.id) == 1


def test_decrement_raises_when_exhausted() -> None:
    """Overspend raises BudgetExceededError."""
    repo = SessionRepository()
    row = repo.create("fast", 0.01, 3600)
    service = BudgetService(session_repo=repo)

    with pytest.raises(BudgetExceededError):
        service.decrement_budget(row.id, 0.05)
