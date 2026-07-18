"""Add business foundation tables for MADAR ERP

Revision ID: 20260718_000009
Revises: 20260718_000008
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000009"
down_revision = "20260718_000008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "brands",
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
    op.create_index(op.f("ix_brands_code"), "brands", ["code"], unique=True)
    op.create_index(op.f("ix_brands_company_id"), "brands", ["company_id"], unique=False)
    op.create_index(op.f("ix_brands_id"), "brands", ["id"], unique=False)

    op.create_table(
        "cost_centers",
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
    op.create_index(op.f("ix_cost_centers_branch_id"), "cost_centers", ["branch_id"], unique=False)
    op.create_index(op.f("ix_cost_centers_code"), "cost_centers", ["code"], unique=True)
    op.create_index(op.f("ix_cost_centers_company_id"), "cost_centers", ["company_id"], unique=False)
    op.create_index(op.f("ix_cost_centers_id"), "cost_centers", ["id"], unique=False)

    op.create_table(
        "customer_groups",
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
    op.create_index(op.f("ix_customer_groups_code"), "customer_groups", ["code"], unique=True)
    op.create_index(op.f("ix_customer_groups_company_id"), "customer_groups", ["company_id"], unique=False)
    op.create_index(op.f("ix_customer_groups_id"), "customer_groups", ["id"], unique=False)

    op.create_table(
        "customer_contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("position", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customer_contacts_company_id"), "customer_contacts", ["company_id"], unique=False)
    op.create_index(op.f("ix_customer_contacts_customer_id"), "customer_contacts", ["customer_id"], unique=False)
    op.create_index(op.f("ix_customer_contacts_id"), "customer_contacts", ["id"], unique=False)

    op.create_table(
        "customer_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("street", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customer_addresses_company_id"), "customer_addresses", ["company_id"], unique=False)
    op.create_index(op.f("ix_customer_addresses_customer_id"), "customer_addresses", ["customer_id"], unique=False)
    op.create_index(op.f("ix_customer_addresses_id"), "customer_addresses", ["id"], unique=False)

    op.create_table(
        "supplier_contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("position", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_supplier_contacts_company_id"), "supplier_contacts", ["company_id"], unique=False)
    op.create_index(op.f("ix_supplier_contacts_id"), "supplier_contacts", ["id"], unique=False)
    op.create_index(op.f("ix_supplier_contacts_supplier_id"), "supplier_contacts", ["supplier_id"], unique=False)

    op.create_table(
        "supplier_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("street", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_supplier_addresses_company_id"), "supplier_addresses", ["company_id"], unique=False)
    op.create_index(op.f("ix_supplier_addresses_id"), "supplier_addresses", ["id"], unique=False)
    op.create_index(op.f("ix_supplier_addresses_supplier_id"), "supplier_addresses", ["supplier_id"], unique=False)

    op.create_table(
        "storage_locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_storage_locations_code"), "storage_locations", ["code"], unique=True)
    op.create_index(op.f("ix_storage_locations_company_id"), "storage_locations", ["company_id"], unique=False)
    op.create_index(op.f("ix_storage_locations_id"), "storage_locations", ["id"], unique=False)
    op.create_index(op.f("ix_storage_locations_warehouse_id"), "storage_locations", ["warehouse_id"], unique=False)

    op.create_table(
        "stock_opening_balances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("warehouse_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("storage_location_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit_cost", sa.Float(), nullable=False),
        sa.Column("batch_no", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["storage_location_id"], ["storage_locations.id"]),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_opening_balances_company_id"), "stock_opening_balances", ["company_id"], unique=False)
    op.create_index(op.f("ix_stock_opening_balances_id"), "stock_opening_balances", ["id"], unique=False)
    op.create_index(op.f("ix_stock_opening_balances_product_id"), "stock_opening_balances", ["product_id"], unique=False)
    op.create_index(op.f("ix_stock_opening_balances_storage_location_id"), "stock_opening_balances", ["storage_location_id"], unique=False)
    op.create_index(op.f("ix_stock_opening_balances_warehouse_id"), "stock_opening_balances", ["warehouse_id"], unique=False)

    op.create_table(
        "barcodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("barcode_type", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_barcodes_code"), "barcodes", ["code"], unique=True)
    op.create_index(op.f("ix_barcodes_company_id"), "barcodes", ["company_id"], unique=False)
    op.create_index(op.f("ix_barcodes_id"), "barcodes", ["id"], unique=False)
    op.create_index(op.f("ix_barcodes_product_id"), "barcodes", ["product_id"], unique=False)

    op.create_table(
        "product_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("caption", sa.String(length=255), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_images_company_id"), "product_images", ["company_id"], unique=False)
    op.create_index(op.f("ix_product_images_id"), "product_images", ["id"], unique=False)
    op.create_index(op.f("ix_product_images_product_id"), "product_images", ["product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_images_product_id"), table_name="product_images")
    op.drop_index(op.f("ix_product_images_id"), table_name="product_images")
    op.drop_index(op.f("ix_product_images_company_id"), table_name="product_images")
    op.drop_table("product_images")

    op.drop_index(op.f("ix_barcodes_product_id"), table_name="barcodes")
    op.drop_index(op.f("ix_barcodes_id"), table_name="barcodes")
    op.drop_index(op.f("ix_barcodes_company_id"), table_name="barcodes")
    op.drop_index(op.f("ix_barcodes_code"), table_name="barcodes")
    op.drop_table("barcodes")

    op.drop_index(op.f("ix_stock_opening_balances_warehouse_id"), table_name="stock_opening_balances")
    op.drop_index(op.f("ix_stock_opening_balances_storage_location_id"), table_name="stock_opening_balances")
    op.drop_index(op.f("ix_stock_opening_balances_product_id"), table_name="stock_opening_balances")
    op.drop_index(op.f("ix_stock_opening_balances_id"), table_name="stock_opening_balances")
    op.drop_index(op.f("ix_stock_opening_balances_company_id"), table_name="stock_opening_balances")
    op.drop_table("stock_opening_balances")

    op.drop_index(op.f("ix_storage_locations_warehouse_id"), table_name="storage_locations")
    op.drop_index(op.f("ix_storage_locations_id"), table_name="storage_locations")
    op.drop_index(op.f("ix_storage_locations_company_id"), table_name="storage_locations")
    op.drop_index(op.f("ix_storage_locations_code"), table_name="storage_locations")
    op.drop_table("storage_locations")

    op.drop_index(op.f("ix_supplier_addresses_supplier_id"), table_name="supplier_addresses")
    op.drop_index(op.f("ix_supplier_addresses_id"), table_name="supplier_addresses")
    op.drop_index(op.f("ix_supplier_addresses_company_id"), table_name="supplier_addresses")
    op.drop_table("supplier_addresses")

    op.drop_index(op.f("ix_supplier_contacts_supplier_id"), table_name="supplier_contacts")
    op.drop_index(op.f("ix_supplier_contacts_id"), table_name="supplier_contacts")
    op.drop_index(op.f("ix_supplier_contacts_company_id"), table_name="supplier_contacts")
    op.drop_table("supplier_contacts")

    op.drop_index(op.f("ix_customer_addresses_customer_id"), table_name="customer_addresses")
    op.drop_index(op.f("ix_customer_addresses_id"), table_name="customer_addresses")
    op.drop_index(op.f("ix_customer_addresses_company_id"), table_name="customer_addresses")
    op.drop_table("customer_addresses")

    op.drop_index(op.f("ix_customer_contacts_customer_id"), table_name="customer_contacts")
    op.drop_index(op.f("ix_customer_contacts_id"), table_name="customer_contacts")
    op.drop_index(op.f("ix_customer_contacts_company_id"), table_name="customer_contacts")
    op.drop_table("customer_contacts")

    op.drop_index(op.f("ix_customer_groups_id"), table_name="customer_groups")
    op.drop_index(op.f("ix_customer_groups_company_id"), table_name="customer_groups")
    op.drop_index(op.f("ix_customer_groups_code"), table_name="customer_groups")
    op.drop_table("customer_groups")

    op.drop_index(op.f("ix_cost_centers_id"), table_name="cost_centers")
    op.drop_index(op.f("ix_cost_centers_company_id"), table_name="cost_centers")
    op.drop_index(op.f("ix_cost_centers_code"), table_name="cost_centers")
    op.drop_index(op.f("ix_cost_centers_branch_id"), table_name="cost_centers")
    op.drop_table("cost_centers")

    op.drop_index(op.f("ix_brands_id"), table_name="brands")
    op.drop_index(op.f("ix_brands_company_id"), table_name="brands")
    op.drop_index(op.f("ix_brands_code"), table_name="brands")
    op.drop_table("brands")
