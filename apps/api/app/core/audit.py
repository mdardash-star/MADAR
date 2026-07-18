from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User


class AuditLogger:
    @staticmethod
    def log_auth_event(db: Session, user: User, event: str, details: str | None = None) -> None:
        audit_entry = {
            "event": event,
            "user_email": user.email,
            "details": details or "",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        db.add(user)
        db.flush()
        # Replace with a persistent audit table in production.
        return audit_entry
