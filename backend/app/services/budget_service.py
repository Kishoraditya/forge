# =============================================================================
# forge / app / services / budget_service
# =============================================================================
# Description : Session credit budget checks, decrements, and ledger entries.
# Layer       : Core
# Feature     : F004 — Session Management
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.exceptions import BudgetExceededError
from app.db.memory_store import LedgerEntry, get_memory_store
from app.db.session_repository import SessionRepository


class BudgetService:
    """Enforce per-session USD credit budgets."""

    def __init__(self, session_repo: SessionRepository | None = None) -> None:
        """
        Initialize budget service.

        Args:
            session_repo: Optional session repository override.
        """
        self._sessions = session_repo or SessionRepository()

    def check_budget(self, session_id: UUID) -> float:
        """
        Verify session has remaining budget.

        Args:
            session_id: Session UUID.

        Returns:
            float: Remaining budget in USD.

        Raises:
            BudgetExceededError: When budget is exhausted.
        """
        row = self._sessions.get(session_id)
        if row is None or row.budget_remaining_usd <= 0:
            raise BudgetExceededError
        return row.budget_remaining_usd

    def decrement_budget(
        self,
        session_id: UUID,
        cost_usd: float,
        reason: str = "inference",
    ) -> float:
        """
        Deduct inference cost and write ledger entry.

        Args:
            session_id: Session UUID.
            cost_usd: Cost to deduct in USD.
            reason: Ledger reason label.

        Returns:
            float: Remaining budget after deduction.

        Raises:
            BudgetExceededError: When deduction would exceed budget.
        """
        row = self._sessions.get(session_id)
        if row is None:
            raise BudgetExceededError("Session not found")
        if cost_usd > row.budget_remaining_usd:
            raise BudgetExceededError
        row.budget_remaining_usd = round(row.budget_remaining_usd - cost_usd, 6)
        self._sessions.save(row)
        entry = LedgerEntry(
            id=uuid4(),
            session_id=session_id,
            amount_usd=-cost_usd,
            reason=reason,
            created_at=datetime.now(UTC),
        )
        get_memory_store().ledger.append(entry)
        return row.budget_remaining_usd

    def credit_ledger_count(self, session_id: UUID) -> int:
        """
        Count ledger entries for a session.

        Args:
            session_id: Session UUID.

        Returns:
            int: Number of ledger rows.
        """
        return sum(1 for e in get_memory_store().ledger if e.session_id == session_id)
