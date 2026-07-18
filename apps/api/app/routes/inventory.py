from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.inventory import (
    StockAdjustmentCreateRequest,
    StockAdjustmentUpdateRequest,
    StockMovementCreateRequest,
    StockMovementUpdateRequest,
    StockTransferCreateRequest,
    StockTransferUpdateRequest,
)
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/stock-movements")
def list_stock_movements(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in InventoryService.list_stock_movements(db, company_id, skip, limit, search)]


@router.post("/stock-movements", status_code=status.HTTP_201_CREATED)
def create_stock_movement(payload: StockMovementCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(InventoryService.create_stock_movement(db, payload.model_dump()))


@router.put("/stock-movements/{stock_movement_id}")
def update_stock_movement(stock_movement_id: int, payload: StockMovementUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = InventoryService.update_stock_movement(db, stock_movement_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
    return _serialize(item)


@router.delete("/stock-movements/{stock_movement_id}")
def delete_stock_movement(stock_movement_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = InventoryService.delete_stock_movement(db, stock_movement_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
    return {"status": "deleted", "id": str(stock_movement_id)}


@router.get("/stock-transfers")
def list_stock_transfers(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in InventoryService.list_stock_transfers(db, company_id, skip, limit, search)]


@router.post("/stock-transfers", status_code=status.HTTP_201_CREATED)
def create_stock_transfer(payload: StockTransferCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(InventoryService.create_stock_transfer(db, payload.model_dump()))


@router.put("/stock-transfers/{stock_transfer_id}")
def update_stock_transfer(stock_transfer_id: int, payload: StockTransferUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = InventoryService.update_stock_transfer(db, stock_transfer_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock transfer not found")
    return _serialize(item)


@router.delete("/stock-transfers/{stock_transfer_id}")
def delete_stock_transfer(stock_transfer_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = InventoryService.delete_stock_transfer(db, stock_transfer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock transfer not found")
    return {"status": "deleted", "id": str(stock_transfer_id)}


@router.get("/stock-adjustments")
def list_stock_adjustments(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in InventoryService.list_stock_adjustments(db, company_id, skip, limit, search)]


@router.post("/stock-adjustments", status_code=status.HTTP_201_CREATED)
def create_stock_adjustment(payload: StockAdjustmentCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(InventoryService.create_stock_adjustment(db, payload.model_dump()))


@router.put("/stock-adjustments/{stock_adjustment_id}")
def update_stock_adjustment(stock_adjustment_id: int, payload: StockAdjustmentUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = InventoryService.update_stock_adjustment(db, stock_adjustment_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock adjustment not found")
    return _serialize(item)


@router.delete("/stock-adjustments/{stock_adjustment_id}")
def delete_stock_adjustment(stock_adjustment_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = InventoryService.delete_stock_adjustment(db, stock_adjustment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock adjustment not found")
    return {"status": "deleted", "id": str(stock_adjustment_id)}
