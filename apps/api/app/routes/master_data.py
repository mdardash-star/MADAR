from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.master_data import (
    CurrencySettingCreateRequest,
    CurrencySettingUpdateRequest,
    CustomerCreateRequest,
    CustomerUpdateRequest,
    DepartmentCreateRequest,
    DepartmentUpdateRequest,
    ProductCategoryCreateRequest,
    ProductCategoryUpdateRequest,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductVariantCreateRequest,
    ProductVariantUpdateRequest,
    SupplierCreateRequest,
    SupplierUpdateRequest,
    TaxSettingCreateRequest,
    TaxSettingUpdateRequest,
    UnitOfMeasureCreateRequest,
    UnitOfMeasureUpdateRequest,
    WarehouseCreateRequest,
    WarehouseUpdateRequest,
)
from app.services.master_data_service import MasterDataService

router = APIRouter(prefix="/master-data", tags=["master-data"])


def _serialize(instance: Any) -> dict[str, Any]:
    payload = {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}
    return payload


@router.get("/departments")
def list_departments(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_departments(db, company_id, skip, limit, search)]


@router.post("/departments", status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_department(db, payload.model_dump())
    return _serialize(item)


@router.put("/departments/{department_id}")
def update_department(department_id: int, payload: DepartmentUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_department(db, department_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return _serialize(item)


@router.delete("/departments/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_department(db, department_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return {"status": "deleted", "id": str(department_id)}


@router.get("/warehouses")
def list_warehouses(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_warehouses(db, company_id, skip, limit, search)]


@router.post("/warehouses", status_code=status.HTTP_201_CREATED)
def create_warehouse(payload: WarehouseCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_warehouse(db, payload.model_dump())
    return _serialize(item)


@router.put("/warehouses/{warehouse_id}")
def update_warehouse(warehouse_id: int, payload: WarehouseUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_warehouse(db, warehouse_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return _serialize(item)


@router.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_warehouse(db, warehouse_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return {"status": "deleted", "id": str(warehouse_id)}


@router.get("/customers")
def list_customers(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_customers(db, company_id, skip, limit, search)]


@router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_customer(db, payload.model_dump())
    return _serialize(item)


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, payload: CustomerUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_customer(db, customer_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return _serialize(item)


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return {"status": "deleted", "id": str(customer_id)}


@router.get("/suppliers")
def list_suppliers(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_suppliers(db, company_id, skip, limit, search)]


@router.post("/suppliers", status_code=status.HTTP_201_CREATED)
def create_supplier(payload: SupplierCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_supplier(db, payload.model_dump())
    return _serialize(item)


@router.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, payload: SupplierUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_supplier(db, supplier_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return _serialize(item)


@router.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_supplier(db, supplier_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return {"status": "deleted", "id": str(supplier_id)}


@router.get("/product-categories")
def list_product_categories(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_product_categories(db, company_id, skip, limit, search)]


@router.post("/product-categories", status_code=status.HTTP_201_CREATED)
def create_product_category(payload: ProductCategoryCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_product_category(db, payload.model_dump())
    return _serialize(item)


@router.put("/product-categories/{category_id}")
def update_product_category(category_id: int, payload: ProductCategoryUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_product_category(db, category_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product category not found")
    return _serialize(item)


@router.delete("/product-categories/{category_id}")
def delete_product_category(category_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_product_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product category not found")
    return {"status": "deleted", "id": str(category_id)}


@router.get("/units-of-measure")
def list_units_of_measure(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_units_of_measure(db, company_id, skip, limit, search)]


@router.post("/units-of-measure", status_code=status.HTTP_201_CREATED)
def create_unit_of_measure(payload: UnitOfMeasureCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_unit_of_measure(db, payload.model_dump())
    return _serialize(item)


@router.put("/units-of-measure/{unit_id}")
def update_unit_of_measure(unit_id: int, payload: UnitOfMeasureUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_unit_of_measure(db, unit_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit of measure not found")
    return _serialize(item)


@router.delete("/units-of-measure/{unit_id}")
def delete_unit_of_measure(unit_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_unit_of_measure(db, unit_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit of measure not found")
    return {"status": "deleted", "id": str(unit_id)}


@router.get("/tax-settings")
def list_tax_settings(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_tax_settings(db, company_id, skip, limit, search)]


@router.post("/tax-settings", status_code=status.HTTP_201_CREATED)
def create_tax_setting(payload: TaxSettingCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_tax_setting(db, payload.model_dump())
    return _serialize(item)


@router.put("/tax-settings/{tax_id}")
def update_tax_setting(tax_id: int, payload: TaxSettingUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_tax_setting(db, tax_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax setting not found")
    return _serialize(item)


@router.delete("/tax-settings/{tax_id}")
def delete_tax_setting(tax_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_tax_setting(db, tax_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tax setting not found")
    return {"status": "deleted", "id": str(tax_id)}


@router.get("/currency-settings")
def list_currency_settings(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_currency_settings(db, company_id, skip, limit, search)]


@router.post("/currency-settings", status_code=status.HTTP_201_CREATED)
def create_currency_setting(payload: CurrencySettingCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_currency_setting(db, payload.model_dump())
    return _serialize(item)


@router.put("/currency-settings/{currency_id}")
def update_currency_setting(currency_id: int, payload: CurrencySettingUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_currency_setting(db, currency_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency setting not found")
    return _serialize(item)


@router.delete("/currency-settings/{currency_id}")
def delete_currency_setting(currency_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_currency_setting(db, currency_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency setting not found")
    return {"status": "deleted", "id": str(currency_id)}


@router.get("/products")
def list_products(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_products(db, company_id, skip, limit, search)]


@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_product(db, payload.model_dump())
    return _serialize(item)


@router.put("/products/{product_id}")
def update_product(product_id: int, payload: ProductUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_product(db, product_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return _serialize(item)


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"status": "deleted", "id": str(product_id)}


@router.get("/products/{product_id}/variants")
def list_product_variants(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in MasterDataService.list_product_variants(db, product_id, skip, limit, search)]


@router.post("/products/{product_id}/variants", status_code=status.HTTP_201_CREATED)
def create_product_variant(product_id: int, payload: ProductVariantCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.create_product_variant(db, {**payload.model_dump(), "product_id": product_id})
    return _serialize(item)


@router.put("/products/variants/{variant_id}")
def update_product_variant(variant_id: int, payload: ProductVariantUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = MasterDataService.update_product_variant(db, variant_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")
    return _serialize(item)


@router.delete("/products/variants/{variant_id}")
def delete_product_variant(variant_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = MasterDataService.delete_product_variant(db, variant_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product variant not found")
    return {"status": "deleted", "id": str(variant_id)}
