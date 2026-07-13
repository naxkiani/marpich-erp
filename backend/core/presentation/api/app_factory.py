"""FastAPI application factory — profile-aware composition root."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.presentation.api.startup_registry import configure_application
from core.presentation.middleware.platform_gateway import PlatformGatewayMiddleware
from contexts.enterprise_message_orchestration.infrastructure.workers.orchestration_worker import (
    get_orchestration_worker,
)
from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher
from shared.infrastructure.messaging.transport_registry import get_transport_registry
from shared.infrastructure.observability.telemetry import setup_observability, shutdown_observability
from shared.infrastructure.settings import settings


def create_app(
    *,
    profile: str | None = None,
    startup_mode: str | None = None,
) -> FastAPI:
    """Build a FastAPI app with a router/service profile."""
    app_profile = profile or settings.marpich_app_profile
    app_startup_mode = startup_mode or settings.marpich_startup_mode

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_application(
            app,
            profile=app_profile,
            startup_mode=app_startup_mode,
        )
        dispatcher = get_outbox_dispatcher()
        await get_transport_registry().start()
        await dispatcher.start()
        orchestration_worker = get_orchestration_worker()
        await orchestration_worker.start()
        setup_observability(app)
        yield
        await orchestration_worker.stop()
        await dispatcher.stop()
        await get_transport_registry().stop()
        shutdown_observability()

    application = FastAPI(
        title="Marpich ERP",
        description="Enterprise Operating System — DDD + Clean Architecture",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    application.add_middleware(PlatformGatewayMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/api/v1/health", tags=["Monitoring"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "marpich-backend",
            "profile": app_profile,
        }

    return application
