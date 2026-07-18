from collections.abc import Sequence
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.models.customer import Customer
from app.models.currency_setting import CurrencySetting
from app.models.department import Department
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_variant import ProductVariant
from app.models.supplier import Supplier
from app.models.tax_setting import TaxSetting
from app.models.unit_of_measure import UnitOfMeasure
from app.models.warehouse import Warehouse


class MasterDataService:
    @staticmethod
    def _search_filter(model: type[Any], search: str | None):
        if not search:
            return None
        search_term = f"%{search.lower()}%"
        return or_(
            model.name.ilike(search_term),
            model.code.ilike(search_term),
            model.description.ilike(search_term),
        )

    @staticmethod
    def list_departments(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Department).filter(Department.company_id == company_id, Department.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Department.name.ilike(f"%{search}%"), Department.code.ilike(f"%{search}%")))
        return query.order_by(Department.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_department(db: Session, payload: dict) -> Department:
        instance = Department(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_department(db: Session, department_id: int, payload: dict) -> Department | None:
        instance = db.query(Department).filter(Department.id == department_id, Department.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_department(db: Session, department_id: int) -> bool:
        instance = db.query(Department).filter(Department.id == department_id, Department.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_warehouses(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Warehouse).filter(Warehouse.company_id == company_id, Warehouse.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Warehouse.name.ilike(f"%{search}%"), Warehouse.code.ilike(f"%{search}%")))
        return query.order_by(Warehouse.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_warehouse(db: Session, payload: dict) -> Warehouse:
        instance = Warehouse(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_warehouse(db: Session, warehouse_id: int, payload: dict) -> Warehouse | None:
        instance = db.query(Warehouse).filter(Warehouse.id == warehouse_id, Warehouse.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_warehouse(db: Session, warehouse_id: int) -> bool:
        instance = db.query(Warehouse).filter(Warehouse.id == warehouse_id, Warehouse.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_customers(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Customer).filter(Customer.company_id == company_id, Customer.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Customer.name.ilike(f"%{search}%"), Customer.code.ilike(f"%{search}%")))
        return query.order_by(Customer.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_customer(db: Session, payload: dict) -> Customer:
        instance = Customer(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_customer(db: Session, customer_id: int, payload: dict) -> Customer | None:
        instance = db.query(Customer).filter(Customer.id == customer_id, Customer.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        instance = db.query(Customer).filter(Customer.id == customer_id, Customer.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_suppliers(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Supplier).filter(Supplier.company_id == company_id, Supplier.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Supplier.name.ilike(f"%{search}%"), Supplier.code.ilike(f"%{search}%")))
        return query.order_by(Supplier.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_supplier(db: Session, payload: dict) -> Supplier:
        instance = Supplier(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_supplier(db: Session, supplier_id: int, payload: dict) -> Supplier | None:
        instance = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_supplier(db: Session, supplier_id: int) -> bool:
        instance = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_product_categories(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(ProductCategory).filter(ProductCategory.company_id == company_id, ProductCategory.is_deleted.is_(False))
        if search:
            query = query.filter(or_(ProductCategory.name.ilike(f"%{search}%"), ProductCategory.code.ilike(f"%{search}%")))
        return query.order_by(ProductCategory.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_product_category(db: Session, payload: dict) -> ProductCategory:
        instance = ProductCategory(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_product_category(db: Session, category_id: int, payload: dict) -> ProductCategory | None:
        instance = db.query(ProductCategory).filter(ProductCategory.id == category_id, ProductCategory.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_product_category(db: Session, category_id: int) -> bool:
        instance = db.query(ProductCategory).filter(ProductCategory.id == category_id, ProductCategory.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_units_of_measure(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(UnitOfMeasure).filter(UnitOfMeasure.company_id == company_id, UnitOfMeasure.is_deleted.is_(False))
        if search:
            query = query.filter(or_(UnitOfMeasure.name.ilike(f"%{search}%"), UnitOfMeasure.code.ilike(f"%{search}%")))
        return query.order_by(UnitOfMeasure.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_unit_of_measure(db: Session, payload: dict) -> UnitOfMeasure:
        instance = UnitOfMeasure(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_unit_of_measure(db: Session, unit_id: int, payload: dict) -> UnitOfMeasure | None:
        instance = db.query(UnitOfMeasure).filter(UnitOfMeasure.id == unit_id, UnitOfMeasure.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_unit_of_measure(db: Session, unit_id: int) -> bool:
        instance = db.query(UnitOfMeasure).filter(UnitOfMeasure.id == unit_id, UnitOfMeasure.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_tax_settings(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(TaxSetting).filter(TaxSetting.company_id == company_id, TaxSetting.is_deleted.is_(False))
        if search:
            query = query.filter(or_(TaxSetting.name.ilike(f"%{search}%"), TaxSetting.code.ilike(f"%{search}%")))
        return query.order_by(TaxSetting.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_tax_setting(db: Session, payload: dict) -> TaxSetting:
        instance = TaxSetting(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_tax_setting(db: Session, tax_id: int, payload: dict) -> TaxSetting | None:
        instance = db.query(TaxSetting).filter(TaxSetting.id == tax_id, TaxSetting.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_tax_setting(db: Session, tax_id: int) -> bool:
        instance = db.query(TaxSetting).filter(TaxSetting.id == tax_id, TaxSetting.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_currency_settings(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(CurrencySetting).filter(CurrencySetting.company_id == company_id, CurrencySetting.is_deleted.is_(False))
        if search:
            query = query.filter(or_(CurrencySetting.name.ilike(f"%{search}%"), CurrencySetting.code.ilike(f"%{search}%")))
        return query.order_by(CurrencySetting.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_currency_setting(db: Session, payload: dict) -> CurrencySetting:
        instance = CurrencySetting(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_currency_setting(db: Session, currency_id: int, payload: dict) -> CurrencySetting | None:
        instance = db.query(CurrencySetting).filter(CurrencySetting.id == currency_id, CurrencySetting.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_currency_setting(db: Session, currency_id: int) -> bool:
        instance = db.query(CurrencySetting).filter(CurrencySetting.id == currency_id, CurrencySetting.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_products(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Product).filter(Product.company_id == company_id, Product.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Product.name.ilike(f"%{search}%"), Product.sku.ilike(f"%{search}%"), Product.barcode.ilike(f"%{search}%")))
        return query.order_by(Product.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, payload: dict) -> Product:
        instance = Product(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_product(db: Session, product_id: int, payload: dict) -> Product | None:
        instance = db.query(Product).filter(Product.id == product_id, Product.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        instance = db.query(Product).filter(Product.id == product_id, Product.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_product_variants(db: Session, product_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(ProductVariant).filter(ProductVariant.product_id == product_id, ProductVariant.is_deleted.is_(False))
        if search:
            query = query.filter(or_(ProductVariant.name.ilike(f"%{search}%"), ProductVariant.sku.ilike(f"%{search}%")))
        return query.order_by(ProductVariant.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_product_variant(db: Session, payload: dict) -> ProductVariant:
        instance = ProductVariant(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_product_variant(db: Session, variant_id: int, payload: dict) -> ProductVariant | None:
        instance = db.query(ProductVariant).filter(ProductVariant.id == variant_id, ProductVariant.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_product_variant(db: Session, variant_id: int) -> bool:
        instance = db.query(ProductVariant).filter(ProductVariant.id == variant_id, ProductVariant.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def list_branches(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Branch).filter(Branch.company_id == company_id, Branch.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Branch.name.ilike(f"%{search}%"), Branch.code.ilike(f"%{search}%")))
        return query.order_by(Branch.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_branch(db: Session, payload: dict) -> Branch:
        instance = Branch(**payload)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def update_branch(db: Session, branch_id: int, payload: dict) -> Branch | None:
        instance = db.query(Branch).filter(Branch.id == branch_id, Branch.is_deleted.is_(False)).first()
        if not instance:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(instance, field, value)
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def delete_branch(db: Session, branch_id: int) -> bool:
        instance = db.query(Branch).filter(Branch.id == branch_id, Branch.is_deleted.is_(False)).first()
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = __import__("datetime").datetime.utcnow()
        db.commit()
        return True
