from pydantic import BaseModel, Field


class PurchaseOrderCreateRequest(BaseModel):
    company_id: int
    supplier_id: int
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    order_date: str | None = None
    expected_delivery_date: str | None = None
    status: str = "draft"
    currency_id: int | None = None
    subtotal_amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    discount_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    payment_status: str = "unpaid"
    note: str | None = None


class PurchaseOrderUpdateRequest(BaseModel):
    supplier_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    order_date: str | None = None
    expected_delivery_date: str | None = None
    status: str | None = None
    currency_id: int | None = None
    subtotal_amount: float | None = Field(default=None, ge=0)
    tax_amount: float | None = Field(default=None, ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    payment_status: str | None = None
    note: str | None = None


class GoodsReceiptCreateRequest(BaseModel):
    company_id: int
    purchase_order_id: int | None = None
    supplier_id: int
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    receipt_date: str | None = None
    status: str = "draft"
    quantity_received: float = Field(ge=0)
    subtotal_amount: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)
    note: str | None = None


class GoodsReceiptUpdateRequest(BaseModel):
    purchase_order_id: int | None = None
    supplier_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    receipt_date: str | None = None
    status: str | None = None
    quantity_received: float | None = Field(default=None, ge=0)
    subtotal_amount: float | None = Field(default=None, ge=0)
    tax_amount: float | None = Field(default=None, ge=0)
    total_amount: float | None = Field(default=None, ge=0)
    note: str | None = None


class PurchaseReturnCreateRequest(BaseModel):
    company_id: int
    supplier_id: int
    purchase_order_id: int | None = None
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    return_date: str | None = None
    reason: str | None = None
    status: str = "draft"
    total_amount: float = Field(ge=0)
    note: str | None = None


class PurchaseReturnUpdateRequest(BaseModel):
    supplier_id: int | None = None
    purchase_order_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    return_date: str | None = None
    reason: str | None = None
    status: str | None = None
    total_amount: float | None = Field(default=None, ge=0)
    note: str | None = None
