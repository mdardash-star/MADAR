from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import CompanyRegistrationRequest
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/register")
def register_company(payload: CompanyRegistrationRequest, db: Session = Depends(get_db)) -> dict:
    try:
        result = CompanyService.register_company(db, payload.model_dump())
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company registration failed: {exc}",
        ) from exc
    return result
