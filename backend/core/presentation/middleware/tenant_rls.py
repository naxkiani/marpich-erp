"""Tenant RLS middleware — bind tenant/principal context per request."""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from shared.infrastructure.database.rls_context import bind_tenant_context, reset_tenant_context
from shared.infrastructure.settings import use_rls


class TenantRlsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if not use_rls():
            return await call_next(request)

        tenant_id = request.headers.get("x-tenant-id")
        principal_id: str | None = None
        auth = request.headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            token = auth[7:].strip()
            if token:
                try:
                    from contexts.identity.container import get_identity_service

                    payload = get_identity_service().verify_access_token(token)
                    if tenant_id and payload.get("tenant_id", "").lower() != tenant_id.lower():
                        principal_id = None
                    else:
                        principal_id = payload.get("sub")
                        tenant_id = tenant_id or payload.get("tenant_id")
                except ValueError:
                    principal_id = None

        tenant_token, principal_token = bind_tenant_context(
            tenant_id=tenant_id.lower() if tenant_id else None,
            principal_id=principal_id,
        )
        try:
            return await call_next(request)
        finally:
            reset_tenant_context(tenant_token, principal_token)
