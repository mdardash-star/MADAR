"""Add CRM tables — leads, pipelines, stages, opportunities, activities, notes

Revision ID: 20260718_000010
Revises: 20260718_000009
Create Date: 2026-07-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "20260718_000010"
down_revision = "20260718_000009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "crm_leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("job_title", sa.String(length=100), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_to"], ["users.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_leads_assigned_to"), "crm_leads", ["assigned_to"], unique=False)
    op.create_index(op.f("ix_crm_leads_company_id"), "crm_leads", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_leads_id"), "crm_leads", ["id"], unique=False)

    op.create_table(
        "crm_pipelines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_pipelines_company_id"), "crm_pipelines", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_pipelines_id"), "crm_pipelines", ["id"], unique=False)

    op.create_table(
        "crm_stages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("is_won", sa.Boolean(), nullable=False),
        sa.Column("is_lost", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["pipeline_id"], ["crm_pipelines.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_stages_company_id"), "crm_stages", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_stages_id"), "crm_stages", ["id"], unique=False)
    op.create_index(op.f("ix_crm_stages_pipeline_id"), "crm_stages", ["pipeline_id"], unique=False)

    op.create_table(
        "crm_opportunities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("customer_id", sa.Integer(), nullable=True),
        sa.Column("pipeline_id", sa.Integer(), nullable=False),
        sa.Column("stage_id", sa.Integer(), nullable=False),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("expected_value", sa.Float(), nullable=False),
        sa.Column("expected_close_date", sa.String(length=10), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_to"], ["users.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.ForeignKeyConstraint(["lead_id"], ["crm_leads.id"]),
        sa.ForeignKeyConstraint(["pipeline_id"], ["crm_pipelines.id"]),
        sa.ForeignKeyConstraint(["stage_id"], ["crm_stages.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_opportunities_assigned_to"), "crm_opportunities", ["assigned_to"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_company_id"), "crm_opportunities", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_customer_id"), "crm_opportunities", ["customer_id"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_id"), "crm_opportunities", ["id"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_lead_id"), "crm_opportunities", ["lead_id"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_pipeline_id"), "crm_opportunities", ["pipeline_id"], unique=False)
    op.create_index(op.f("ix_crm_opportunities_stage_id"), "crm_opportunities", ["stage_id"], unique=False)

    op.create_table(
        "crm_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("opportunity_id", sa.Integer(), nullable=True),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        sa.Column("activity_type", sa.String(length=50), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("due_date", sa.String(length=10), nullable=True),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["assigned_to"], ["users.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["lead_id"], ["crm_leads.id"]),
        sa.ForeignKeyConstraint(["opportunity_id"], ["crm_opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_activities_assigned_to"), "crm_activities", ["assigned_to"], unique=False)
    op.create_index(op.f("ix_crm_activities_company_id"), "crm_activities", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_activities_id"), "crm_activities", ["id"], unique=False)
    op.create_index(op.f("ix_crm_activities_lead_id"), "crm_activities", ["lead_id"], unique=False)
    op.create_index(op.f("ix_crm_activities_opportunity_id"), "crm_activities", ["opportunity_id"], unique=False)

    op.create_table(
        "crm_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("opportunity_id", sa.Integer(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["lead_id"], ["crm_leads.id"]),
        sa.ForeignKeyConstraint(["opportunity_id"], ["crm_opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crm_notes_author_id"), "crm_notes", ["author_id"], unique=False)
    op.create_index(op.f("ix_crm_notes_company_id"), "crm_notes", ["company_id"], unique=False)
    op.create_index(op.f("ix_crm_notes_id"), "crm_notes", ["id"], unique=False)
    op.create_index(op.f("ix_crm_notes_lead_id"), "crm_notes", ["lead_id"], unique=False)
    op.create_index(op.f("ix_crm_notes_opportunity_id"), "crm_notes", ["opportunity_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_crm_notes_opportunity_id"), table_name="crm_notes")
    op.drop_index(op.f("ix_crm_notes_lead_id"), table_name="crm_notes")
    op.drop_index(op.f("ix_crm_notes_id"), table_name="crm_notes")
    op.drop_index(op.f("ix_crm_notes_company_id"), table_name="crm_notes")
    op.drop_index(op.f("ix_crm_notes_author_id"), table_name="crm_notes")
    op.drop_table("crm_notes")

    op.drop_index(op.f("ix_crm_activities_opportunity_id"), table_name="crm_activities")
    op.drop_index(op.f("ix_crm_activities_lead_id"), table_name="crm_activities")
    op.drop_index(op.f("ix_crm_activities_id"), table_name="crm_activities")
    op.drop_index(op.f("ix_crm_activities_company_id"), table_name="crm_activities")
    op.drop_index(op.f("ix_crm_activities_assigned_to"), table_name="crm_activities")
    op.drop_table("crm_activities")

    op.drop_index(op.f("ix_crm_opportunities_stage_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_pipeline_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_lead_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_customer_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_company_id"), table_name="crm_opportunities")
    op.drop_index(op.f("ix_crm_opportunities_assigned_to"), table_name="crm_opportunities")
    op.drop_table("crm_opportunities")

    op.drop_index(op.f("ix_crm_stages_pipeline_id"), table_name="crm_stages")
    op.drop_index(op.f("ix_crm_stages_id"), table_name="crm_stages")
    op.drop_index(op.f("ix_crm_stages_company_id"), table_name="crm_stages")
    op.drop_table("crm_stages")

    op.drop_index(op.f("ix_crm_pipelines_id"), table_name="crm_pipelines")
    op.drop_index(op.f("ix_crm_pipelines_company_id"), table_name="crm_pipelines")
    op.drop_table("crm_pipelines")

    op.drop_index(op.f("ix_crm_leads_id"), table_name="crm_leads")
    op.drop_index(op.f("ix_crm_leads_company_id"), table_name="crm_leads")
    op.drop_index(op.f("ix_crm_leads_assigned_to"), table_name="crm_leads")
    op.drop_table("crm_leads")
