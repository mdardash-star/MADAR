from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.procurement import (
    GoodsReceiptCreateRequest,
    GoodsReceiptUpdateRequest,
    PurchaseOrderCreateRequest,
    PurchaseOrderUpdateRequest,
    PurchaseReturnCreateRequest,
    PurchaseReturnUpdateRequest,
)
from app.services.procurement_service import ProcurementService

router = APIRouter(prefix="/procurement", tags=["procurement"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/purchase-orders")
def list_purchase_orders(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in ProcurementService.list_purchase_orders(db, company_id, skip, limit, search)]


@router.post("/purchase-orders", status_code=status.HTTP_201_CREATED)
def create_purchase_order(payload: PurchaseOrderCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(ProcurementService.create_purchase_order(db, payload.model_dump()))


@router.put("/purchase-orders/{purchase_order_id}")
def update_purchase_order(purchase_order_id: int, payload: PurchaseOrderUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = ProcurementService.update_purchase_order(db, purchase_order_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    return _serialize(item)


@router.delete("/purchase-orders/{purchase_order_id}")
def delete_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = ProcurementService.delete_purchase_order(db, purchase_order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    return {"status": "deleted", "id": str(purchase_order_id)}


@router.get("/goods-receipts")
def list_goods_receipts(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in ProcurementService.list_goods_receipts(db, company_id, skip, limit, search)]


@router.post("/goods-receipts", status_code=status.HTTP_201_CREATED)
def create_goods_receipt(payload: GoodsReceiptCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(ProcurementService.create_goods_receipt(db, payload.model_dump()))


@router.put("/goods-receipts/{goods_receipt_id}")
def update_goods_receipt(goods_receipt_id: int, payload: GoodsReceiptUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = ProcurementService.update_goods_receipt(db, goods_receipt_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goods receipt not found")
    return _serialize(item)


@router.delete("/goods-receipts/{goods_receipt_id}")
def delete_goods_receipt(goods_receipt_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = ProcurementService.delete_goods_receipt(db, goods_receipt_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goods receipt not found")
    return {"status": "deleted", "id": str(goods_receipt_id)}


@router.get("/purchase-returns")
def list_purchase_returns(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in ProcurementService.list_purchase_returns(db, company_id, skip, limit, search)]


@router.post("/purchase-returns", status_code=status.HTTP_201_CREATED)
def create_purchase_return(payload: PurchaseReturnCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(ProcurementService.create_purchase_return(db, payload.model_dump()))


@router.put("/purchase-returns/{purchase_return_id}")
def update_purchase_return(purchase_return_id: int, payload: PurchaseReturnUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = ProcurementService.update_purchase_return(db, purchase_return_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase return not found")
    return _serialize(item)


@router.delete("/purchase-returns/{purchase_return_id}")
def delete_purchase_return(purchase_return_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = ProcurementService.delete_purchase_return(db, purchase_return_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase return not found")
    return {"status": "deleted", "id": str(purchase_return_id)}
