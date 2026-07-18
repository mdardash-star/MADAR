from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CrmOpportunity(Base):
    """A qualified deal being tracked through a CRM pipeline."""

    __tablename__ = "crm_opportunities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("crm_leads.id"), nullable=True, index=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id"), nullable=True, index=True)
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("crm_pipelines.id"), nullable=False, index=True)
    stage_id: Mapped[int] = mapped_column(ForeignKey("crm_stages.id"), nullable=False, index=True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    expected_close_date: Mapped[str | None] = mapped_column(String(10), nullable=True)  # ISO date string YYYY-MM-DD
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")  # open/won/lost
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
