from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.asset_assignment import AssetAssignment
from app.models.fixed_asset import FixedAsset


class AssetsService:
    @staticmethod
    def list_fixed_assets(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(FixedAsset).filter(FixedAsset.company_id == company_id, FixedAsset.is_deleted.is_(False))
        if search:
            query = query.filter(or_(FixedAsset.code.ilike(f"%{search}%"), FixedAsset.name.ilike(f"%{search}%")))
        return query.order_by(FixedAsset.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_fixed_asset(db: Session, payload: dict) -> FixedAsset:
        item = FixedAsset(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_fixed_asset(db: Session, asset_id: int, payload: dict) -> FixedAsset | None:
        item = db.query(FixedAsset).filter(FixedAsset.id == asset_id, FixedAsset.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_fixed_asset(db: Session, asset_id: int) -> bool:
        item = db.query(FixedAsset).filter(FixedAsset.id == asset_id, FixedAsset.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_asset_assignments(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(AssetAssignment).filter(AssetAssignment.company_id == company_id, AssetAssignment.is_deleted.is_(False))
        if search:
            query = query.filter(or_(AssetAssignment.status.ilike(f"%{search}%"), AssetAssignment.note.ilike(f"%{search}%")))
        return query.order_by(AssetAssignment.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_asset_assignment(db: Session, payload: dict) -> AssetAssignment:
        item = AssetAssignment(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_asset_assignment(db: Session, assignment_id: int, payload: dict) -> AssetAssignment | None:
        item = db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id, AssetAssignment.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_asset_assignment(db: Session, assignment_id: int) -> bool:
        item = db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id, AssetAssignment.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True
