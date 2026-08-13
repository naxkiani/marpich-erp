"""FastAPI application factory — profile-aware composition root."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.presentation.api.startup_registry import configure_application
from core.presentation.middleware.platform_gateway import PlatformGatewayMiddleware
from core.presentation.middleware.tenant_rls import TenantRlsMiddleware
from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher
from shared.infrastructure.observability.telemetry import setup_observability, shutdown_observability
from shared.infrastructure.settings import settings


def _try_import(attr: str, module: str) -> Any | None:
    try:
        mod = __import__(module, fromlist=[attr])
        return getattr(mod, attr)
    except (ModuleNotFoundError, AttributeError):
        return None


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
        get_transport_registry = _try_import(
            "get_transport_registry",
            "shared.infrastructure.messaging.transport_registry",
        )
        transport = get_transport_registry() if get_transport_registry else None
        if transport is not None:
            await transport.start()
        await dispatcher.start()
        get_orchestration_worker = _try_import(
            "get_orchestration_worker",
            "contexts.enterprise_message_orchestration.infrastructure.workers.orchestration_worker",
        )
        orchestration_worker = get_orchestration_worker() if get_orchestration_worker else None
        if orchestration_worker is not None:
            await orchestration_worker.start()
        setup_observability(app)
        yield
        if orchestration_worker is not None:
            await orchestration_worker.stop()
        await dispatcher.stop()
        if transport is not None:
            await transport.stop()
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
    application.add_middleware(TenantRlsMiddleware)
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
