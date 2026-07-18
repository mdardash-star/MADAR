from fastapi import APIRouter

from app.routes.me import router as me_router

router = APIRouter(prefix="/api/v1")
router.include_router(me_router)


@router.get("/status")
def api_status() -> dict[str, str]:
    return {"status": "ok"}
