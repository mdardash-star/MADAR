from pydantic import BaseModel, Field


class EmployeeCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    role_id: int | None = None
    employee_code: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    status: str = "active"


class EmployeeUpdateRequest(BaseModel):
    branch_id: int | None = None
    role_id: int | None = None
    employee_code: str | None = Field(default=None, min_length=1, max_length=50)
    first_name: str | None = Field(default=None, min_length=1, max_length=255)
    last_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    status: str | None = None


class AttendanceCreateRequest(BaseModel):
    company_id: int
    employee_id: int
    branch_id: int | None = None
    attendance_date: str | None = None
    check_in: str | None = None
    check_out: str | None = None
    status: str = "present"
    note: str | None = None


class AttendanceUpdateRequest(BaseModel):
    employee_id: int | None = None
    branch_id: int | None = None
    attendance_date: str | None = None
    check_in: str | None = None
    check_out: str | None = None
    status: str | None = None
    note: str | None = None


class PayrollCreateRequest(BaseModel):
    company_id: int
    employee_id: int
    branch_id: int | None = None
    payroll_month: str = Field(min_length=1, max_length=20)
    basic_salary: float = Field(ge=0)
    allowances: float = Field(ge=0)
    deductions: float = Field(ge=0)
    net_salary: float = Field(ge=0)
    status: str = "draft"
    note: str | None = None


class PayrollUpdateRequest(BaseModel):
    employee_id: int | None = None
    branch_id: int | None = None
    payroll_month: str | None = Field(default=None, min_length=1, max_length=20)
    basic_salary: float | None = Field(default=None, ge=0)
    allowances: float | None = Field(default=None, ge=0)
    deductions: float | None = Field(default=None, ge=0)
    net_salary: float | None = Field(default=None, ge=0)
    status: str | None = None
    note: str | None = None
