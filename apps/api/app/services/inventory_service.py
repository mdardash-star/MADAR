from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.stock_adjustment import StockAdjustment
from app.models.stock_movement import StockMovement
from app.models.stock_transfer import StockTransfer


class InventoryService:
    @staticmethod
    def list_stock_movements(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(StockMovement).filter(StockMovement.company_id == company_id, StockMovement.is_deleted.is_(False))
        if search:
            query = query.filter(or_(StockMovement.movement_type.ilike(f"%{search}%"), StockMovement.note.ilike(f"%{search}%")))
        return query.order_by(StockMovement.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_stock_movement(db: Session, payload: dict) -> StockMovement:
        item = StockMovement(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_stock_movement(db: Session, stock_movement_id: int, payload: dict) -> StockMovement | None:
        item = db.query(StockMovement).filter(StockMovement.id == stock_movement_id, StockMovement.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_stock_movement(db: Session, stock_movement_id: int) -> bool:
        item = db.query(StockMovement).filter(StockMovement.id == stock_movement_id, StockMovement.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_stock_transfers(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(StockTransfer).filter(StockTransfer.company_id == company_id, StockTransfer.is_deleted.is_(False))
        if search:
            query = query.filter(or_(StockTransfer.code.ilike(f"%{search}%"), StockTransfer.note.ilike(f"%{search}%")))
        return query.order_by(StockTransfer.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_stock_transfer(db: Session, payload: dict) -> StockTransfer:
        item = StockTransfer(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_stock_transfer(db: Session, stock_transfer_id: int, payload: dict) -> StockTransfer | None:
        item = db.query(StockTransfer).filter(StockTransfer.id == stock_transfer_id, StockTransfer.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_stock_transfer(db: Session, stock_transfer_id: int) -> bool:
        item = db.query(StockTransfer).filter(StockTransfer.id == stock_transfer_id, StockTransfer.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_stock_adjustments(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(StockAdjustment).filter(StockAdjustment.company_id == company_id, StockAdjustment.is_deleted.is_(False))
        if search:
            query = query.filter(or_(StockAdjustment.code.ilike(f"%{search}%"), StockAdjustment.reason.ilike(f"%{search}%")))
        return query.order_by(StockAdjustment.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_stock_adjustment(db: Session, payload: dict) -> StockAdjustment:
        item = StockAdjustment(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_stock_adjustment(db: Session, stock_adjustment_id: int, payload: dict) -> StockAdjustment | None:
        item = db.query(StockAdjustment).filter(StockAdjustment.id == stock_adjustment_id, StockAdjustment.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_stock_adjustment(db: Session, stock_adjustment_id: int) -> bool:
        item = db.query(StockAdjustment).filter(StockAdjustment.id == stock_adjustment_id, StockAdjustment.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True
