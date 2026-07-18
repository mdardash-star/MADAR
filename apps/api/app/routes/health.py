"""
Comprehensive health check endpoints for MADAR API.
Provides /health, /health/ready, and /health/live endpoints.
"""
import time
from datetime import datetime, UTC

import redis as redis_client
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])

# Track startup time for uptime calculation
_startup_time = time.time()


@router.get("", summary="Basic health check")
def health_check() -> dict[str, str]:
    """Quick liveness probe — no DB checks."""
    return {"status": "healthy"}


@router.get("/live", summary="Liveness probe")
def liveness() -> dict:
    """Container liveness probe — confirms process is alive."""
    return {
        "status": "alive",
        "version": settings.api_version,
        "environment": settings.app_env,
        "uptime_seconds": round(time.time() - _startup_time),
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/ready", summary="Readiness probe")
def readiness(db: Session = Depends(get_db)) -> dict:
    """
    Readiness probe — confirms all dependencies are reachable.
    Used by load balancers to decide whether to send traffic.
    """
    checks: dict[str, str] = {}
    healthy = True

    # Database check
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {type(e).__name__}"
        healthy = False

    # Redis check
    try:
        r = redis_client.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            socket_connect_timeout=2,
        )
        r.ping()
        checks["redis"] = "connected"
    except Exception as e:
        checks["redis"] = f"error: {type(e).__name__}"
        # Redis degraded but not fatal

    status = "ready" if healthy else "degraded"
    return {
        "status": status,
        "checks": checks,
        "version": settings.api_version,
        "timestamp": datetime.now(UTC).isoformat(),
    }

