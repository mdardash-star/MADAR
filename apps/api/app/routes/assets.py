from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.assets import (
    AssetAssignmentCreateRequest,
    AssetAssignmentUpdateRequest,
    FixedAssetCreateRequest,
    FixedAssetUpdateRequest,
)
from app.services.assets_service import AssetsService

router = APIRouter(prefix="/assets", tags=["assets"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/fixed-assets")
def list_fixed_assets(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in AssetsService.list_fixed_assets(db, company_id, skip, limit, search)]


@router.post("/fixed-assets", status_code=status.HTTP_201_CREATED)
def create_fixed_asset(payload: FixedAssetCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(AssetsService.create_fixed_asset(db, payload.model_dump()))


@router.put("/fixed-assets/{asset_id}")
def update_fixed_asset(asset_id: int, payload: FixedAssetUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = AssetsService.update_fixed_asset(db, asset_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fixed asset not found")
    return _serialize(item)


@router.delete("/fixed-assets/{asset_id}")
def delete_fixed_asset(asset_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = AssetsService.delete_fixed_asset(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fixed asset not found")
    return {"status": "deleted", "id": str(asset_id)}


@router.get("/assignments")
def list_asset_assignments(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in AssetsService.list_asset_assignments(db, company_id, skip, limit, search)]


@router.post("/assignments", status_code=status.HTTP_201_CREATED)
def create_asset_assignment(payload: AssetAssignmentCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(AssetsService.create_asset_assignment(db, payload.model_dump()))


@router.put("/assignments/{assignment_id}")
def update_asset_assignment(assignment_id: int, payload: AssetAssignmentUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = AssetsService.update_asset_assignment(db, assignment_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset assignment not found")
    return _serialize(item)


@router.delete("/assignments/{assignment_id}")
def delete_asset_assignment(assignment_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = AssetsService.delete_asset_assignment(db, assignment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset assignment not found")
    return {"status": "deleted", "id": str(assignment_id)}
