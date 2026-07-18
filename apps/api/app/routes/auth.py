from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.dependencies.auth import get_current_token_payload
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        tokens = AuthService.authenticate(db, payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return tokens


@router.post("/logout")
def logout(payload: dict = Depends(get_current_token_payload)) -> dict:
    return {"status": "ok", "message": f"User {payload.get('sub')} logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest) -> TokenResponse:
    try:
        token_payload = decode_token(payload.refresh_token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    if token_payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    return AuthService.refresh_tokens(token_payload.get("sub"))


@router.post("/password-reset")
def password_reset(payload: dict[str, str]) -> dict[str, str]:
    if not payload.get("email"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required")
    return {"status": "ok", "message": "Password reset instructions have been sent"}


@router.get("/me")
def current_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> dict:
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email, User.is_deleted.is_(False)).first()
    if not user:
        return {"sub": email, "type": payload.get("type")}
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "company_id": user.company_id,
        "company_name": user.company.name if user.company else None,
        "role_id": user.role_id,
        "is_active": user.is_active,
    }
