from pydantic import BaseModel, Field


# ── Lead ──────────────────────────────────────────────────────────────────────

class LeadCreateRequest(BaseModel):
    company_id: int
    full_name: str = Field(min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    company_name: str | None = Field(default=None, max_length=255)
    job_title: str | None = Field(default=None, max_length=100)
    source: str | None = Field(default=None, max_length=100)
    status: str = Field(default="new", max_length=50)
    assigned_to: int | None = None
    notes: str | None = None


class LeadUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    company_name: str | None = Field(default=None, max_length=255)
    job_title: str | None = Field(default=None, max_length=100)
    source: str | None = Field(default=None, max_length=100)
    status: str | None = Field(default=None, max_length=50)
    assigned_to: int | None = None
    notes: str | None = None


# ── Pipeline ──────────────────────────────────────────────────────────────────

class PipelineCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    is_default: bool = False


class PipelineUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_default: bool | None = None
    is_active: bool | None = None


# ── Stage ─────────────────────────────────────────────────────────────────────

class StageCreateRequest(BaseModel):
    company_id: int
    pipeline_id: int
    name: str = Field(min_length=1, max_length=100)
    sequence: int = Field(default=10, ge=0)
    probability: float = Field(default=0.0, ge=0.0, le=100.0)
    is_won: bool = False
    is_lost: bool = False


class StageUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    sequence: int | None = Field(default=None, ge=0)
    probability: float | None = Field(default=None, ge=0.0, le=100.0)
    is_won: bool | None = None
    is_lost: bool | None = None
    is_active: bool | None = None


# ── Opportunity ───────────────────────────────────────────────────────────────

class OpportunityCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    pipeline_id: int
    stage_id: int
    lead_id: int | None = None
    customer_id: int | None = None
    assigned_to: int | None = None
    expected_value: float = Field(default=0.0, ge=0.0)
    expected_close_date: str | None = None
    notes: str | None = None


class OpportunityUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    stage_id: int | None = None
    lead_id: int | None = None
    customer_id: int | None = None
    assigned_to: int | None = None
    expected_value: float | None = Field(default=None, ge=0.0)
    expected_close_date: str | None = None
    status: str | None = None
    notes: str | None = None


# ── Activity ──────────────────────────────────────────────────────────────────

class ActivityCreateRequest(BaseModel):
    company_id: int
    subject: str = Field(min_length=1, max_length=255)
    activity_type: str = Field(max_length=50)
    lead_id: int | None = None
    opportunity_id: int | None = None
    assigned_to: int | None = None
    due_date: str | None = None
    outcome: str | None = None
    status: str = Field(default="planned", max_length=50)


class ActivityUpdateRequest(BaseModel):
    subject: str | None = Field(default=None, min_length=1, max_length=255)
    activity_type: str | None = Field(default=None, max_length=50)
    assigned_to: int | None = None
    due_date: str | None = None
    outcome: str | None = None
    status: str | None = Field(default=None, max_length=50)


# ── Note ──────────────────────────────────────────────────────────────────────

class NoteCreateRequest(BaseModel):
    company_id: int
    content: str = Field(min_length=1)
    lead_id: int | None = None
    opportunity_id: int | None = None
    author_id: int | None = None


class NoteUpdateRequest(BaseModel):
    content: str | None = Field(default=None, min_length=1)
