"""Platform gateway middleware — request ID, timing, structured access log."""
from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from shared.infrastructure.observability.telemetry import annotate_active_span, record_http_request

logger = logging.getLogger("marpich.gateway")


class PlatformGatewayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        correlation_id = request.headers.get("x-correlation-id") or request_id
        tenant_id = request.headers.get("x-tenant-id", "")
        started = time.perf_counter()
        annotate_active_span(
            **{
                "marpich.request_id": request_id,
                "marpich.correlation_id": correlation_id,
            }
        )
        if tenant_id:
            annotate_active_span(**{"marpich.tenant_id": tenant_id.lower()})

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
