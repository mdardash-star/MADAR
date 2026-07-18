"""Fix roles slug uniqueness — change global unique to per-company unique constraint

Revision ID: 20260718_000013
Revises: 20260718_000012
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op

revision = "20260718_000013"
down_revision = "20260718_000012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the global unique index on slug
    op.drop_index("ix_roles_slug", table_name="roles")
    # Create a per-company unique constraint on (company_id, slug) instead
    op.create_index("uq_roles_company_slug", "roles", ["company_id", "slug"], unique=True)


def downgrade() -> None:
    op.drop_index("uq_roles_company_slug", table_name="roles")
    op.create_index("ix_roles_slug", "roles", ["slug"], unique=True)
