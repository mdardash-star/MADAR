from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    tenant_id: int | None = None
