from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.chart_of_account import ChartOfAccount
from app.models.journal_entry import JournalEntry


class FinanceService:
    @staticmethod
    def list_chart_of_accounts(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(ChartOfAccount).filter(ChartOfAccount.company_id == company_id, ChartOfAccount.is_deleted.is_(False))
        if search:
            query = query.filter(or_(ChartOfAccount.code.ilike(f"%{search}%"), ChartOfAccount.name.ilike(f"%{search}%")))
        return query.order_by(ChartOfAccount.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_chart_of_account(db: Session, payload: dict) -> ChartOfAccount:
        item = ChartOfAccount(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_chart_of_account(db: Session, account_id: int, payload: dict) -> ChartOfAccount | None:
        item = db.query(ChartOfAccount).filter(ChartOfAccount.id == account_id, ChartOfAccount.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_chart_of_account(db: Session, account_id: int) -> bool:
        item = db.query(ChartOfAccount).filter(ChartOfAccount.id == account_id, ChartOfAccount.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_journal_entries(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(JournalEntry).filter(JournalEntry.company_id == company_id, JournalEntry.is_deleted.is_(False))
        if search:
            query = query.filter(or_(JournalEntry.code.ilike(f"%{search}%"), JournalEntry.note.ilike(f"%{search}%")))
        return query.order_by(JournalEntry.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_journal_entry(db: Session, payload: dict) -> JournalEntry:
        item = JournalEntry(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_journal_entry(db: Session, journal_entry_id: int, payload: dict) -> JournalEntry | None:
        item = db.query(JournalEntry).filter(JournalEntry.id == journal_entry_id, JournalEntry.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_journal_entry(db: Session, journal_entry_id: int) -> bool:
        item = db.query(JournalEntry).filter(JournalEntry.id == journal_entry_id, JournalEntry.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True
