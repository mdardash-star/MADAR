from datetime import datetime

from sqlalchemy.orm import Session

from app.models.crm_activity import CrmActivity, CrmNote
from app.models.crm_lead import CrmLead
from app.models.crm_opportunity import CrmOpportunity
from app.models.crm_pipeline import CrmPipeline, CrmStage


class CRMService:
    # ── Leads ─────────────────────────────────────────────────────────────────

    @staticmethod
    def create_lead(db: Session, payload: dict) -> CrmLead:
        item = CrmLead(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_leads(
        db: Session,
        company_id: int,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        status: str | None = None,
    ):
        q = db.query(CrmLead).filter(
            CrmLead.company_id == company_id,
            CrmLead.is_deleted.is_(False),
        )
        if status:
            q = q.filter(CrmLead.status == status)
        if search:
            q = q.filter(
                CrmLead.full_name.ilike(f"%{search}%")
                | CrmLead.email.ilike(f"%{search}%")
                | CrmLead.company_name.ilike(f"%{search}%")
            )
        return q.order_by(CrmLead.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_lead(db: Session, lead_id: int) -> CrmLead | None:
        return db.query(CrmLead).filter(CrmLead.id == lead_id, CrmLead.is_deleted.is_(False)).first()

    @staticmethod
    def update_lead(db: Session, lead_id: int, payload: dict) -> CrmLead | None:
        item = CRMService.get_lead(db, lead_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_lead(db: Session, lead_id: int) -> bool:
        item = CRMService.get_lead(db, lead_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    # ── Pipelines ─────────────────────────────────────────────────────────────

    @staticmethod
    def create_pipeline(db: Session, payload: dict) -> CrmPipeline:
        item = CrmPipeline(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_pipelines(db: Session, company_id: int, skip: int = 0, limit: int = 50):
        return (
            db.query(CrmPipeline)
            .filter(CrmPipeline.company_id == company_id, CrmPipeline.is_deleted.is_(False))
            .order_by(CrmPipeline.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_pipeline(db: Session, pipeline_id: int) -> CrmPipeline | None:
        return (
            db.query(CrmPipeline)
            .filter(CrmPipeline.id == pipeline_id, CrmPipeline.is_deleted.is_(False))
            .first()
        )

    @staticmethod
    def update_pipeline(db: Session, pipeline_id: int, payload: dict) -> CrmPipeline | None:
        item = CRMService.get_pipeline(db, pipeline_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_pipeline(db: Session, pipeline_id: int) -> bool:
        item = CRMService.get_pipeline(db, pipeline_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    # ── Stages ────────────────────────────────────────────────────────────────

    @staticmethod
    def create_stage(db: Session, payload: dict) -> CrmStage:
        item = CrmStage(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_stages(db: Session, company_id: int, pipeline_id: int):
        return (
            db.query(CrmStage)
            .filter(
                CrmStage.company_id == company_id,
                CrmStage.pipeline_id == pipeline_id,
                CrmStage.is_deleted.is_(False),
            )
            .order_by(CrmStage.sequence)
            .all()
        )

    @staticmethod
    def get_stage(db: Session, stage_id: int) -> CrmStage | None:
        return (
            db.query(CrmStage)
            .filter(CrmStage.id == stage_id, CrmStage.is_deleted.is_(False))
            .first()
        )

    @staticmethod
    def update_stage(db: Session, stage_id: int, payload: dict) -> CrmStage | None:
        item = CRMService.get_stage(db, stage_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_stage(db: Session, stage_id: int) -> bool:
        item = CRMService.get_stage(db, stage_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    # ── Opportunities ─────────────────────────────────────────────────────────

    @staticmethod
    def create_opportunity(db: Session, payload: dict) -> CrmOpportunity:
        item = CrmOpportunity(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_opportunities(
        db: Session,
        company_id: int,
        skip: int = 0,
        limit: int = 50,
        pipeline_id: int | None = None,
        stage_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
    ):
        q = db.query(CrmOpportunity).filter(
            CrmOpportunity.company_id == company_id,
            CrmOpportunity.is_deleted.is_(False),
        )
        if pipeline_id:
            q = q.filter(CrmOpportunity.pipeline_id == pipeline_id)
        if stage_id:
            q = q.filter(CrmOpportunity.stage_id == stage_id)
        if status:
            q = q.filter(CrmOpportunity.status == status)
        if search:
            q = q.filter(CrmOpportunity.name.ilike(f"%{search}%"))
        return q.order_by(CrmOpportunity.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_opportunity(db: Session, opportunity_id: int) -> CrmOpportunity | None:
        return (
            db.query(CrmOpportunity)
            .filter(CrmOpportunity.id == opportunity_id, CrmOpportunity.is_deleted.is_(False))
            .first()
        )

    @staticmethod
    def update_opportunity(db: Session, opportunity_id: int, payload: dict) -> CrmOpportunity | None:
        item = CRMService.get_opportunity(db, opportunity_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_opportunity(db: Session, opportunity_id: int) -> bool:
        item = CRMService.get_opportunity(db, opportunity_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    # ── Activities ────────────────────────────────────────────────────────────

    @staticmethod
    def create_activity(db: Session, payload: dict) -> CrmActivity:
        item = CrmActivity(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_activities(
        db: Session,
        company_id: int,
        skip: int = 0,
        limit: int = 50,
        lead_id: int | None = None,
        opportunity_id: int | None = None,
        assigned_to: int | None = None,
    ):
        q = db.query(CrmActivity).filter(
            CrmActivity.company_id == company_id,
            CrmActivity.is_deleted.is_(False),
        )
        if lead_id:
            q = q.filter(CrmActivity.lead_id == lead_id)
        if opportunity_id:
            q = q.filter(CrmActivity.opportunity_id == opportunity_id)
        if assigned_to:
            q = q.filter(CrmActivity.assigned_to == assigned_to)
        return q.order_by(CrmActivity.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_activity(db: Session, activity_id: int) -> CrmActivity | None:
        return (
            db.query(CrmActivity)
            .filter(CrmActivity.id == activity_id, CrmActivity.is_deleted.is_(False))
            .first()
        )

    @staticmethod
    def update_activity(db: Session, activity_id: int, payload: dict) -> CrmActivity | None:
        item = CRMService.get_activity(db, activity_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_activity(db: Session, activity_id: int) -> bool:
        item = CRMService.get_activity(db, activity_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True

    # ── Notes ─────────────────────────────────────────────────────────────────

    @staticmethod
    def create_note(db: Session, payload: dict) -> CrmNote:
        item = CrmNote(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_notes(
        db: Session,
        company_id: int,
        lead_id: int | None = None,
        opportunity_id: int | None = None,
        skip: int = 0,
        limit: int = 50,
    ):
        q = db.query(CrmNote).filter(
            CrmNote.company_id == company_id,
            CrmNote.is_deleted.is_(False),
        )
        if lead_id:
            q = q.filter(CrmNote.lead_id == lead_id)
        if opportunity_id:
            q = q.filter(CrmNote.opportunity_id == opportunity_id)
        return q.order_by(CrmNote.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_note(db: Session, note_id: int) -> CrmNote | None:
        return (
            db.query(CrmNote)
            .filter(CrmNote.id == note_id, CrmNote.is_deleted.is_(False))
            .first()
        )

    @staticmethod
    def update_note(db: Session, note_id: int, payload: dict) -> CrmNote | None:
        item = CRMService.get_note(db, note_id)
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_note(db: Session, note_id: int) -> bool:
        item = CRMService.get_note(db, note_id)
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        db.commit()
        return True
