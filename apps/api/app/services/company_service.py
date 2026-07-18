from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.models.branch import Branch
from app.models.company import Company
from app.models.role import Role
from app.models.user import User
from app.services.seed_service import SeedService


class CompanyService:
    @staticmethod
    def register_company(db: Session, payload: dict) -> dict:
        company = Company(
            name=payload["company_name"],
            slug=payload["company_slug"],
            legal_name=payload.get("legal_name"),
            email=payload.get("email"),
            phone=payload.get("phone"),
        )
        db.add(company)
        db.flush()

        primary_branch = Branch(
            company_id=company.id,
            name="Head Office",
            code=f"HO-{company.slug.upper()}",
            country="UAE",
            city="Abu Dhabi",
            timezone="Asia/Dubai",
        )
        db.add(primary_branch)
        db.flush()

        SeedService.seed_initial_permissions(db)
        admin_role = SeedService.seed_initial_roles(db, company.id)

        admin_user = User(
            company_id=company.id,
            branch_id=primary_branch.id,
            role_id=admin_role.id,
            email=payload["admin_email"],
            full_name=payload["admin_full_name"],
            hashed_password=get_password_hash(payload["admin_password"]),
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        access_token = create_access_token(subject=admin_user.email)
        refresh_token = create_refresh_token(subject=admin_user.email)
        return {
            "company": {
                "id": company.id,
                "name": company.name,
                "slug": company.slug,
            },
            "admin": {
                "id": admin_user.id,
                "email": admin_user.email,
                "full_name": admin_user.full_name,
            },
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
        }
