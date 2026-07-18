"""Add timestamps and soft-delete columns to companies and branches tables

Revision ID: 20260718_000011
Revises: 20260718_000010
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "20260718_000011"
down_revision = "20260718_000010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # companies — add missing columns
    op.add_column("companies", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("companies", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("companies", sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default="false"))
    op.add_column("companies", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    # backfill so NOT NULL can be enforced after the fact
    op.execute("UPDATE companies SET created_at = NOW() WHERE created_at IS NULL")
    op.execute("UPDATE companies SET is_deleted = false WHERE is_deleted IS NULL")
    op.alter_column("companies", "created_at", nullable=False)
    op.alter_column("companies", "is_deleted", nullable=False)

    # branches — add missing columns
    op.add_column("branches", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("branches", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("branches", sa.Column("is_deleted", sa.Boolean(), nullable=True, server_default="false"))
    op.add_column("branches", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.execute("UPDATE branches SET created_at = NOW() WHERE created_at IS NULL")
    op.execute("UPDATE branches SET is_deleted = false WHERE is_deleted IS NULL")
    op.alter_column("branches", "created_at", nullable=False)
    op.alter_column("branches", "is_deleted", nullable=False)


def downgrade() -> None:
    op.drop_column("branches", "deleted_at")
    op.drop_column("branches", "is_deleted")
    op.drop_column("branches", "updated_at")
    op.drop_column("branches", "created_at")

    op.drop_column("companies", "deleted_at")
    op.drop_column("companies", "is_deleted")
    op.drop_column("companies", "updated_at")
    op.drop_column("companies", "created_at")
