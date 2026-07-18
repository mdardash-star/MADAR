"""Add HR tables for MADAR ERP

Revision ID: 20260718_000007
Revises: 20260718_000006
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260718_000007"
down_revision = "20260718_000006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("employee_code", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_employees_branch_id"), "employees", ["branch_id"], unique=False)
    op.create_index(op.f("ix_employees_company_id"), "employees", ["company_id"], unique=False)
    op.create_index(op.f("ix_employees_email"), "employees", ["email"], unique=False)
    op.create_index(op.f("ix_employees_employee_code"), "employees", ["employee_code"], unique=True)
    op.create_index(op.f("ix_employees_id"), "employees", ["id"], unique=False)
    op.create_index(op.f("ix_employees_role_id"), "employees", ["role_id"], unique=False)

    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("attendance_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("check_in", sa.DateTime(timezone=True), nullable=True),
        sa.Column("check_out", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_attendances_branch_id"), "attendances", ["branch_id"], unique=False)
    op.create_index(op.f("ix_attendances_company_id"), "attendances", ["company_id"], unique=False)
    op.create_index(op.f("ix_attendances_employee_id"), "attendances", ["employee_id"], unique=False)
    op.create_index(op.f("ix_attendances_id"), "attendances", ["id"], unique=False)

    op.create_table(
        "payrolls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("payroll_month", sa.String(length=20), nullable=False),
        sa.Column("basic_salary", sa.Float(), nullable=False),
        sa.Column("allowances", sa.Float(), nullable=False),
        sa.Column("deductions", sa.Float(), nullable=False),
        sa.Column("net_salary", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payrolls_branch_id"), "payrolls", ["branch_id"], unique=False)
    op.create_index(op.f("ix_payrolls_company_id"), "payrolls", ["company_id"], unique=False)
    op.create_index(op.f("ix_payrolls_employee_id"), "payrolls", ["employee_id"], unique=False)
    op.create_index(op.f("ix_payrolls_id"), "payrolls", ["id"], unique=False)
    op.create_index(op.f("ix_payrolls_payroll_month"), "payrolls", ["payroll_month"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_payrolls_payroll_month"), table_name="payrolls")
    op.drop_index(op.f("ix_payrolls_id"), table_name="payrolls")
    op.drop_index(op.f("ix_payrolls_employee_id"), table_name="payrolls")
    op.drop_index(op.f("ix_payrolls_company_id"), table_name="payrolls")
    op.drop_index(op.f("ix_payrolls_branch_id"), table_name="payrolls")
    op.drop_table("payrolls")

    op.drop_index(op.f("ix_attendances_id"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_employee_id"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_company_id"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_branch_id"), table_name="attendances")
    op.drop_table("attendances")

    op.drop_index(op.f("ix_employees_role_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_employee_code"), table_name="employees")
    op.drop_index(op.f("ix_employees_email"), table_name="employees")
    op.drop_index(op.f("ix_employees_company_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_branch_id"), table_name="employees")
    op.drop_table("employees")
