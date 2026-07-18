from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.crm import (
    ActivityCreateRequest,
    ActivityUpdateRequest,
    LeadCreateRequest,
    LeadUpdateRequest,
    NoteCreateRequest,
    NoteUpdateRequest,
    OpportunityCreateRequest,
    OpportunityUpdateRequest,
    PipelineCreateRequest,
    PipelineUpdateRequest,
    StageCreateRequest,
    StageUpdateRequest,
)
from app.services.crm_service import CRMService

router = APIRouter(prefix="/crm", tags=["crm"])


def _s(obj: Any) -> dict[str, Any]:
    return {k: v for k, v in obj.__dict__.items() if k != "_sa_instance_state"}


# ── Leads ─────────────────────────────────────────────────────────────────────

@router.get("/leads")
def list_leads(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_s(i) for i in CRMService.list_leads(db, company_id, skip, limit, search, status)]


@router.post("/leads", status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_lead(db, payload.model_dump()))


@router.get("/leads/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.get_lead(db, lead_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return _s(item)


@router.put("/leads/{lead_id}")
def update_lead(lead_id: int, payload: LeadUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.update_lead(db, lead_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return _s(item)


@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_lead(db, lead_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return {"status": "deleted", "id": str(lead_id)}


# ── Pipelines ─────────────────────────────────────────────────────────────────

@router.get("/pipelines")
def list_pipelines(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_s(i) for i in CRMService.list_pipelines(db, company_id, skip, limit)]


@router.post("/pipelines", status_code=status.HTTP_201_CREATED)
def create_pipeline(payload: PipelineCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_pipeline(db, payload.model_dump()))


@router.get("/pipelines/{pipeline_id}")
def get_pipeline(pipeline_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.get_pipeline(db, pipeline_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return _s(item)


@router.put("/pipelines/{pipeline_id}")
def update_pipeline(pipeline_id: int, payload: PipelineUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.update_pipeline(db, pipeline_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return _s(item)


@router.delete("/pipelines/{pipeline_id}")
def delete_pipeline(pipeline_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_pipeline(db, pipeline_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return {"status": "deleted", "id": str(pipeline_id)}


# ── Stages ────────────────────────────────────────────────────────────────────

@router.get("/pipelines/{pipeline_id}/stages")
def list_stages(
    pipeline_id: int,
    company_id: int = Query(...),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_s(i) for i in CRMService.list_stages(db, company_id, pipeline_id)]


@router.post("/stages", status_code=status.HTTP_201_CREATED)
def create_stage(payload: StageCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_stage(db, payload.model_dump()))


@router.put("/stages/{stage_id}")
def update_stage(stage_id: int, payload: StageUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.update_stage(db, stage_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stage not found")
    return _s(item)


@router.delete("/stages/{stage_id}")
def delete_stage(stage_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_stage(db, stage_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stage not found")
    return {"status": "deleted", "id": str(stage_id)}


# ── Opportunities ─────────────────────────────────────────────────────────────

@router.get("/opportunities")
def list_opportunities(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    pipeline_id: int | None = None,
    stage_id: int | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [
        _s(i)
        for i in CRMService.list_opportunities(
            db, company_id, skip, limit, pipeline_id, stage_id, status_filter, search
        )
    ]


@router.post("/opportunities", status_code=status.HTTP_201_CREATED)
def create_opportunity(payload: OpportunityCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_opportunity(db, payload.model_dump()))


@router.get("/opportunities/{opportunity_id}")
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.get_opportunity(db, opportunity_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return _s(item)


@router.put("/opportunities/{opportunity_id}")
def update_opportunity(
    opportunity_id: int,
    payload: OpportunityUpdateRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    item = CRMService.update_opportunity(db, opportunity_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return _s(item)


@router.delete("/opportunities/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_opportunity(db, opportunity_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return {"status": "deleted", "id": str(opportunity_id)}


# ── Activities ────────────────────────────────────────────────────────────────

@router.get("/activities")
def list_activities(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    lead_id: int | None = None,
    opportunity_id: int | None = None,
    assigned_to: int | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [
        _s(i)
        for i in CRMService.list_activities(db, company_id, skip, limit, lead_id, opportunity_id, assigned_to)
    ]


@router.post("/activities", status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_activity(db, payload.model_dump()))


@router.get("/activities/{activity_id}")
def get_activity(activity_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.get_activity(db, activity_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return _s(item)


@router.put("/activities/{activity_id}")
def update_activity(
    activity_id: int,
    payload: ActivityUpdateRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    item = CRMService.update_activity(db, activity_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return _s(item)


@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_activity(db, activity_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return {"status": "deleted", "id": str(activity_id)}


# ── Notes ─────────────────────────────────────────────────────────────────────

@router.get("/notes")
def list_notes(
    company_id: int = Query(...),
    lead_id: int | None = None,
    opportunity_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_s(i) for i in CRMService.list_notes(db, company_id, lead_id, opportunity_id, skip, limit)]


@router.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _s(CRMService.create_note(db, payload.model_dump()))


@router.put("/notes/{note_id}")
def update_note(note_id: int, payload: NoteUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = CRMService.update_note(db, note_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return _s(item)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    if not CRMService.delete_note(db, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return {"status": "deleted", "id": str(note_id)}
