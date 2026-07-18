"""Add procurement tables for MADAR ERP

Revision ID: 20260718_000004
Revises: 20260718_000003
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000004"
down_revision = "20260718_000003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("order_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expected_delivery_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=True),
        sa.Column("subtotal_amount", sa.Float(), nullable=False),
        sa.Column("tax_amount", sa.Float(), nullable=False),
        sa.Column("discount_amount", sa.Float(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("payment_status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["currency_id"], ["currency_settings.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_orders_code"), "purchase_orders", ["code"], unique=True)
    op.create_index(op.f("ix_purchase_orders_company_id"), "purchase_orders", ["company_id"], unique=False)
    op.create_index(op.f("ix_purchase_orders_currency_id"), "purchase_orders", ["currency_id"], unique=False)
    op.create_index(op.f("ix_purchase_orders_id"), "purchase_orders", ["id"], unique=False)
    op.create_index(op.f("ix_purchase_orders_supplier_id"), "purchase_orders", ["supplier_id"], unique=False)
    op.create_index(op.f("ix_purchase_orders_warehouse_id"), "purchase_orders", ["warehouse_id"], unique=False)

    op.create_table(
        "goods_receipts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("purchase_order_id", sa.Integer(), nullable=True),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("receipt_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("quantity_received", sa.Float(), nullable=False),
        sa.Column("subtotal_amount", sa.Float(), nullable=False),
        sa.Column("tax_amount", sa.Float(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["purchase_order_id"], ["purchase_orders.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_goods_receipts_code"), "goods_receipts", ["code"], unique=True)
    op.create_index(op.f("ix_goods_receipts_company_id"), "goods_receipts", ["company_id"], unique=False)
    op.create_index(op.f("ix_goods_receipts_id"), "goods_receipts", ["id"], unique=False)
    op.create_index(op.f("ix_goods_receipts_purchase_order_id"), "goods_receipts", ["purchase_order_id"], unique=False)
    op.create_index(op.f("ix_goods_receipts_supplier_id"), "goods_receipts", ["supplier_id"], unique=False)
    op.create_index(op.f("ix_goods_receipts_warehouse_id"), "goods_receipts", ["warehouse_id"], unique=False)

    op.create_table(
        "purchase_returns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("purchase_order_id", sa.Integer(), nullable=True),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("return_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["purchase_order_id"], ["purchase_orders.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_returns_code"), "purchase_returns", ["code"], unique=True)
    op.create_index(op.f("ix_purchase_returns_company_id"), "purchase_returns", ["company_id"], unique=False)
    op.create_index(op.f("ix_purchase_returns_id"), "purchase_returns", ["id"], unique=False)
    op.create_index(op.f("ix_purchase_returns_purchase_order_id"), "purchase_returns", ["purchase_order_id"], unique=False)
    op.create_index(op.f("ix_purchase_returns_supplier_id"), "purchase_returns", ["supplier_id"], unique=False)
    op.create_index(op.f("ix_purchase_returns_warehouse_id"), "purchase_returns", ["warehouse_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_purchase_returns_warehouse_id"), table_name="purchase_returns")
    op.drop_index(op.f("ix_purchase_returns_supplier_id"), table_name="purchase_returns")
    op.drop_index(op.f("ix_purchase_returns_purchase_order_id"), table_name="purchase_returns")
    op.drop_index(op.f("ix_purchase_returns_id"), table_name="purchase_returns")
    op.drop_index(op.f("ix_purchase_returns_company_id"), table_name="purchase_returns")
    op.drop_index(op.f("ix_purchase_returns_code"), table_name="purchase_returns")
    op.drop_table("purchase_returns")

    op.drop_index(op.f("ix_goods_receipts_warehouse_id"), table_name="goods_receipts")
    op.drop_index(op.f("ix_goods_receipts_supplier_id"), table_name="goods_receipts")
    op.drop_index(op.f("ix_goods_receipts_purchase_order_id"), table_name="goods_receipts")
    op.drop_index(op.f("ix_goods_receipts_id"), table_name="goods_receipts")
    op.drop_index(op.f("ix_goods_receipts_company_id"), table_name="goods_receipts")
    op.drop_index(op.f("ix_goods_receipts_code"), table_name="goods_receipts")
    op.drop_table("goods_receipts")

    op.drop_index(op.f("ix_purchase_orders_warehouse_id"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_supplier_id"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_id"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_currency_id"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_company_id"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_code"), table_name="purchase_orders")
    op.drop_table("purchase_orders")
