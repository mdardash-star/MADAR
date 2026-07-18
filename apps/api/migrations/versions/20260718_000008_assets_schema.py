"""Add assets tables for MADAR ERP

Revision ID: 20260718_000008
Revises: 20260718_000007
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000008"
down_revision = "20260718_000007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fixed_assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("purchase_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cost", sa.Float(), nullable=False),
        sa.Column("depreciation_rate", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_fixed_assets_branch_id"), "fixed_assets", ["branch_id"], unique=False)
    op.create_index(op.f("ix_fixed_assets_code"), "fixed_assets", ["code"], unique=True)
    op.create_index(op.f("ix_fixed_assets_company_id"), "fixed_assets", ["company_id"], unique=False)
    op.create_index(op.f("ix_fixed_assets_id"), "fixed_assets", ["id"], unique=False)
    op.create_index(op.f("ix_fixed_assets_name"), "fixed_assets", ["name"], unique=False)
    op.create_index(op.f("ix_fixed_assets_warehouse_id"), "fixed_assets", ["warehouse_id"], unique=False)

    op.create_table(
        "asset_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("assigned_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("returned_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["asset_id"], ["fixed_assets.id"]),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_asset_assignments_asset_id"), "asset_assignments", ["asset_id"], unique=False)
    op.create_index(op.f("ix_asset_assignments_branch_id"), "asset_assignments", ["branch_id"], unique=False)
    op.create_index(op.f("ix_asset_assignments_company_id"), "asset_assignments", ["company_id"], unique=False)
    op.create_index(op.f("ix_asset_assignments_employee_id"), "asset_assignments", ["employee_id"], unique=False)
    op.create_index(op.f("ix_asset_assignments_id"), "asset_assignments", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_asset_assignments_id"), table_name="asset_assignments")
    op.drop_index(op.f("ix_asset_assignments_employee_id"), table_name="asset_assignments")
    op.drop_index(op.f("ix_asset_assignments_company_id"), table_name="asset_assignments")
    op.drop_index(op.f("ix_asset_assignments_branch_id"), table_name="asset_assignments")
    op.drop_index(op.f("ix_asset_assignments_asset_id"), table_name="asset_assignments")
    op.drop_table("asset_assignments")

    op.drop_index(op.f("ix_fixed_assets_warehouse_id"), table_name="fixed_assets")
    op.drop_index(op.f("ix_fixed_assets_name"), table_name="fixed_assets")
    op.drop_index(op.f("ix_fixed_assets_id"), table_name="fixed_assets")
    op.drop_index(op.f("ix_fixed_assets_company_id"), table_name="fixed_assets")
    op.drop_index(op.f("ix_fixed_assets_code"), table_name="fixed_assets")
    op.drop_index(op.f("ix_fixed_assets_branch_id"), table_name="fixed_assets")
    op.drop_table("fixed_assets")
