"""FastAPI dependencies — tenant, auth, RBAC."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from contexts.identity.container import get_identity_service

_bearer = HTTPBearer(auto_error=False)


async def get_tenant_id(x_tenant_id: Annotated[str | None, Header()] = None) -> str:
    if not x_tenant_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "X-Tenant-ID header required")
    return x_tenant_id.strip().lower()


async def get_correlation_id(
    x_correlation_id: Annotated[str | None, Header()] = None,
) -> str:
    return x_correlation_id or str(uuid.uuid4())


def get_client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> dict:
    if not credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required")
    try:
        return get_identity_service().verify_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from exc


def require_permissions(*permissions: str):
    async def checker(user: Annotated[dict, Depends(get_current_user)]) -> dict:
        svc = get_identity_service()
        user_perms = user.get("permissions", [])
        for perm in permissions:
            if not svc.check_permission(user_perms, perm):
                raise HTTPException(status.HTTP_403_FORBIDDEN, f"Missing permission: {perm}")
        return user

    return checker
