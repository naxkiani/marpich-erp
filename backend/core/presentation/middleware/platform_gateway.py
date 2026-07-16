"""Platform gateway middleware — request ID, timing, structured access log."""
from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from shared.infrastructure.observability.telemetry import annotate_active_span, record_http_request

logger = logging.getLogger("marpich.gateway")

# Tenant-scoped business APIs require X-Tenant-ID at the edge (fail-fast).
# Platform meta, health, and OpenAPI remain exempt (cross-tenant / public).
_TENANT_EXEMPT_PREFIXES = (
    "/health",
    "/api/v1/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/docs",
    "/api/redoc",
    "/api/openapi.json",
    "/api/v1/platform/",
    "/api/v1/documents/verify/",
)


def _requires_tenant_header(path: str, method: str) -> bool:
    if method.upper() == "OPTIONS":
        return False
    if not path.startswith("/api/v1/"):
        return False
    return not any(path == p or path.startswith(p) for p in _TENANT_EXEMPT_PREFIXES)


class PlatformGatewayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        correlation_id = request.headers.get("x-correlation-id") or request_id
        tenant_id = request.headers.get("x-tenant-id", "").strip()
        started = time.perf_counter()
        annotate_active_span(
            **{
                "marpich.request_id": request_id,
                "marpich.correlation_id": correlation_id,
            }
        )
        if tenant_id:
            annotate_active_span(**{"marpich.tenant_id": tenant_id.lower()})
        elif _requires_tenant_header(request.url.path, request.method):
            return JSONResponse(
                status_code=400,
                content={"detail": "X-Tenant-ID header required"},
                headers={
                    "X-Request-ID": request_id,
                    "X-Correlation-ID": correlation_id,
                },
            )

        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        response.headers["X-Request-ID"] = request_id
        if not response.headers.get("X-Correlation-ID"):
            response.headers["X-Correlation-ID"] = correlation_id

        record_http_request(
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(elapsed_ms, 2),
        )
        logger.info(
            "gateway request",
            extra={
                "request_id": request_id,
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round(elapsed_ms, 2),
            },
        )
        return response
