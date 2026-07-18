from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.permission import Permission
from app.models.role import Role
from app.models.role import role_permission_association
from app.models.user import User


class SeedService:
    @staticmethod
    def seed_initial_permissions(db: Session) -> None:
        permissions = [
            {"codename": "company.manage", "description": "Manage company settings"},
            {"codename": "branch.manage", "description": "Manage branches"},
            {"codename": "user.manage", "description": "Manage users"},
            {"codename": "rbac.manage", "description": "Manage roles and permissions"},
            {"codename": "audit.view", "description": "View audit events"},
        ]

        for item in permissions:
            exists = db.query(Permission).filter(Permission.codename == item["codename"]).first()
            if not exists:
                db.add(Permission(**item))

        db.commit()

    @staticmethod
    def seed_initial_roles(db: Session, company_id: int) -> Role:
        role = db.query(Role).filter(Role.company_id == company_id, Role.slug == "admin").first()
        if role is None:
            role = Role(company_id=company_id, name="Admin", slug="admin")
            db.add(role)
            db.flush()

        permissions = db.query(Permission).all()
        role.permissions = permissions
        db.commit()
        return role

    @staticmethod
    def seed_first_administrator(db: Session, company_id: int) -> User:
        admin = db.query(User).filter(User.company_id == company_id, User.email == "admin@madar.local").first()
        if admin is None:
            admin = User(
                company_id=company_id,
                email="admin@madar.local",
                full_name="System Administrator",
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
            )
            db.add(admin)
            db.flush()

            role = SeedService.seed_initial_roles(db, company_id)
            admin.role_id = role.id
            db.commit()
            db.refresh(admin)

        return admin
