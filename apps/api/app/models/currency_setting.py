from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CurrencySetting(Base):
    __tablename__ = "currency_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String(10), nullable=True)
    exchange_rate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
