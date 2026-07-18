from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_token_payload
from app.models.user import User

router = APIRouter(prefix="/me", tags=["me"])


@router.get("")
def current_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> dict:
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "company_id": user.company_id,
        "branch_id": user.branch_id,
        "role_id": user.role_id,
    }
