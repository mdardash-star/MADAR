"""Add finance tables for MADAR ERP

Revision ID: 20260718_000006
Revises: 20260718_000005
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000006"
down_revision = "20260718_000005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chart_of_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("parent_account_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("account_type", sa.String(length=50), nullable=False),
        sa.Column("normal_balance", sa.String(length=10), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["parent_account_id"], ["chart_of_accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chart_of_accounts_branch_id"), "chart_of_accounts", ["branch_id"], unique=False)
    op.create_index(op.f("ix_chart_of_accounts_code"), "chart_of_accounts", ["code"], unique=True)
    op.create_index(op.f("ix_chart_of_accounts_company_id"), "chart_of_accounts", ["company_id"], unique=False)
    op.create_index(op.f("ix_chart_of_accounts_id"), "chart_of_accounts", ["id"], unique=False)
    op.create_index(op.f("ix_chart_of_accounts_name"), "chart_of_accounts", ["name"], unique=False)

    op.create_table(
        "journal_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("entry_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("total_debit", sa.Float(), nullable=False),
        sa.Column("total_credit", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_journal_entries_branch_id"), "journal_entries", ["branch_id"], unique=False)
    op.create_index(op.f("ix_journal_entries_code"), "journal_entries", ["code"], unique=True)
    op.create_index(op.f("ix_journal_entries_company_id"), "journal_entries", ["company_id"], unique=False)
    op.create_index(op.f("ix_journal_entries_id"), "journal_entries", ["id"], unique=False)
    op.create_index(op.f("ix_journal_entries_reference_id"), "journal_entries", ["reference_id"], unique=False)

    op.create_table(
        "journal_entry_lines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("journal_entry_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("debit_amount", sa.Float(), nullable=False),
        sa.Column("credit_amount", sa.Float(), nullable=False),
        sa.Column("line_note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["chart_of_accounts.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["journal_entry_id"], ["journal_entries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_journal_entry_lines_account_id"), "journal_entry_lines", ["account_id"], unique=False)
    op.create_index(op.f("ix_journal_entry_lines_company_id"), "journal_entry_lines", ["company_id"], unique=False)
    op.create_index(op.f("ix_journal_entry_lines_id"), "journal_entry_lines", ["id"], unique=False)
    op.create_index(op.f("ix_journal_entry_lines_journal_entry_id"), "journal_entry_lines", ["journal_entry_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_journal_entry_lines_journal_entry_id"), table_name="journal_entry_lines")
    op.drop_index(op.f("ix_journal_entry_lines_id"), table_name="journal_entry_lines")
    op.drop_index(op.f("ix_journal_entry_lines_company_id"), table_name="journal_entry_lines")
    op.drop_index(op.f("ix_journal_entry_lines_account_id"), table_name="journal_entry_lines")
    op.drop_table("journal_entry_lines")

    op.drop_index(op.f("ix_journal_entries_reference_id"), table_name="journal_entries")
    op.drop_index(op.f("ix_journal_entries_id"), table_name="journal_entries")
    op.drop_index(op.f("ix_journal_entries_company_id"), table_name="journal_entries")
    op.drop_index(op.f("ix_journal_entries_code"), table_name="journal_entries")
    op.drop_index(op.f("ix_journal_entries_branch_id"), table_name="journal_entries")
    op.drop_table("journal_entries")

    op.drop_index(op.f("ix_chart_of_accounts_name"), table_name="chart_of_accounts")
    op.drop_index(op.f("ix_chart_of_accounts_id"), table_name="chart_of_accounts")
    op.drop_index(op.f("ix_chart_of_accounts_company_id"), table_name="chart_of_accounts")
    op.drop_index(op.f("ix_chart_of_accounts_code"), table_name="chart_of_accounts")
    op.drop_index(op.f("ix_chart_of_accounts_branch_id"), table_name="chart_of_accounts")
    op.drop_table("chart_of_accounts")
