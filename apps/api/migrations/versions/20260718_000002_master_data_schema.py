"""Add master data tables for MADAR ERP

Revision ID: 20260718_000002
Revises: 20260718_000001
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000002"
down_revision = "20260718_000001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_departments_code"), "departments", ["code"], unique=True)
    op.create_index(op.f("ix_departments_company_id"), "departments", ["company_id"], unique=False)
    op.create_index(op.f("ix_departments_id"), "departments", ["id"], unique=False)

    op.create_table(
        "warehouses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_warehouses_code"), "warehouses", ["code"], unique=True)
    op.create_index(op.f("ix_warehouses_company_id"), "warehouses", ["company_id"], unique=False)
    op.create_index(op.f("ix_warehouses_id"), "warehouses", ["id"], unique=False)

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_code"), "customers", ["code"], unique=True)
    op.create_index(op.f("ix_customers_company_id"), "customers", ["company_id"], unique=False)
    op.create_index(op.f("ix_customers_id"), "customers", ["id"], unique=False)

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_suppliers_code"), "suppliers", ["code"], unique=True)
    op.create_index(op.f("ix_suppliers_company_id"), "suppliers", ["company_id"], unique=False)
    op.create_index(op.f("ix_suppliers_id"), "suppliers", ["id"], unique=False)

    op.create_table(
        "product_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_categories_code"), "product_categories", ["code"], unique=True)
    op.create_index(op.f("ix_product_categories_company_id"), "product_categories", ["company_id"], unique=False)
    op.create_index(op.f("ix_product_categories_id"), "product_categories", ["id"], unique=False)

    op.create_table(
        "units_of_measure",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("abbreviation", sa.String(length=20), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_units_of_measure_code"), "units_of_measure", ["code"], unique=True)
    op.create_index(op.f("ix_units_of_measure_company_id"), "units_of_measure", ["company_id"], unique=False)
    op.create_index(op.f("ix_units_of_measure_id"), "units_of_measure", ["id"], unique=False)

    op.create_table(
        "tax_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("rate_percent", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tax_settings_code"), "tax_settings", ["code"], unique=True)
    op.create_index(op.f("ix_tax_settings_company_id"), "tax_settings", ["company_id"], unique=False)
    op.create_index(op.f("ix_tax_settings_id"), "tax_settings", ["id"], unique=False)

    op.create_table(
        "currency_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("symbol", sa.String(length=10), nullable=True),
        sa.Column("exchange_rate", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_currency_settings_code"), "currency_settings", ["code"], unique=True)
    op.create_index(op.f("ix_currency_settings_company_id"), "currency_settings", ["company_id"], unique=False)
    op.create_index(op.f("ix_currency_settings_id"), "currency_settings", ["id"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("unit_of_measure_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("barcode", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("selling_price", sa.Float(), nullable=False),
        sa.Column("cost_price", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["product_categories.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["unit_of_measure_id"], ["units_of_measure.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_barcode"), "products", ["barcode"], unique=True)
    op.create_index(op.f("ix_products_company_id"), "products", ["company_id"], unique=False)
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=True)

    op.create_table(
        "product_variants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("variant_price", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_variants_id"), "product_variants", ["id"], unique=False)
    op.create_index(op.f("ix_product_variants_product_id"), "product_variants", ["product_id"], unique=False)
    op.create_index(op.f("ix_product_variants_sku"), "product_variants", ["sku"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_variants_sku"), table_name="product_variants")
    op.drop_index(op.f("ix_product_variants_product_id"), table_name="product_variants")
    op.drop_index(op.f("ix_product_variants_id"), table_name="product_variants")
    op.drop_table("product_variants")

    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_index(op.f("ix_products_company_id"), table_name="products")
    op.drop_index(op.f("ix_products_barcode"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_currency_settings_id"), table_name="currency_settings")
    op.drop_index(op.f("ix_currency_settings_company_id"), table_name="currency_settings")
    op.drop_index(op.f("ix_currency_settings_code"), table_name="currency_settings")
    op.drop_table("currency_settings")

    op.drop_index(op.f("ix_tax_settings_id"), table_name="tax_settings")
    op.drop_index(op.f("ix_tax_settings_company_id"), table_name="tax_settings")
    op.drop_index(op.f("ix_tax_settings_code"), table_name="tax_settings")
    op.drop_table("tax_settings")

    op.drop_index(op.f("ix_units_of_measure_id"), table_name="units_of_measure")
    op.drop_index(op.f("ix_units_of_measure_company_id"), table_name="units_of_measure")
    op.drop_index(op.f("ix_units_of_measure_code"), table_name="units_of_measure")
    op.drop_table("units_of_measure")

    op.drop_index(op.f("ix_product_categories_id"), table_name="product_categories")
    op.drop_index(op.f("ix_product_categories_company_id"), table_name="product_categories")
    op.drop_index(op.f("ix_product_categories_code"), table_name="product_categories")
    op.drop_table("product_categories")

    op.drop_index(op.f("ix_suppliers_id"), table_name="suppliers")
    op.drop_index(op.f("ix_suppliers_company_id"), table_name="suppliers")
    op.drop_index(op.f("ix_suppliers_code"), table_name="suppliers")
    op.drop_table("suppliers")

    op.drop_index(op.f("ix_customers_id"), table_name="customers")
    op.drop_index(op.f("ix_customers_company_id"), table_name="customers")
    op.drop_index(op.f("ix_customers_code"), table_name="customers")
    op.drop_table("customers")

    op.drop_index(op.f("ix_warehouses_id"), table_name="warehouses")
    op.drop_index(op.f("ix_warehouses_company_id"), table_name="warehouses")
    op.drop_index(op.f("ix_warehouses_code"), table_name="warehouses")
    op.drop_table("warehouses")

    op.drop_index(op.f("ix_departments_id"), table_name="departments")
    op.drop_index(op.f("ix_departments_company_id"), table_name="departments")
    op.drop_index(op.f("ix_departments_code"), table_name="departments")
    op.drop_table("departments")
