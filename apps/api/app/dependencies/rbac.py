from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_token_payload
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


class RBACChecker:
    @staticmethod
    def require_permission(permission: str):
        def dependency(payload: dict = Depends(get_current_token_payload)) -> dict:
            if payload.get("sub") is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
            return payload

        return dependency
