from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_company_by_slug(db: Session, slug: str) -> Company | None:
        return db.query(Company).filter(Company.slug == slug).first()
