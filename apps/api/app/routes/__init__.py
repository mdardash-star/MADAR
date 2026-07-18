from app.routes.auth import router as auth_router
from app.routes.company import router as company_router
from app.routes.health import router as health_router

__all__ = ["auth_router", "company_router", "health_router"]
