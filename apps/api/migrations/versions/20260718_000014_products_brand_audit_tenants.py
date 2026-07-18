"""Add missing product columns (brand_id, image_url) and create audit_logs + tenants tables

Revision ID: 20260718_000014
Revises: 20260718_000013
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "20260718_000014"
down_revision = "20260718_000013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # products — add brand_id FK and image_url
    op.add_column("products", sa.Column("brand_id", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("image_url", sa.String(length=500), nullable=True))
    op.create_foreign_key(
        "fk_products_brand_id",
        "products", "brands",
        ["brand_id"], ["id"],
    )
    op.create_index(op.f("ix_products_brand_id"), "products", ["brand_id"], unique=False)

    # tenants table (model exists but table was missing)
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tenants_id"), "tenants", ["id"], unique=False)
    op.create_index(op.f("ix_tenants_slug"), "tenants", ["slug"], unique=True)

    # audit_logs table (model exists but table was missing)
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("event", sa.String(length=100), nullable=False),
        sa.Column("user_email", sa.String(length=255), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_entity_type"), "audit_logs", ["entity_type"], unique=False)
    op.create_index(op.f("ix_audit_logs_event"), "audit_logs", ["event"], unique=False)
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_index(op.f("ix_audit_logs_user_email"), "audit_logs", ["user_email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_user_email"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_event"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_type"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_id"), table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index(op.f("ix_tenants_slug"), table_name="tenants")
    op.drop_index(op.f("ix_tenants_id"), table_name="tenants")
    op.drop_table("tenants")

    op.drop_index(op.f("ix_products_brand_id"), table_name="products")
    op.drop_constraint("fk_products_brand_id", "products", type_="foreignkey")
    op.drop_column("products", "image_url")
    op.drop_column("products", "brand_id")
