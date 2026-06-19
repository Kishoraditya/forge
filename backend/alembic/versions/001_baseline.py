"""Baseline empty migration."""

from collections.abc import Sequence

revision: str = "001_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """No-op baseline revision."""


def downgrade() -> None:
    """No-op baseline downgrade."""
