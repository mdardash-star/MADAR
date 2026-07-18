"""Add missing timestamp and soft-delete columns to identity tables (roles, permissions, users)

Revision ID: 20260718_000012
Revises: 20260718_000011
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "20260718_000012"
down_revision = "20260718_000011"
branch_labels = None
depends_on = None


def _add_audit_cols(table: str) -> None:
    op.add_column(table, sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(table, sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(table, sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default="false"))
    op.add_column(table, sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.execute(f"UPDATE {table} SET created_at = NOW() WHERE created_at IS NULL")  # noqa: S608
    op.execute(f"UPDATE {table} SET is_deleted = false WHERE is_deleted IS NULL")  # noqa: S608
    op.alter_column(table, "created_at", nullable=False)
    op.alter_column(table, "is_deleted", nullable=False)


def _drop_audit_cols(table: str) -> None:
    op.drop_column(table, "deleted_at")
    op.drop_column(table, "is_deleted")
    op.drop_column(table, "updated_at")
    op.drop_column(table, "created_at")


def upgrade() -> None:
    _add_audit_cols("roles")
    _add_audit_cols("permissions")
    _add_audit_cols("users")


def downgrade() -> None:
    _drop_audit_cols("users")
    _drop_audit_cols("permissions")
    _drop_audit_cols("roles")
