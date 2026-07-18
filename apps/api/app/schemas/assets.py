from pydantic import BaseModel, Field


class FixedAssetCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    warehouse_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    purchase_date: str | None = None
    cost: float = Field(ge=0)
    depreciation_rate: float = Field(ge=0)
    status: str = "active"
    note: str | None = None


class FixedAssetUpdateRequest(BaseModel):
    branch_id: int | None = None
    warehouse_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    purchase_date: str | None = None
    cost: float | None = Field(default=None, ge=0)
    depreciation_rate: float | None = Field(default=None, ge=0)
    status: str | None = None
    note: str | None = None


class AssetAssignmentCreateRequest(BaseModel):
    company_id: int
    asset_id: int
    employee_id: int | None = None
    branch_id: int | None = None
    assigned_date: str | None = None
    returned_date: str | None = None
    status: str = "assigned"
    note: str | None = None


class AssetAssignmentUpdateRequest(BaseModel):
    asset_id: int | None = None
    employee_id: int | None = None
    branch_id: int | None = None
    assigned_date: str | None = None
    returned_date: str | None = None
    status: str | None = None
    note: str | None = None
