"""Add sales tables for MADAR ERP

Revision ID: 20260718_000003
Revises: 20260718_000002
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000003"
down_revision = "20260718_000002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sales_quotations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("quote_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("currency_id", sa.Integer(), nullable=True),
        sa.Column("subtotal_amount", sa.Float(), nullable=False),
        sa.Column("tax_amount", sa.Float(), nullable=False),
        sa.Column("discount_amount", sa.Float(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["currency_id"], ["currency_settings.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_quotations_code"), "sales_quotations", ["code"], unique=True)
    op.create_index(op.f("ix_sales_quotations_company_id"), "sales_quotations", ["company_id"], unique=False)
    op.create_index(op.f("ix_sales_quotations_currency_id"), "sales_quotations", ["currency_id"], unique=False)
    op.create_index(op.f("ix_sales_quotations_customer_id"), "sales_quotations", ["customer_id"], unique=False)
    op.create_index(op.f("ix_sales_quotations_id"), "sales_quotations", ["id"], unique=False)
    op.create_index(op.f("ix_sales_quotations_warehouse_id"), "sales_quotations", ["warehouse_id"], unique=False)

    op.create_table(
        "sales_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("order_date", sa.DateTime(timezone=True), nullable=False),
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
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["currency_id"], ["currency_settings.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_orders_code"), "sales_orders", ["code"], unique=True)
    op.create_index(op.f("ix_sales_orders_company_id"), "sales_orders", ["company_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_currency_id"), "sales_orders", ["currency_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_customer_id"), "sales_orders", ["customer_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_id"), "sales_orders", ["id"], unique=False)
    op.create_index(op.f("ix_sales_orders_warehouse_id"), "sales_orders", ["warehouse_id"], unique=False)

    op.create_table(
        "sales_invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("warehouse_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("invoice_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["currency_id"], ["currency_settings.id"]),
        sa.ForeignKeyConstraint(["order_id"], ["sales_orders.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_invoices_code"), "sales_invoices", ["code"], unique=True)
    op.create_index(op.f("ix_sales_invoices_company_id"), "sales_invoices", ["company_id"], unique=False)
    op.create_index(op.f("ix_sales_invoices_currency_id"), "sales_invoices", ["currency_id"], unique=False)
    op.create_index(op.f("ix_sales_invoices_customer_id"), "sales_invoices", ["customer_id"], unique=False)
    op.create_index(op.f("ix_sales_invoices_id"), "sales_invoices", ["id"], unique=False)
    op.create_index(op.f("ix_sales_invoices_order_id"), "sales_invoices", ["order_id"], unique=False)
    op.create_index(op.f("ix_sales_invoices_warehouse_id"), "sales_invoices", ["warehouse_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_sales_invoices_warehouse_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_order_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_customer_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_currency_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_company_id"), table_name="sales_invoices")
    op.drop_index(op.f("ix_sales_invoices_code"), table_name="sales_invoices")
    op.drop_table("sales_invoices")

    op.drop_index(op.f("ix_sales_orders_warehouse_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_customer_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_currency_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_company_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_code"), table_name="sales_orders")
    op.drop_table("sales_orders")

    op.drop_index(op.f("ix_sales_quotations_warehouse_id"), table_name="sales_quotations")
    op.drop_index(op.f("ix_sales_quotations_id"), table_name="sales_quotations")
    op.drop_index(op.f("ix_sales_quotations_customer_id"), table_name="sales_quotations")
    op.drop_index(op.f("ix_sales_quotations_currency_id"), table_name="sales_quotations")
    op.drop_index(op.f("ix_sales_quotations_company_id"), table_name="sales_quotations")
    op.drop_index(op.f("ix_sales_quotations_code"), table_name="sales_quotations")
    op.drop_table("sales_quotations")
