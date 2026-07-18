from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.goods_receipt import GoodsReceipt
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_return import PurchaseReturn


class ProcurementService:
    @staticmethod
    def list_purchase_orders(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(PurchaseOrder).filter(PurchaseOrder.company_id == company_id, PurchaseOrder.is_deleted.is_(False))
        if search:
            query = query.filter(or_(PurchaseOrder.code.ilike(f"%{search}%"), PurchaseOrder.note.ilike(f"%{search}%")))
        return query.order_by(PurchaseOrder.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_purchase_order(db: Session, payload: dict) -> PurchaseOrder:
        item = PurchaseOrder(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_purchase_order(db: Session, purchase_order_id: int, payload: dict) -> PurchaseOrder | None:
        item = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id, PurchaseOrder.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_purchase_order(db: Session, purchase_order_id: int) -> bool:
        item = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id, PurchaseOrder.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_goods_receipts(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(GoodsReceipt).filter(GoodsReceipt.company_id == company_id, GoodsReceipt.is_deleted.is_(False))
        if search:
            query = query.filter(or_(GoodsReceipt.code.ilike(f"%{search}%"), GoodsReceipt.note.ilike(f"%{search}%")))
        return query.order_by(GoodsReceipt.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_goods_receipt(db: Session, payload: dict) -> GoodsReceipt:
        item = GoodsReceipt(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_goods_receipt(db: Session, goods_receipt_id: int, payload: dict) -> GoodsReceipt | None:
        item = db.query(GoodsReceipt).filter(GoodsReceipt.id == goods_receipt_id, GoodsReceipt.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_goods_receipt(db: Session, goods_receipt_id: int) -> bool:
        item = db.query(GoodsReceipt).filter(GoodsReceipt.id == goods_receipt_id, GoodsReceipt.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_purchase_returns(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(PurchaseReturn).filter(PurchaseReturn.company_id == company_id, PurchaseReturn.is_deleted.is_(False))
        if search:
            query = query.filter(or_(PurchaseReturn.code.ilike(f"%{search}%"), PurchaseReturn.reason.ilike(f"%{search}%")))
        return query.order_by(PurchaseReturn.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_purchase_return(db: Session, payload: dict) -> PurchaseReturn:
        item = PurchaseReturn(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_purchase_return(db: Session, purchase_return_id: int, payload: dict) -> PurchaseReturn | None:
        item = db.query(PurchaseReturn).filter(PurchaseReturn.id == purchase_return_id, PurchaseReturn.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_purchase_return(db: Session, purchase_return_id: int) -> bool:
        item = db.query(PurchaseReturn).filter(PurchaseReturn.id == purchase_return_id, PurchaseReturn.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True
