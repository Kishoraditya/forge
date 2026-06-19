"""Core Phase 0 schema: sessions, messages, BYOK, documents, pgvector."""

from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

from app.db import orm_models  # noqa: F401
from app.db.base import Base

revision: str = "002_core_schema"
down_revision: str | None = "001_baseline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_STUB_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS personalities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS graph_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    label TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS graph_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES graph_nodes(id) ON DELETE CASCADE,
    target_id UUID REFERENCES graph_nodes(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key TEXT NOT NULL UNIQUE,
    enabled BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def upgrade() -> None:
    """Create pgvector extension and all Phase 0 tables."""
    op.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    bind = op.get_bind()
    Base.metadata.create_all(bind)
    for statement in _STUB_TABLES_SQL.strip().split(";"):
        stmt = statement.strip()
        if stmt:
            op.execute(text(stmt))


def downgrade() -> None:
    """Drop Phase 0 tables (destructive)."""
    op.execute(text("DROP TABLE IF EXISTS graph_edges CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS graph_nodes CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS decisions CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS prompts CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS personalities CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS skills CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS tools CASCADE"))
    op.execute(text("DROP TABLE IF EXISTS feature_flags CASCADE"))
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
