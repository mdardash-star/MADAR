from pydantic import BaseModel, Field


class SalesQuotationCreateRequest(BaseModel):
    company_id: int
    customer_id: int
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    quote_date: str | None = None
    valid_until: str | None = None
    status: str = "draft"
    currency_id: int | None = None
    subtotal_amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    discount_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    note: str | None = None


class SalesQuotationUpdateRequest(BaseModel):
    customer_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    quote_date: str | None = None
    valid_until: str | None = None
    status: str | None = None
    currency_id: int | None = None
    subtotal_amount: float | None = Field(default=None, ge=0)
    tax_amount: float | None = Field(default=None, ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    note: str | None = None


class SalesOrderCreateRequest(BaseModel):
    company_id: int
    customer_id: int
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    order_date: str | None = None
    status: str = "draft"
    currency_id: int | None = None
    subtotal_amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    discount_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    payment_status: str = "unpaid"
    note: str | None = None


class SalesOrderUpdateRequest(BaseModel):
    customer_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    order_date: str | None = None
    status: str | None = None
    currency_id: int | None = None
    subtotal_amount: float | None = Field(default=None, ge=0)
    tax_amount: float | None = Field(default=None, ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    payment_status: str | None = None
    note: str | None = None


class SalesInvoiceCreateRequest(BaseModel):
    company_id: int
    customer_id: int
    order_id: int | None = None
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    invoice_date: str | None = None
    due_date: str | None = None
    status: str = "draft"
    currency_id: int | None = None
    subtotal_amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    discount_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    payment_status: str = "unpaid"
    note: str | None = None


class SalesInvoiceUpdateRequest(BaseModel):
    customer_id: int | None = None
    order_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    invoice_date: str | None = None
    due_date: str | None = None
    status: str | None = None
    currency_id: int | None = None
    subtotal_amount: float | None = Field(default=None, ge=0)
    tax_amount: float | None = Field(default=None, ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    payment_status: str | None = None
    note: str | None = None
