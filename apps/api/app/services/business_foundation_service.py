from datetime import datetime

from sqlalchemy.orm import Session

from app.models.barcode import Barcode
from app.models.brand import Brand
from app.models.cost_center import CostCenter
from app.models.customer_address import CustomerAddress
from app.models.customer_contact import CustomerContact
from app.models.customer_group import CustomerGroup
from app.models.product_image import ProductImage
from app.models.stock_opening_balance import StockOpeningBalance
from app.models.storage_location import StorageLocation
from app.models.supplier_address import SupplierAddress
from app.models.supplier_contact import SupplierContact


class BusinessFoundationService:
    @staticmethod
    def create_cost_center(db: Session, payload: dict) -> CostCenter:
        item = CostCenter(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_cost_centers(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(CostCenter).filter(CostCenter.company_id == company_id, CostCenter.is_deleted.is_(False))
        if search:
            query = query.filter((CostCenter.name.ilike(f"%{search}%")) | (CostCenter.code.ilike(f"%{search}%")))
        return query.order_by(CostCenter.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_cost_center(db: Session, cost_center_id: int, payload: dict) -> CostCenter | None:
        item = db.query(CostCenter).filter(CostCenter.id == cost_center_id, CostCenter.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_cost_center(db: Session, cost_center_id: int) -> bool:
        item = db.query(CostCenter).filter(CostCenter.id == cost_center_id, CostCenter.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_customer_group(db: Session, payload: dict) -> CustomerGroup:
        item = CustomerGroup(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_customer_groups(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(CustomerGroup).filter(CustomerGroup.company_id == company_id, CustomerGroup.is_deleted.is_(False))
        if search:
            query = query.filter((CustomerGroup.name.ilike(f"%{search}%")) | (CustomerGroup.code.ilike(f"%{search}%")))
        return query.order_by(CustomerGroup.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_customer_group(db: Session, group_id: int, payload: dict) -> CustomerGroup | None:
        item = db.query(CustomerGroup).filter(CustomerGroup.id == group_id, CustomerGroup.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_customer_group(db: Session, group_id: int) -> bool:
        item = db.query(CustomerGroup).filter(CustomerGroup.id == group_id, CustomerGroup.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_customer_contact(db: Session, payload: dict) -> CustomerContact:
        item = CustomerContact(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_customer_contacts(db: Session, company_id: int, customer_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(CustomerContact).filter(CustomerContact.company_id == company_id, CustomerContact.customer_id == customer_id, CustomerContact.is_deleted.is_(False))
        if search:
            query = query.filter(CustomerContact.full_name.ilike(f"%{search}%"))
        return query.order_by(CustomerContact.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_customer_contact(db: Session, contact_id: int, payload: dict) -> CustomerContact | None:
        item = db.query(CustomerContact).filter(CustomerContact.id == contact_id, CustomerContact.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_customer_contact(db: Session, contact_id: int) -> bool:
        item = db.query(CustomerContact).filter(CustomerContact.id == contact_id, CustomerContact.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_customer_address(db: Session, payload: dict) -> CustomerAddress:
        item = CustomerAddress(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_customer_addresses(db: Session, company_id: int, customer_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(CustomerAddress).filter(CustomerAddress.company_id == company_id, CustomerAddress.customer_id == customer_id, CustomerAddress.is_deleted.is_(False))
        if search:
            query = query.filter(CustomerAddress.label.ilike(f"%{search}%"))
        return query.order_by(CustomerAddress.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_customer_address(db: Session, address_id: int, payload: dict) -> CustomerAddress | None:
        item = db.query(CustomerAddress).filter(CustomerAddress.id == address_id, CustomerAddress.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_customer_address(db: Session, address_id: int) -> bool:
        item = db.query(CustomerAddress).filter(CustomerAddress.id == address_id, CustomerAddress.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_supplier_contact(db: Session, payload: dict) -> SupplierContact:
        item = SupplierContact(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_supplier_contacts(db: Session, company_id: int, supplier_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(SupplierContact).filter(SupplierContact.company_id == company_id, SupplierContact.supplier_id == supplier_id, SupplierContact.is_deleted.is_(False))
        if search:
            query = query.filter(SupplierContact.full_name.ilike(f"%{search}%"))
        return query.order_by(SupplierContact.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_supplier_contact(db: Session, contact_id: int, payload: dict) -> SupplierContact | None:
        item = db.query(SupplierContact).filter(SupplierContact.id == contact_id, SupplierContact.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_supplier_contact(db: Session, contact_id: int) -> bool:
        item = db.query(SupplierContact).filter(SupplierContact.id == contact_id, SupplierContact.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_supplier_address(db: Session, payload: dict) -> SupplierAddress:
        item = SupplierAddress(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_supplier_addresses(db: Session, company_id: int, supplier_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(SupplierAddress).filter(SupplierAddress.company_id == company_id, SupplierAddress.supplier_id == supplier_id, SupplierAddress.is_deleted.is_(False))
        if search:
            query = query.filter(SupplierAddress.label.ilike(f"%{search}%"))
        return query.order_by(SupplierAddress.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_supplier_address(db: Session, address_id: int, payload: dict) -> SupplierAddress | None:
        item = db.query(SupplierAddress).filter(SupplierAddress.id == address_id, SupplierAddress.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_supplier_address(db: Session, address_id: int) -> bool:
        item = db.query(SupplierAddress).filter(SupplierAddress.id == address_id, SupplierAddress.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_brand(db: Session, payload: dict) -> Brand:
        item = Brand(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_brands(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Brand).filter(Brand.company_id == company_id, Brand.is_deleted.is_(False))
        if search:
            query = query.filter((Brand.name.ilike(f"%{search}%")) | (Brand.code.ilike(f"%{search}%")))
        return query.order_by(Brand.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_brand(db: Session, brand_id: int, payload: dict) -> Brand | None:
        item = db.query(Brand).filter(Brand.id == brand_id, Brand.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_brand(db: Session, brand_id: int) -> bool:
        item = db.query(Brand).filter(Brand.id == brand_id, Brand.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_storage_location(db: Session, payload: dict) -> StorageLocation:
        item = StorageLocation(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_storage_locations(db: Session, company_id: int, warehouse_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(StorageLocation).filter(StorageLocation.company_id == company_id, StorageLocation.warehouse_id == warehouse_id, StorageLocation.is_deleted.is_(False))
        if search:
            query = query.filter((StorageLocation.name.ilike(f"%{search}%")) | (StorageLocation.code.ilike(f"%{search}%")))
        return query.order_by(StorageLocation.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_storage_location(db: Session, location_id: int, payload: dict) -> StorageLocation | None:
        item = db.query(StorageLocation).filter(StorageLocation.id == location_id, StorageLocation.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_storage_location(db: Session, location_id: int) -> bool:
        item = db.query(StorageLocation).filter(StorageLocation.id == location_id, StorageLocation.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_stock_opening_balance(db: Session, payload: dict) -> StockOpeningBalance:
        item = StockOpeningBalance(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_stock_opening_balances(db: Session, company_id: int, warehouse_id: int | None = None, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(StockOpeningBalance).filter(StockOpeningBalance.company_id == company_id, StockOpeningBalance.is_deleted.is_(False))
        if warehouse_id:
            query = query.filter(StockOpeningBalance.warehouse_id == warehouse_id)
        if search:
            query = query.filter(StockOpeningBalance.batch_no.ilike(f"%{search}%"))
        return query.order_by(StockOpeningBalance.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_stock_opening_balance(db: Session, balance_id: int, payload: dict) -> StockOpeningBalance | None:
        item = db.query(StockOpeningBalance).filter(StockOpeningBalance.id == balance_id, StockOpeningBalance.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_stock_opening_balance(db: Session, balance_id: int) -> bool:
        item = db.query(StockOpeningBalance).filter(StockOpeningBalance.id == balance_id, StockOpeningBalance.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_barcode(db: Session, payload: dict) -> Barcode:
        item = Barcode(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_barcodes(db: Session, company_id: int, product_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Barcode).filter(Barcode.company_id == company_id, Barcode.product_id == product_id, Barcode.is_deleted.is_(False))
        if search:
            query = query.filter(Barcode.code.ilike(f"%{search}%"))
        return query.order_by(Barcode.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_barcode(db: Session, barcode_id: int, payload: dict) -> Barcode | None:
        item = db.query(Barcode).filter(Barcode.id == barcode_id, Barcode.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_barcode(db: Session, barcode_id: int) -> bool:
        item = db.query(Barcode).filter(Barcode.id == barcode_id, Barcode.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_product_image(db: Session, payload: dict):
        item = ProductImage(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_product_images(db: Session, company_id: int, product_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(ProductImage).filter(ProductImage.company_id == company_id, ProductImage.product_id == product_id, ProductImage.is_deleted.is_(False))
        if search:
            query = query.filter(ProductImage.image_url.ilike(f"%{search}%"))
        return query.order_by(ProductImage.id).offset(skip).limit(limit).all()

    @staticmethod
    def update_product_image(db: Session, image_id: int, payload: dict):
        item = db.query(ProductImage).filter(ProductImage.id == image_id, ProductImage.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_product_image(db: Session, image_id: int) -> bool:
        item = db.query(ProductImage).filter(ProductImage.id == image_id, ProductImage.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True
