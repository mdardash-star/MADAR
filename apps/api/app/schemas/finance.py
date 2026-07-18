from pydantic import BaseModel, Field


class ChartOfAccountCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    parent_account_id: int | None = None
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    account_type: str = Field(default="asset", min_length=1, max_length=50)
    normal_balance: str = Field(default="debit", min_length=1, max_length=10)
    description: str | None = None
    is_active: bool = True


class ChartOfAccountUpdateRequest(BaseModel):
    branch_id: int | None = None
    parent_account_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    account_type: str | None = Field(default=None, min_length=1, max_length=50)
    normal_balance: str | None = Field(default=None, min_length=1, max_length=10)
    description: str | None = None
    is_active: bool | None = None


class JournalEntryCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    code: str = Field(min_length=1, max_length=100)
    entry_date: str | None = None
    reference_type: str | None = Field(default=None, max_length=50)
    reference_id: int | None = None
    status: str = "draft"
    note: str | None = None
    total_debit: float = Field(ge=0)
    total_credit: float = Field(ge=0)


class JournalEntryUpdateRequest(BaseModel):
    branch_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=100)
    entry_date: str | None = None
    reference_type: str | None = Field(default=None, max_length=50)
    reference_id: int | None = None
    status: str | None = None
    note: str | None = None
    total_debit: float | None = Field(default=None, ge=0)
    total_credit: float | None = Field(default=None, ge=0)
