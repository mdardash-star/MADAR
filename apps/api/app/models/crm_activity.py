from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CrmActivity(Base):
    """A logged interaction tied to a lead or opportunity (call, meeting, email, task)."""

    __tablename__ = "crm_activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("crm_leads.id"), nullable=True, index=True)
    opportunity_id: Mapped[int | None] = mapped_column(ForeignKey("crm_opportunities.id"), nullable=True, index=True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # call/meeting/email/task
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[str | None] = mapped_column(String(10), nullable=True)  # ISO date string YYYY-MM-DD
    outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="planned")  # planned/done/cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CrmNote(Base):
    """A free-text note attached to a lead or opportunity."""

    __tablename__ = "crm_notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("crm_leads.id"), nullable=True, index=True)
    opportunity_id: Mapped[int | None] = mapped_column(ForeignKey("crm_opportunities.id"), nullable=True, index=True)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
