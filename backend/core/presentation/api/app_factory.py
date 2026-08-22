"""FastAPI application factory — profile-aware composition root."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Protocol

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.presentation.api.startup_registry import configure_application
from core.presentation.middleware.platform_gateway import PlatformGatewayMiddleware
from core.presentation.middleware.tenant_rls import TenantRlsMiddleware
from shared.infrastructure.messaging.dispatcher import get_outbox_dispatcher
from shared.infrastructure.observability.telemetry import setup_observability, shutdown_observability
from shared.infrastructure.settings import settings


class _LifecycleWorker(Protocol):
    async def start(self) -> None: ...
    async def stop(self) -> None: ...


class _NoopLifecycle:
    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None


def _optional_orchestration_worker() -> _LifecycleWorker | None:
    """Message orchestration context may be absent when sources are not restored."""
    try:
        from contexts.enterprise_message_orchestration.infrastructure.workers.orchestration_worker import (
            get_orchestration_worker,
        )
    except ModuleNotFoundError:
        return None
    return get_orchestration_worker()


def _transport_registry() -> _LifecycleWorker:
    """Prefer shared transport registry; fall back to no-op when module is missing."""
    try:
        from shared.infrastructure.messaging.transport_registry import get_transport_registry
    except ModuleNotFoundError:
        return _NoopLifecycle()
    return get_transport_registry()


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
        transport = _transport_registry()
        await transport.start()
        await dispatcher.start()
        orchestration_worker = _optional_orchestration_worker()
        if orchestration_worker is not None:
            await orchestration_worker.start()
        setup_observability(app)
        yield
        if orchestration_worker is not None:
            await orchestration_worker.stop()
        await dispatcher.stop()
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

    # Register routers at build time so ASGI tests without lifespan still resolve
    # /api/v1/* routes. Lifespan configure_application remains idempotent.
    configure_application(
        application,
        profile=app_profile,
        startup_mode=app_startup_mode,
    )

    @application.get("/api/v1/health", tags=["Monitoring"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "marpich-backend",
            "profile": app_profile,
        }

    @application.get("/live", tags=["Monitoring"])
    @application.get("/api/v1/live", tags=["Monitoring"])
    async def live() -> dict[str, str]:
        return {"status": "live", "service": "marpich-backend"}

    @application.get("/ready", tags=["Monitoring"])
    @application.get("/api/v1/ready", tags=["Monitoring"])
    async def ready() -> dict[str, Any]:
        from shared.infrastructure.settings import use_postgres

        if not use_postgres():
            return {"status": "ready", "service": "marpich-backend", "database": "not_required"}
        try:
            from sqlalchemy import text

            from shared.infrastructure.database.engine import get_engine

            async with get_engine().connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as exc:  # noqa: BLE001 — readiness must fail closed
            return JSONResponse(
                status_code=503,
                content={
                    "status": "not_ready",
                    "service": "marpich-backend",
                    "database": "unreachable",
                    "detail": type(exc).__name__,
                },
            )
        return {"status": "ready", "service": "marpich-backend", "database": "ok"}

    return application
