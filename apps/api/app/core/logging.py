"""
Structured JSON logging for MADAR API.
Outputs JSON in production, colored console in development.
"""
import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

import structlog

from app.core.config import settings

# Context variable for request correlation
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
company_id_var: ContextVar[int | None] = ContextVar("company_id", default=None)
user_id_var: ContextVar[int | None] = ContextVar("user_id", default=None)


def add_request_context(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Inject request context into every log record."""
    req_id = request_id_var.get("")
    if req_id:
        event_dict["request_id"] = req_id
    company_id = company_id_var.get(None)
    if company_id:
        event_dict["company_id"] = company_id
    user_id = user_id_var.get(None)
    if user_id:
        event_dict["user_id"] = user_id
    return event_dict


def configure_logging() -> None:
    """Configure structlog and stdlib logging."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        add_request_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.log_format == "json" or settings.is_production:
        # JSON for production / log aggregation
        renderer = structlog.processors.JSONRenderer()
    else:
        # Human-readable for local development
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a named structured logger."""
    return structlog.get_logger(name)


# Module-level loggers
request_logger = get_logger("madar.request")
auth_logger = get_logger("madar.auth")
business_logger = get_logger("madar.business")
db_logger = get_logger("madar.db")
