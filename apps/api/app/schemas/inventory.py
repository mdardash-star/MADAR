from pydantic import BaseModel, Field


class StockMovementCreateRequest(BaseModel):
    company_id: int
    product_id: int
    warehouse_id: int | None = None
    movement_type: str = Field(min_length=1, max_length=50)
    quantity: float = Field(ge=0)
    reference_type: str | None = Field(default=None, max_length=50)
    reference_id: int | None = None
    movement_date: str | None = None
    note: str | None = None


class StockMovementUpdateRequest(BaseModel):
    product_id: int | None = None
    warehouse_id: int | None = None
    movement_type: str | None = Field(default=None, min_length=1, max_length=50)
    quantity: float | None = Field(default=None, ge=0)
    reference_type: str | None = Field(default=None, max_length=50)
    reference_id: int | None = None
    movement_date: str | None = None
    note: str | None = None


class StockTransferCreateRequest(BaseModel):
    company_id: int
    from_warehouse_id: int
    to_warehouse_id: int
    product_id: int
    code: str = Field(min_length=1, max_length=100)
    transfer_date: str | None = None
    quantity: float = Field(ge=0)
    status: str = "draft"
    note: str | None = None


class StockTransferUpdateRequest(BaseModel):
    from_warehouse_id: int | None = None
    to_warehouse_id: int | None = None
    product_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    transfer_date: str | None = None
    quantity: float | None = Field(default=None, ge=0)
    status: str | None = None
    note: str | None = None


class StockAdjustmentCreateRequest(BaseModel):
    company_id: int
    product_id: int
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    adjustment_date: str | None = None
    adjustment_type: str = Field(min_length=1, max_length=50)
    quantity: float = Field(ge=0)
    reason: str | None = None
    note: str | None = None


class StockAdjustmentUpdateRequest(BaseModel):
    product_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    adjustment_date: str | None = None
    adjustment_type: str | None = Field(default=None, min_length=1, max_length=50)
    quantity: float | None = Field(default=None, ge=0)
    reason: str | None = None
    note: str | None = None
