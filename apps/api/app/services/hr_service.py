from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.payroll import Payroll


class HRService:
    @staticmethod
    def list_employees(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Employee).filter(Employee.company_id == company_id, Employee.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Employee.employee_code.ilike(f"%{search}%"), Employee.first_name.ilike(f"%{search}%"), Employee.last_name.ilike(f"%{search}%")))
        return query.order_by(Employee.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_employee(db: Session, payload: dict) -> Employee:
        item = Employee(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_employee(db: Session, employee_id: int, payload: dict) -> Employee | None:
        item = db.query(Employee).filter(Employee.id == employee_id, Employee.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        item = db.query(Employee).filter(Employee.id == employee_id, Employee.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_attendances(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Attendance).filter(Attendance.company_id == company_id, Attendance.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Attendance.status.ilike(f"%{search}%"), Attendance.note.ilike(f"%{search}%")))
        return query.order_by(Attendance.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_attendance(db: Session, payload: dict) -> Attendance:
        item = Attendance(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_attendance(db: Session, attendance_id: int, payload: dict) -> Attendance | None:
        item = db.query(Attendance).filter(Attendance.id == attendance_id, Attendance.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_attendance(db: Session, attendance_id: int) -> bool:
        item = db.query(Attendance).filter(Attendance.id == attendance_id, Attendance.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True

    @staticmethod
    def list_payrolls(db: Session, company_id: int, skip: int = 0, limit: int = 50, search: str | None = None):
        query = db.query(Payroll).filter(Payroll.company_id == company_id, Payroll.is_deleted.is_(False))
        if search:
            query = query.filter(or_(Payroll.payroll_month.ilike(f"%{search}%"), Payroll.status.ilike(f"%{search}%")))
        return query.order_by(Payroll.id).offset(skip).limit(limit).all()

    @staticmethod
    def create_payroll(db: Session, payload: dict) -> Payroll:
        item = Payroll(**payload)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_payroll(db: Session, payroll_id: int, payload: dict) -> Payroll | None:
        item = db.query(Payroll).filter(Payroll.id == payroll_id, Payroll.is_deleted.is_(False)).first()
        if not item:
            return None
        for field, value in payload.items():
            if value is not None:
                setattr(item, field, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_payroll(db: Session, payroll_id: int) -> bool:
        item = db.query(Payroll).filter(Payroll.id == payroll_id, Payroll.is_deleted.is_(False)).first()
        if not item:
            return False
        item.is_deleted = True
        item.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return True
