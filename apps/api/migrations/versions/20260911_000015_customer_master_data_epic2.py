"""Expand customer master data for EPIC 2.1

Revision ID: 20260911_000015
Revises: 20260718_000014
Create Date: 2026-09-11 20:30:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260911_000015"
down_revision = "20260718_000014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_customers_code", table_name="customers")

    op.add_column("customers", sa.Column("branch_id", sa.Integer(), nullable=True))
    op.add_column("customers", sa.Column("customer_group_id", sa.Integer(), nullable=True))
    op.add_column("customers", sa.Column("sales_owner_id", sa.Integer(), nullable=True))
    op.add_column("customers", sa.Column("customer_type", sa.String(length=20), nullable=False, server_default="company"))
    op.add_column("customers", sa.Column("tax_number", sa.String(length=50), nullable=True))
    op.add_column("customers", sa.Column("credit_limit", sa.Float(), nullable=False, server_default="0"))
    op.add_column("customers", sa.Column("payment_terms_days", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("customers", sa.Column("notes", sa.String(length=1000), nullable=True))

    op.create_foreign_key("fk_customers_branch_id", "customers", "branches", ["branch_id"], ["id"])
    op.create_foreign_key("fk_customers_customer_group_id", "customers", "customer_groups", ["customer_group_id"], ["id"])
    op.create_foreign_key("fk_customers_sales_owner_id", "customers", "users", ["sales_owner_id"], ["id"])

    op.create_index("ix_customers_branch_id", "customers", ["branch_id"], unique=False)
    op.create_index("ix_customers_customer_group_id", "customers", ["customer_group_id"], unique=False)
    op.create_index("ix_customers_sales_owner_id", "customers", ["sales_owner_id"], unique=False)
    op.create_index("ix_customers_customer_type", "customers", ["customer_type"], unique=False)
    op.create_index("ix_customers_tax_number", "customers", ["tax_number"], unique=False)
    op.create_index("ix_customers_code", "customers", ["code"], unique=False)

    op.create_unique_constraint("uq_customers_company_code", "customers", ["company_id", "code"])
    op.create_unique_constraint("uq_customers_company_tax_number", "customers", ["company_id", "tax_number"])

    op.add_column(
        "customer_addresses",
        sa.Column("address_type", sa.String(length=20), nullable=False, server_default="other"),
    )
    op.create_index("ix_customer_addresses_address_type", "customer_addresses", ["address_type"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_customer_addresses_address_type", table_name="customer_addresses")
    op.drop_column("customer_addresses", "address_type")

    op.drop_constraint("uq_customers_company_tax_number", "customers", type_="unique")
    op.drop_constraint("uq_customers_company_code", "customers", type_="unique")

    op.drop_index("ix_customers_tax_number", table_name="customers")
    op.drop_index("ix_customers_customer_type", table_name="customers")
    op.drop_index("ix_customers_sales_owner_id", table_name="customers")
    op.drop_index("ix_customers_customer_group_id", table_name="customers")
    op.drop_index("ix_customers_branch_id", table_name="customers")
    op.drop_index("ix_customers_code", table_name="customers")

    op.drop_constraint("fk_customers_sales_owner_id", "customers", type_="foreignkey")
    op.drop_constraint("fk_customers_customer_group_id", "customers", type_="foreignkey")
    op.drop_constraint("fk_customers_branch_id", "customers", type_="foreignkey")

    op.drop_column("customers", "notes")
    op.drop_column("customers", "payment_terms_days")
    op.drop_column("customers", "credit_limit")
    op.drop_column("customers", "tax_number")
    op.drop_column("customers", "customer_type")
    op.drop_column("customers", "sales_owner_id")
    op.drop_column("customers", "customer_group_id")
    op.drop_column("customers", "branch_id")

    op.create_index("ix_customers_code", "customers", ["code"], unique=True)
