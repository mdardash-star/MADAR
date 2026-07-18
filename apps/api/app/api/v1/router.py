from fastapi import APIRouter

from app.routes.business_foundation import router as business_foundation_router
from app.routes.master_data import router as master_data_router
from app.routes.me import router as me_router
from app.routes.sales import router as sales_router

router = APIRouter(prefix="/api/v1")
router.include_router(me_router)
router.include_router(master_data_router)
router.include_router(business_foundation_router)
router.include_router(sales_router)


@router.get("/status")
def api_status() -> dict[str, str]:
    return {"status": "ok"}
