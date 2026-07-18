from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.business_foundation import (
    BarcodeCreateRequest,
    BarcodeUpdateRequest,
    BrandCreateRequest,
    BrandUpdateRequest,
    CostCenterCreateRequest,
    CostCenterUpdateRequest,
    CustomerAddressCreateRequest,
    CustomerAddressUpdateRequest,
    CustomerContactCreateRequest,
    CustomerContactUpdateRequest,
    CustomerGroupCreateRequest,
    CustomerGroupUpdateRequest,
    ProductImageCreateRequest,
    ProductImageUpdateRequest,
    StockOpeningBalanceCreateRequest,
    StockOpeningBalanceUpdateRequest,
    StorageLocationCreateRequest,
    StorageLocationUpdateRequest,
    SupplierAddressCreateRequest,
    SupplierAddressUpdateRequest,
    SupplierContactCreateRequest,
    SupplierContactUpdateRequest,
)
from app.services.business_foundation_service import BusinessFoundationService

router = APIRouter(prefix="/business-foundation", tags=["business-foundation"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/cost-centers")
def list_cost_centers(company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_cost_centers(db, company_id, skip, limit, search)]


@router.post("/cost-centers", status_code=status.HTTP_201_CREATED)
def create_cost_center(payload: CostCenterCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_cost_center(db, payload.model_dump()))


@router.put("/cost-centers/{cost_center_id}")
def update_cost_center(cost_center_id: int, payload: CostCenterUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_cost_center(db, cost_center_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost center not found")
    return _serialize(item)


@router.delete("/cost-centers/{cost_center_id}")
def delete_cost_center(cost_center_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_cost_center(db, cost_center_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost center not found")
    return {"status": "deleted", "id": str(cost_center_id)}


@router.get("/customer-groups")
def list_customer_groups(company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_customer_groups(db, company_id, skip, limit, search)]


@router.post("/customer-groups", status_code=status.HTTP_201_CREATED)
def create_customer_group(payload: CustomerGroupCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_customer_group(db, payload.model_dump()))


@router.put("/customer-groups/{group_id}")
def update_customer_group(group_id: int, payload: CustomerGroupUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_customer_group(db, group_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer group not found")
    return _serialize(item)


@router.delete("/customer-groups/{group_id}")
def delete_customer_group(group_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_customer_group(db, group_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer group not found")
    return {"status": "deleted", "id": str(group_id)}


@router.get("/customers/{customer_id}/contacts")
def list_customer_contacts(customer_id: int, company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_customer_contacts(db, company_id, customer_id, skip, limit, search)]


@router.post("/customers/{customer_id}/contacts", status_code=status.HTTP_201_CREATED)
def create_customer_contact(customer_id: int, payload: CustomerContactCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_customer_contact(db, {**payload.model_dump(), "customer_id": customer_id}))


@router.put("/customers/contacts/{contact_id}")
def update_customer_contact(contact_id: int, payload: CustomerContactUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_customer_contact(db, contact_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer contact not found")
    return _serialize(item)


@router.delete("/customers/contacts/{contact_id}")
def delete_customer_contact(contact_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_customer_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer contact not found")
    return {"status": "deleted", "id": str(contact_id)}


@router.get("/customers/{customer_id}/addresses")
def list_customer_addresses(customer_id: int, company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_customer_addresses(db, company_id, customer_id, skip, limit, search)]


@router.post("/customers/{customer_id}/addresses", status_code=status.HTTP_201_CREATED)
def create_customer_address(customer_id: int, payload: CustomerAddressCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_customer_address(db, {**payload.model_dump(), "customer_id": customer_id}))


@router.put("/customers/addresses/{address_id}")
def update_customer_address(address_id: int, payload: CustomerAddressUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_customer_address(db, address_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer address not found")
    return _serialize(item)


@router.delete("/customers/addresses/{address_id}")
def delete_customer_address(address_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_customer_address(db, address_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer address not found")
    return {"status": "deleted", "id": str(address_id)}


@router.get("/suppliers/{supplier_id}/contacts")
def list_supplier_contacts(supplier_id: int, company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_supplier_contacts(db, company_id, supplier_id, skip, limit, search)]


@router.post("/suppliers/{supplier_id}/contacts", status_code=status.HTTP_201_CREATED)
def create_supplier_contact(supplier_id: int, payload: SupplierContactCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_supplier_contact(db, {**payload.model_dump(), "supplier_id": supplier_id}))


@router.put("/suppliers/contacts/{contact_id}")
def update_supplier_contact(contact_id: int, payload: SupplierContactUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_supplier_contact(db, contact_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier contact not found")
    return _serialize(item)


@router.delete("/suppliers/contacts/{contact_id}")
def delete_supplier_contact(contact_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_supplier_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier contact not found")
    return {"status": "deleted", "id": str(contact_id)}


@router.get("/suppliers/{supplier_id}/addresses")
def list_supplier_addresses(supplier_id: int, company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_supplier_addresses(db, company_id, supplier_id, skip, limit, search)]


@router.post("/suppliers/{supplier_id}/addresses", status_code=status.HTTP_201_CREATED)
def create_supplier_address(supplier_id: int, payload: SupplierAddressCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_supplier_address(db, {**payload.model_dump(), "supplier_id": supplier_id}))


@router.put("/suppliers/addresses/{address_id}")
def update_supplier_address(address_id: int, payload: SupplierAddressUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_supplier_address(db, address_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier address not found")
    return _serialize(item)


@router.delete("/suppliers/addresses/{address_id}")
def delete_supplier_address(address_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_supplier_address(db, address_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier address not found")
    return {"status": "deleted", "id": str(address_id)}


@router.get("/brands")
def list_brands(company_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_brands(db, company_id, skip, limit, search)]


@router.post("/brands", status_code=status.HTTP_201_CREATED)
def create_brand(payload: BrandCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_brand(db, payload.model_dump()))


@router.put("/brands/{brand_id}")
def update_brand(brand_id: int, payload: BrandUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_brand(db, brand_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return _serialize(item)


@router.delete("/brands/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_brand(db, brand_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return {"status": "deleted", "id": str(brand_id)}


@router.get("/storage-locations")
def list_storage_locations(company_id: int = Query(...), warehouse_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_storage_locations(db, company_id, warehouse_id, skip, limit, search)]


@router.post("/storage-locations", status_code=status.HTTP_201_CREATED)
def create_storage_location(payload: StorageLocationCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_storage_location(db, payload.model_dump()))


@router.put("/storage-locations/{location_id}")
def update_storage_location(location_id: int, payload: StorageLocationUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_storage_location(db, location_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storage location not found")
    return _serialize(item)


@router.delete("/storage-locations/{location_id}")
def delete_storage_location(location_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_storage_location(db, location_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storage location not found")
    return {"status": "deleted", "id": str(location_id)}


@router.get("/stock-opening-balances")
def list_stock_opening_balances(company_id: int = Query(...), warehouse_id: int | None = None, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_stock_opening_balances(db, company_id, warehouse_id, skip, limit, search)]


@router.post("/stock-opening-balances", status_code=status.HTTP_201_CREATED)
def create_stock_opening_balance(payload: StockOpeningBalanceCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_stock_opening_balance(db, payload.model_dump()))


@router.put("/stock-opening-balances/{balance_id}")
def update_stock_opening_balance(balance_id: int, payload: StockOpeningBalanceUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_stock_opening_balance(db, balance_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock opening balance not found")
    return _serialize(item)


@router.delete("/stock-opening-balances/{balance_id}")
def delete_stock_opening_balance(balance_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_stock_opening_balance(db, balance_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock opening balance not found")
    return {"status": "deleted", "id": str(balance_id)}


@router.get("/barcodes")
def list_barcodes(company_id: int = Query(...), product_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_barcodes(db, company_id, product_id, skip, limit, search)]


@router.post("/barcodes", status_code=status.HTTP_201_CREATED)
def create_barcode(payload: BarcodeCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_barcode(db, payload.model_dump()))


@router.put("/barcodes/{barcode_id}")
def update_barcode(barcode_id: int, payload: BarcodeUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_barcode(db, barcode_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barcode not found")
    return _serialize(item)


@router.delete("/barcodes/{barcode_id}")
def delete_barcode(barcode_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_barcode(db, barcode_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barcode not found")
    return {"status": "deleted", "id": str(barcode_id)}


@router.get("/product-images")
def list_product_images(company_id: int = Query(...), product_id: int = Query(...), skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200), search: str | None = None, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    return [_serialize(item) for item in BusinessFoundationService.list_product_images(db, company_id, product_id, skip, limit, search)]


@router.post("/product-images", status_code=status.HTTP_201_CREATED)
def create_product_image(payload: ProductImageCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(BusinessFoundationService.create_product_image(db, payload.model_dump()))


@router.put("/product-images/{image_id}")
def update_product_image(image_id: int, payload: ProductImageUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = BusinessFoundationService.update_product_image(db, image_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")
    return _serialize(item)


@router.delete("/product-images/{image_id}")
def delete_product_image(image_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = BusinessFoundationService.delete_product_image(db, image_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")
    return {"status": "deleted", "id": str(image_id)}
