from sqlalchemy.orm import Session

from app.core.audit import AuditLogger
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.user import User
from app.schemas.auth import TokenResponse


class AuthService:
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> TokenResponse:
        if not email or not password:
            raise ValueError("Email and password are required")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            AuditLogger.log_auth_event(db, user, "login_failed", "Incorrect password")
            raise ValueError("Invalid credentials")

        AuditLogger.log_auth_event(db, user, "login_succeeded", "JWT issued")
        access_token = create_access_token(subject=user.email)
        refresh_token = create_refresh_token(subject=user.email)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    def refresh_tokens(subject: str | None) -> TokenResponse:
        if not subject:
            raise ValueError("Invalid refresh token payload")

        access_token = create_access_token(subject=subject)
        refresh_token = create_refresh_token(subject=subject)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
