import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.branch import Branch
from app.models.customer import Customer
from app.models.customer_address import CustomerAddress
from app.models.customer_contact import CustomerContact
from app.models.customer_group import CustomerGroup
from app.models.user import User


class CustomerMasterService:
    @staticmethod
    def _audit(
        db: Session,
        *,
        company_id: int,
        user_email: str,
        event: str,
        entity_id: int | None,
        details: dict[str, Any] | None = None,
    ) -> None:
        payload = {"company_id": company_id, **(details or {})}
        db.add(
            AuditLog(
                entity_type="customer",
                entity_id=entity_id,
                event=event,
                user_email=user_email,
                details=json.dumps(payload, ensure_ascii=False, default=str),
            )
        )

    @staticmethod
    def _validate_relations(
        db: Session,
        company_id: int,
        payload: dict[str, Any],
    ) -> None:
        branch_id = payload.get("branch_id")
        if branch_id is not None:
            branch = (
                db.query(Branch)
                .filter(
                    Branch.id == branch_id,
                    Branch.company_id == company_id,
                    Branch.is_deleted.is_(False),
                )
                .first()
            )
            if not branch:
                raise ValueError("Invalid branch_id for this company")

        group_id = payload.get("customer_group_id")
        if group_id is not None:
            group = (
                db.query(CustomerGroup)
                .filter(
                    CustomerGroup.id == group_id,
                    CustomerGroup.company_id == company_id,
                    CustomerGroup.is_deleted.is_(False),
                )
                .first()
            )
            if not group:
                raise ValueError("Invalid customer_group_id for this company")

        owner_id = payload.get("sales_owner_id")
        if owner_id is not None:
            owner = (
                db.query(User)
                .filter(
                    User.id == owner_id,
                    User.company_id == company_id,
                    User.is_deleted.is_(False),
                    User.is_active.is_(True),
                )
                .first()
            )
            if not owner:
                raise ValueError("Invalid sales_owner_id for this company")

    @staticmethod
    def _validate_uniques(
        db: Session,
        company_id: int,
        *,
        code: str | None = None,
        tax_number: str | None = None,
        exclude_customer_id: int | None = None,
    ) -> None:
        if code:
            query = db.query(Customer).filter(
                Customer.company_id == company_id,
                Customer.code == code,
            )
            if exclude_customer_id is not None:
                query = query.filter(Customer.id != exclude_customer_id)
            if query.first():
                raise ValueError("Customer code already exists in this company")

        if tax_number:
            query = db.query(Customer).filter(
                Customer.company_id == company_id,
                Customer.tax_number == tax_number,
            )
            if exclude_customer_id is not None:
                query = query.filter(Customer.id != exclude_customer_id)
            if query.first():
                raise ValueError("Customer tax number already exists in this company")

    @staticmethod
    def list_customers(
        db: Session,
        company_id: int,
        *,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        customer_type: str | None = None,
        is_active: bool | None = None,
        include_archived: bool = False,
    ) -> tuple[list[Customer], int]:
        query = db.query(Customer).filter(Customer.company_id == company_id)
        if not include_archived:
            query = query.filter(Customer.is_deleted.is_(False))
        if search:
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Customer.name.ilike(term),
                    Customer.code.ilike(term),
                    Customer.email.ilike(term),
                    Customer.phone.ilike(term),
                    Customer.tax_number.ilike(term),
                )
            )
        if customer_type:
            query = query.filter(Customer.customer_type == customer_type)
        if is_active is not None:
            query = query.filter(Customer.is_active.is_(is_active))
        total = query.count()
        return query.order_by(Customer.id.desc()).offset(skip).limit(limit).all(), total

    @staticmethod
    def get_customer(
        db: Session,
        company_id: int,
        customer_id: int,
        include_archived: bool = False,
    ) -> Customer | None:
        query = db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.company_id == company_id,
        )
        if not include_archived:
            query = query.filter(Customer.is_deleted.is_(False))
        return query.first()

    @classmethod
    def create_customer(
        cls,
        db: Session,
        company_id: int,
        payload: dict[str, Any],
        user_email: str,
    ) -> Customer:
        cls._validate_relations(db, company_id, payload)
        cls._validate_uniques(
            db,
            company_id,
            code=payload.get("code"),
            tax_number=payload.get("tax_number"),
        )
        data = {**payload, "company_id": company_id}
        instance = Customer(**data)
        db.add(instance)
        db.flush()
        cls._audit(
            db,
            company_id=company_id,
            user_email=user_email,
            event="customer_created",
            entity_id=instance.id,
        )
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def update_customer(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        payload: dict[str, Any],
        user_email: str,
    ) -> Customer | None:
        instance = cls.get_customer(db, company_id, customer_id)
        if not instance:
            return None
        cls._validate_relations(db, company_id, payload)
        cls._validate_uniques(
            db,
            company_id,
            code=payload.get("code"),
            tax_number=payload.get("tax_number"),
            exclude_customer_id=customer_id,
        )
        changes: dict[str, Any] = {}
        for field, value in payload.items():
            old = getattr(instance, field)
            if old != value:
                changes[field] = {"from": old, "to": value}
                setattr(instance, field, value)
        cls._audit(
            db,
            company_id=company_id,
            user_email=user_email,
            event="customer_updated",
            entity_id=instance.id,
            details={"changes": changes},
        )
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def archive_customer(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        user_email: str,
    ) -> bool:
        instance = cls.get_customer(db, company_id, customer_id)
        if not instance:
            return False
        instance.is_deleted = True
        instance.deleted_at = datetime.now(UTC)
        cls._audit(
            db,
            company_id=company_id,
            user_email=user_email,
            event="customer_archived",
            entity_id=instance.id,
        )
        db.commit()
        return True

    @classmethod
    def restore_customer(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        user_email: str,
    ) -> Customer | None:
        instance = cls.get_customer(
            db,
            company_id,
            customer_id,
            include_archived=True,
        )
        if not instance or not instance.is_deleted:
            return None
        cls._validate_uniques(
            db,
            company_id,
            code=instance.code,
            tax_number=instance.tax_number,
            exclude_customer_id=instance.id,
        )
        instance.is_deleted = False
        instance.deleted_at = None
        cls._audit(
            db,
            company_id=company_id,
            user_email=user_email,
            event="customer_restored",
            entity_id=instance.id,
        )
        db.commit()
        db.refresh(instance)
        return instance

    @staticmethod
    def list_contacts(
        db: Session,
        company_id: int,
        customer_id: int,
    ) -> list[CustomerContact]:
        return (
            db.query(CustomerContact)
            .filter(
                CustomerContact.company_id == company_id,
                CustomerContact.customer_id == customer_id,
                CustomerContact.is_deleted.is_(False),
            )
            .order_by(CustomerContact.is_primary.desc(), CustomerContact.id)
            .all()
        )

    @classmethod
    def create_contact(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        payload: dict[str, Any],
    ) -> CustomerContact | None:
        if not cls.get_customer(db, company_id, customer_id):
            return None
        if payload.get("is_primary"):
            db.query(CustomerContact).filter(
                CustomerContact.company_id == company_id,
                CustomerContact.customer_id == customer_id,
                CustomerContact.is_deleted.is_(False),
            ).update({CustomerContact.is_primary: False}, synchronize_session=False)
        item = CustomerContact(company_id=company_id, customer_id=customer_id, **payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @classmethod
    def update_contact(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        contact_id: int,
        payload: dict[str, Any],
    ) -> CustomerContact | None:
        item = (
            db.query(CustomerContact)
            .filter(
                CustomerContact.id == contact_id,
                CustomerContact.company_id == company_id,
                CustomerContact.customer_id == customer_id,
                CustomerContact.is_deleted.is_(False),
            )
            .first()
        )
        if not item:
            return None
        if payload.get("is_primary"):
            db.query(CustomerContact).filter(
                CustomerContact.company_id == company_id,
                CustomerContact.customer_id == customer_id,
                CustomerContact.id != contact_id,
                CustomerContact.is_deleted.is_(False),
            ).update({CustomerContact.is_primary: False}, synchronize_session=False)
        for field, value in payload.items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_contact(
        db: Session,
        company_id: int,
        customer_id: int,
        contact_id: int,
    ) -> bool:
        item = (
            db.query(CustomerContact)
            .filter(
                CustomerContact.id == contact_id,
                CustomerContact.company_id == company_id,
                CustomerContact.customer_id == customer_id,
                CustomerContact.is_deleted.is_(False),
            )
            .first()
        )
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(UTC)
        db.commit()
        return True

    @staticmethod
    def list_addresses(
        db: Session,
        company_id: int,
        customer_id: int,
    ) -> list[CustomerAddress]:
        return (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.company_id == company_id,
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_deleted.is_(False),
            )
            .order_by(CustomerAddress.is_primary.desc(), CustomerAddress.id)
            .all()
        )

    @classmethod
    def create_address(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        payload: dict[str, Any],
    ) -> CustomerAddress | None:
        if not cls.get_customer(db, company_id, customer_id):
            return None
        if payload.get("is_primary"):
            db.query(CustomerAddress).filter(
                CustomerAddress.company_id == company_id,
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_deleted.is_(False),
            ).update({CustomerAddress.is_primary: False}, synchronize_session=False)
        item = CustomerAddress(company_id=company_id, customer_id=customer_id, **payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @classmethod
    def update_address(
        cls,
        db: Session,
        company_id: int,
        customer_id: int,
        address_id: int,
        payload: dict[str, Any],
    ) -> CustomerAddress | None:
        item = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.id == address_id,
                CustomerAddress.company_id == company_id,
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_deleted.is_(False),
            )
            .first()
        )
        if not item:
            return None
        if payload.get("is_primary"):
            db.query(CustomerAddress).filter(
                CustomerAddress.company_id == company_id,
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.id != address_id,
                CustomerAddress.is_deleted.is_(False),
            ).update({CustomerAddress.is_primary: False}, synchronize_session=False)
        for field, value in payload.items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_address(
        db: Session,
        company_id: int,
        customer_id: int,
        address_id: int,
    ) -> bool:
        item = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.id == address_id,
                CustomerAddress.company_id == company_id,
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_deleted.is_(False),
            )
            .first()
        )
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(UTC)
        db.commit()
        return True
