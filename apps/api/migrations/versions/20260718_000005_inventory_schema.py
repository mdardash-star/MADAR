"""Add inventory tables for MADAR ERP

Revision ID: 20260718_000005
Revises: 20260718_000004
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000005"
down_revision = "20260718_000004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stock_movements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("movement_type", sa.String(length=50), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("movement_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_movements_company_id"), "stock_movements", ["company_id"], unique=False)
    op.create_index(op.f("ix_stock_movements_id"), "stock_movements", ["id"], unique=False)
    op.create_index(op.f("ix_stock_movements_product_id"), "stock_movements", ["product_id"], unique=False)
    op.create_index(op.f("ix_stock_movements_reference_id"), "stock_movements", ["reference_id"], unique=False)
    op.create_index(op.f("ix_stock_movements_warehouse_id"), "stock_movements", ["warehouse_id"], unique=False)

    op.create_table(
        "stock_transfers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("from_warehouse_id", sa.Integer(), nullable=False),
        sa.Column("to_warehouse_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("transfer_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["from_warehouse_id"], ["warehouses.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["to_warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_transfers_code"), "stock_transfers", ["code"], unique=True)
    op.create_index(op.f("ix_stock_transfers_company_id"), "stock_transfers", ["company_id"], unique=False)
    op.create_index(op.f("ix_stock_transfers_from_warehouse_id"), "stock_transfers", ["from_warehouse_id"], unique=False)
    op.create_index(op.f("ix_stock_transfers_id"), "stock_transfers", ["id"], unique=False)
    op.create_index(op.f("ix_stock_transfers_product_id"), "stock_transfers", ["product_id"], unique=False)
    op.create_index(op.f("ix_stock_transfers_to_warehouse_id"), "stock_transfers", ["to_warehouse_id"], unique=False)

    op.create_table(
        "stock_adjustments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("adjustment_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("adjustment_type", sa.String(length=50), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_adjustments_code"), "stock_adjustments", ["code"], unique=True)
    op.create_index(op.f("ix_stock_adjustments_company_id"), "stock_adjustments", ["company_id"], unique=False)
    op.create_index(op.f("ix_stock_adjustments_id"), "stock_adjustments", ["id"], unique=False)
    op.create_index(op.f("ix_stock_adjustments_product_id"), "stock_adjustments", ["product_id"], unique=False)
    op.create_index(op.f("ix_stock_adjustments_warehouse_id"), "stock_adjustments", ["warehouse_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_stock_adjustments_warehouse_id"), table_name="stock_adjustments")
    op.drop_index(op.f("ix_stock_adjustments_product_id"), table_name="stock_adjustments")
    op.drop_index(op.f("ix_stock_adjustments_id"), table_name="stock_adjustments")
    op.drop_index(op.f("ix_stock_adjustments_company_id"), table_name="stock_adjustments")
    op.drop_index(op.f("ix_stock_adjustments_code"), table_name="stock_adjustments")
    op.drop_table("stock_adjustments")

    op.drop_index(op.f("ix_stock_transfers_to_warehouse_id"), table_name="stock_transfers")
    op.drop_index(op.f("ix_stock_transfers_product_id"), table_name="stock_transfers")
    op.drop_index(op.f("ix_stock_transfers_id"), table_name="stock_transfers")
    op.drop_index(op.f("ix_stock_transfers_from_warehouse_id"), table_name="stock_transfers")
    op.drop_index(op.f("ix_stock_transfers_company_id"), table_name="stock_transfers")
    op.drop_index(op.f("ix_stock_transfers_code"), table_name="stock_transfers")
    op.drop_table("stock_transfers")

    op.drop_index(op.f("ix_stock_movements_warehouse_id"), table_name="stock_movements")
    op.drop_index(op.f("ix_stock_movements_reference_id"), table_name="stock_movements")
    op.drop_index(op.f("ix_stock_movements_product_id"), table_name="stock_movements")
    op.drop_index(op.f("ix_stock_movements_id"), table_name="stock_movements")
    op.drop_index(op.f("ix_stock_movements_company_id"), table_name="stock_movements")
    op.drop_table("stock_movements")
