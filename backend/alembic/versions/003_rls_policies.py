"""RLS policies for admin-only configuration tables."""

from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

revision: str = "003_rls_policies"
down_revision: str | None = "002_core_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RLS_SQL = """
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_aliases ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS api_keys_admin_all ON api_keys;
CREATE POLICY api_keys_admin_all ON api_keys
    FOR ALL USING (auth.jwt() ->> 'email' IS NOT NULL);

DROP POLICY IF EXISTS documents_admin_all ON documents;
CREATE POLICY documents_admin_all ON documents
    FOR ALL USING (auth.jwt() ->> 'email' IS NOT NULL);

DROP POLICY IF EXISTS document_chunks_admin_all ON document_chunks;
CREATE POLICY document_chunks_admin_all ON document_chunks
    FOR ALL USING (auth.jwt() ->> 'email' IS NOT NULL);

DROP POLICY IF EXISTS model_aliases_admin_all ON model_aliases;
CREATE POLICY model_aliases_admin_all ON model_aliases
    FOR ALL USING (auth.jwt() ->> 'email' IS NOT NULL);
"""


def upgrade() -> None:
    """Enable RLS and admin policies on configuration tables."""
    for statement in _RLS_SQL.strip().split(";"):
        stmt = statement.strip()
        if stmt:
            op.execute(text(stmt))


def downgrade() -> None:
    """Disable RLS policies."""
    for table in ("api_keys", "documents", "document_chunks", "model_aliases"):
        op.execute(text(f"DROP POLICY IF EXISTS {table}_admin_all ON {table}"))
        op.execute(text(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY"))
