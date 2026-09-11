from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_token_payload
from app.models.user import User
from app.schemas.customer_master import (
    AddressCreate,
    AddressUpdate,
    ContactCreate,
    ContactUpdate,
    CustomerCreate,
    CustomerUpdate,
)
from app.services.customer_master_service import CustomerMasterService

router = APIRouter(prefix="/master-data/customers", tags=["customers"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {
        key: value
        for key, value in instance.__dict__.items()
        if key != "_sa_instance_state"
    }


def _current_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> User:
    subject = payload.get("sub")
    if not subject or not isinstance(subject, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = (
        db.query(User)
        .filter(
            User.email == subject,
            User.is_deleted.is_(False),
            User.is_active.is_(True),
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or unknown user",
        )
    return user


def _permission_dependency(*permissions: str) -> Callable:
    def dependency(user: User = Depends(_current_user)) -> User:
        role = user.role
        if role and role.slug == "admin":
            return user
        granted = {permission.codename for permission in role.permissions} if role else set()
        if not granted.intersection(permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return dependency


read_customer = _permission_dependency("customers.read", "customers.write", "customers.delete")
write_customer = _permission_dependency("customers.write")
delete_customer_permission = _permission_dependency("customers.delete")


def _assert_company(user: User, company_id: int) -> None:
    if user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )


def _bad_request(exc: ValueError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("")
def list_customers(
    response: Response,
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    customer_type: str | None = Query(default=None, pattern="^(company|individual)$"),
    is_active: bool | None = None,
    include_archived: bool = False,
    with_meta: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(read_customer),
) -> Any:
    _assert_company(user, company_id)
    items, total = CustomerMasterService.list_customers(
        db,
        company_id,
        skip=skip,
        limit=limit,
        search=search,
        customer_type=customer_type,
        is_active=is_active,
        include_archived=include_archived,
    )
    response.headers["X-Total-Count"] = str(total)
    serialized = [_serialize(item) for item in items]
    if with_meta:
        return {"items": serialized, "total": total, "skip": skip, "limit": limit}
    return serialized


@router.post("", status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    _assert_company(user, payload.company_id)
    try:
        item = CustomerMasterService.create_customer(
            db,
            user.company_id,
            payload.model_dump(exclude={"company_id"}),
            user.email,
        )
    except ValueError as exc:
        raise _bad_request(exc) from exc
    return _serialize(item)


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    include_archived: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(read_customer),
) -> dict[str, Any]:
    item = CustomerMasterService.get_customer(
        db,
        user.company_id,
        customer_id,
        include_archived=include_archived,
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    result = _serialize(item)
    result["contacts"] = [
        _serialize(x)
        for x in CustomerMasterService.list_contacts(db, user.company_id, customer_id)
    ]
    result["addresses"] = [
        _serialize(x)
        for x in CustomerMasterService.list_addresses(db, user.company_id, customer_id)
    ]
    return result


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    try:
        item = CustomerMasterService.update_customer(
            db,
            user.company_id,
            customer_id,
            payload.model_dump(exclude_unset=True),
            user.email,
        )
    except ValueError as exc:
        raise _bad_request(exc) from exc
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return _serialize(item)


@router.delete("/{customer_id}")
def archive_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(delete_customer_permission),
) -> dict[str, str]:
    if not CustomerMasterService.archive_customer(
        db,
        user.company_id,
        customer_id,
        user.email,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return {"status": "archived", "id": str(customer_id)}


@router.post("/{customer_id}/restore")
def restore_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    try:
        item = CustomerMasterService.restore_customer(
            db,
            user.company_id,
            customer_id,
            user.email,
        )
    except ValueError as exc:
        raise _bad_request(exc) from exc
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archived customer not found",
        )
    return _serialize(item)


@router.post("/{customer_id}/contacts", status_code=status.HTTP_201_CREATED)
def create_contact(
    customer_id: int,
    payload: ContactCreate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    item = CustomerMasterService.create_contact(
        db,
        user.company_id,
        customer_id,
        payload.model_dump(),
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return _serialize(item)


@router.put("/{customer_id}/contacts/{contact_id}")
def update_contact(
    customer_id: int,
    contact_id: int,
    payload: ContactUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    item = CustomerMasterService.update_contact(
        db,
        user.company_id,
        customer_id,
        contact_id,
        payload.model_dump(exclude_unset=True),
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return _serialize(item)


@router.delete("/{customer_id}/contacts/{contact_id}")
def delete_contact(
    customer_id: int,
    contact_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, str]:
    if not CustomerMasterService.delete_contact(
        db,
        user.company_id,
        customer_id,
        contact_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return {"status": "deleted", "id": str(contact_id)}


@router.post("/{customer_id}/addresses", status_code=status.HTTP_201_CREATED)
def create_address(
    customer_id: int,
    payload: AddressCreate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    item = CustomerMasterService.create_address(
        db,
        user.company_id,
        customer_id,
        payload.model_dump(),
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return _serialize(item)


@router.put("/{customer_id}/addresses/{address_id}")
def update_address(
    customer_id: int,
    address_id: int,
    payload: AddressUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, Any]:
    item = CustomerMasterService.update_address(
        db,
        user.company_id,
        customer_id,
        address_id,
        payload.model_dump(exclude_unset=True),
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return _serialize(item)


@router.delete("/{customer_id}/addresses/{address_id}")
def delete_address(
    customer_id: int,
    address_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(write_customer),
) -> dict[str, str]:
    if not CustomerMasterService.delete_address(
        db,
        user.company_id,
        customer_id,
        address_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )
    return {"status": "deleted", "id": str(address_id)}
