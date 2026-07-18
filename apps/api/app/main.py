from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.company import router as company_router
from app.routes.health import router as health_router

app = FastAPI(
    title="MADAR ERP API",
    version="1.0.0",
    description="Production-ready ERP SaaS backend for multi-tenant operations.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(api_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"name": "MADAR ERP API", "status": "ok", "environment": settings.app_env}
