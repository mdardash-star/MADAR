import uuid
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.logging import configure_logging, request_logger, request_id_var, company_id_var
from app.routes.auth import router as auth_router
from app.routes.company import router as company_router
from app.routes.health import router as health_router

# Initialize structured logging
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    request_logger.info(
        "MADAR API starting",
        version=settings.api_version,
        environment=settings.app_env,
    )
    yield
    request_logger.info("MADAR API shutting down")


# Initialize Sentry error tracking (only if DSN configured)
if settings.sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        release=f"madar@{settings.api_version}",
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1 if settings.is_production else 0.0,
        send_default_pii=False,
    )

app = FastAPI(
    title="MADAR ERP API",
    version=settings.api_version,
    description="Production-ready ERP SaaS backend for multi-tenant operations.",
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    """
    Per-request middleware:
    - Assigns a unique request ID
    - Logs request start and completion
    - Records response time
    """
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request_id_var.set(req_id)

    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        request_logger.error(
            "Unhandled exception",
            method=request.method,
            path=request.url.path,
            exc_info=exc,
        )
        raise

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = req_id

    # Log every request (skip health checks to reduce noise)
    if request.url.path not in ("/health", "/health/live"):
        request_logger.info(
            "Request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=request.client.host if request.client else "unknown",
        )

    return response


# Prometheus metrics endpoint
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=False,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/health", "/health/live", "/metrics"],
        inprogress_name="http_requests_in_flight",
        inprogress_labels=True,
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
except ImportError:
    # prometheus_fastapi_instrumentator not installed — skip metrics
    pass

# Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(api_router)


@app.get("/", include_in_schema=False)
def read_root() -> dict[str, str]:
    return {
        "name": "MADAR ERP API",
        "status": "ok",
        "version": settings.api_version,
        "environment": settings.app_env,
    }

