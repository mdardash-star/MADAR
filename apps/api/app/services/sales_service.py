from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.sales_invoice import SalesInvoice
from app.models.sales_order import SalesOrder
from app.models.sales_quotation import SalesQuotation


class SalesService:
    @staticmethod
    def list_quotations(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(SalesQuotation).filter(SalesQuotation.company_id == company_id, SalesQuotation.is_deleted.is_(False))
        if search:
            query = query.filter(or_(SalesQuotation.code.ilike(f"%{search}%"), SalesQuotation.note.ilike(f"%{search}%")))
        return query.order_by(SalesQuotation.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_quotation(db: Session, payload: dict) -> SalesQuotation:
        item = SalesQuotation(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_quotation(db: Session, quotation_id: int, payload: dict) -> SalesQuotation | None:
        item = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id, SalesQuotation.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_quotation(db: Session, quotation_id: int) -> bool:
        item = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id, SalesQuotation.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_orders(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(SalesOrder).filter(SalesOrder.company_id == company_id, SalesOrder.is_deleted.is_(False))
        if search:
            query = query.filter(or_(SalesOrder.code.ilike(f"%{search}%"), SalesOrder.note.ilike(f"%{search}%")))
        return query.order_by(SalesOrder.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_order(db: Session, payload: dict) -> SalesOrder:
        item = SalesOrder(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_order(db: Session, order_id: int, payload: dict) -> SalesOrder | None:
        item = db.query(SalesOrder).filter(SalesOrder.id == order_id, SalesOrder.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        item = db.query(SalesOrder).filter(SalesOrder.id == order_id, SalesOrder.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_invoices(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(SalesInvoice).filter(SalesInvoice.company_id == company_id, SalesInvoice.is_deleted.is_(False))
        if search:
            query = query.filter(or_(SalesInvoice.code.ilike(f"%{search}%"), SalesInvoice.note.ilike(f"%{search}%")))
        return query.order_by(SalesInvoice.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_invoice(db: Session, payload: dict) -> SalesInvoice:
        item = SalesInvoice(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_invoice(db: Session, invoice_id: int, payload: dict) -> SalesInvoice | None:
        item = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id, SalesInvoice.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_invoice(db: Session, invoice_id: int) -> bool:
        item = db.query(SalesInvoice).filter(SalesInvoice.id == invoice_id, SalesInvoice.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True
