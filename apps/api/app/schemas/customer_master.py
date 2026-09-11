from typing import Literal

from pydantic import BaseModel, Field


CustomerType = Literal["company", "individual"]
AddressType = Literal["billing", "shipping", "other"]


class CustomerCreate(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    customer_type: CustomerType = "company"
    tax_number: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=255)
    branch_id: int | None = None
    customer_group_id: int | None = None
    sales_owner_id: int | None = None
    credit_limit: float = Field(default=0, ge=0)
    payment_terms_days: int = Field(default=0, ge=0)
    notes: str | None = Field(default=None, max_length=1000)
    is_active: bool = True


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    customer_type: CustomerType | None = None
    tax_number: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=255)
    branch_id: int | None = None
    customer_group_id: int | None = None
    sales_owner_id: int | None = None
    credit_limit: float | None = Field(default=None, ge=0)
    payment_terms_days: int | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None


class ContactCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    position: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    is_primary: bool = False
    is_active: bool = True


class ContactUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    is_primary: bool | None = None
    is_active: bool | None = None


class AddressCreate(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    address_type: AddressType = "other"
    street: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    is_primary: bool = False
    is_active: bool = True


class AddressUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=100)
    address_type: AddressType | None = None
    street: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    is_primary: bool | None = None
    is_active: bool | None = None
