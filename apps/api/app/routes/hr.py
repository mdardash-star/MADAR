from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hr import (
    AttendanceCreateRequest,
    AttendanceUpdateRequest,
    EmployeeCreateRequest,
    EmployeeUpdateRequest,
    PayrollCreateRequest,
    PayrollUpdateRequest,
)
from app.services.hr_service import HRService

router = APIRouter(prefix="/hr", tags=["hr"])


def _serialize(instance: Any) -> dict[str, Any]:
    return {key: value for key, value in instance.__dict__.items() if key != "_sa_instance_state"}


@router.get("/employees")
def list_employees(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in HRService.list_employees(db, company_id, skip, limit, search)]


@router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(HRService.create_employee(db, payload.model_dump()))


@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, payload: EmployeeUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = HRService.update_employee(db, employee_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return _serialize(item)


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = HRService.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return {"status": "deleted", "id": str(employee_id)}


@router.get("/attendances")
def list_attendances(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in HRService.list_attendances(db, company_id, skip, limit, search)]


@router.post("/attendances", status_code=status.HTTP_201_CREATED)
def create_attendance(payload: AttendanceCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(HRService.create_attendance(db, payload.model_dump()))


@router.put("/attendances/{attendance_id}")
def update_attendance(attendance_id: int, payload: AttendanceUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = HRService.update_attendance(db, attendance_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    return _serialize(item)


@router.delete("/attendances/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = HRService.delete_attendance(db, attendance_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    return {"status": "deleted", "id": str(attendance_id)}


@router.get("/payrolls")
def list_payrolls(
    company_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    return [_serialize(item) for item in HRService.list_payrolls(db, company_id, skip, limit, search)]


@router.post("/payrolls", status_code=status.HTTP_201_CREATED)
def create_payroll(payload: PayrollCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    return _serialize(HRService.create_payroll(db, payload.model_dump()))


@router.put("/payrolls/{payroll_id}")
def update_payroll(payroll_id: int, payload: PayrollUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    item = HRService.update_payroll(db, payroll_id, payload.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")
    return _serialize(item)


@router.delete("/payrolls/{payroll_id}")
def delete_payroll(payroll_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = HRService.delete_payroll(db, payroll_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found")
    return {"status": "deleted", "id": str(payroll_id)}
