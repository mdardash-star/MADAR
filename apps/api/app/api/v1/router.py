from fastapi import APIRouter

from app.routes.assets import router as assets_router
from app.routes.crm import router as crm_router
from app.routes.business_foundation import router as business_foundation_router
from app.routes.customers import router as customers_router
from app.routes.dashboard import router as dashboard_router
from app.routes.finance import router as finance_router
from app.routes.hr import router as hr_router
from app.routes.inventory import router as inventory_router
from app.routes.master_data import router as master_data_router
from app.routes.me import router as me_router
from app.routes.procurement import router as procurement_router
from app.routes.sales import router as sales_router

router = APIRouter(prefix="/api/v1")
router.include_router(me_router)
router.include_router(dashboard_router)
# Register secure customer routes before the legacy master-data router so the
# customer paths resolve to the tenant-scoped implementation.
router.include_router(customers_router)
router.include_router(master_data_router)
router.include_router(business_foundation_router)
router.include_router(sales_router)
router.include_router(procurement_router)
router.include_router(inventory_router)
router.include_router(finance_router)
router.include_router(hr_router)
router.include_router(assets_router)
router.include_router(crm_router)


@router.get("/status")
def api_status() -> dict[str, str]:
    return {"status": "ok"}
