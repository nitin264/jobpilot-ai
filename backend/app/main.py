from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.health import router as health_router
from app.api.request_logging import RequestLoggingMiddleware
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    logger = get_logger(__name__)
    logger.info(
        "application_startup",
        extra={
            "environment": settings.environment,
            "app_name": settings.app_name,
        },
    )
    app.state.settings = settings
    yield
    logger.info(
        "application_shutdown",
        extra={
            "environment": settings.environment,
            "app_name": settings.app_name,
        },
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.app_version,
        debug=resolved_settings.debug,
        lifespan=lifespan,
    )

    app.state.settings = resolved_settings
    app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(app)
    app.include_router(health_router)
    return app


app = create_app()
