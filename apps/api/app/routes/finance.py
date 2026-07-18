from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.finance import (
    ChartOfAccountCreateRequest,
    ChartOfAccountUpdateRequest,
    JournalEntryCreateRequest,
    JournalEntryUpdateRequest,
)
from app.services.finance_service import FinanceService

router = APIRouter(prefix="/finance", tags=["finance"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/chart-of-accounts")
def list_chart_of_accounts(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in FinanceService.list_chart_of_accounts(db, company_id, skip, limit, search)]


@router.post("/chart-of-accounts", status_code=status.HTTP_201_CREATED)
def create_chart_of_account(payload: ChartOfAccountCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(FinanceService.create_chart_of_account(db, payload.model_dump()))


@router.put("/chart-of-accounts/{account_id}")
def update_chart_of_account(account_id: int, payload: ChartOfAccountUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = FinanceService.update_chart_of_account(db, account_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart of account not found")
    return _serialize(item)


@router.delete("/chart-of-accounts/{account_id}")
def delete_chart_of_account(account_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = FinanceService.delete_chart_of_account(db, account_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart of account not found")
    return {"status": "deleted", "id": str(account_id)}


@router.get("/journal-entries")
def list_journal_entries(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in FinanceService.list_journal_entries(db, company_id, skip, limit, search)]


@router.post("/journal-entries", status_code=status.HTTP_201_CREATED)
def create_journal_entry(payload: JournalEntryCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(FinanceService.create_journal_entry(db, payload.model_dump()))


@router.put("/journal-entries/{journal_entry_id}")
def update_journal_entry(journal_entry_id: int, payload: JournalEntryUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = FinanceService.update_journal_entry(db, journal_entry_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
    return _serialize(item)


@router.delete("/journal-entries/{journal_entry_id}")
def delete_journal_entry(journal_entry_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = FinanceService.delete_journal_entry(db, journal_entry_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal entry not found")
    return {"status": "deleted", "id": str(journal_entry_id)}
