from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class CompanyRegistrationRequest(BaseModel):
    company_name: str
    company_slug: str
    legal_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    admin_full_name: str
    admin_email: EmailStr
    admin_password: str
