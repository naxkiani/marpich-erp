"""Identity FastAPI router — Auth, Users, MFA."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status

from contexts.identity.application.service import AuthTokens
from contexts.identity.container import get_identity_service
from contexts.identity.presentation.dependencies import (
    get_client_ip,
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.identity.presentation.schemas import (
    AssignRolesRequest,
    LoginRequest,
    LogoutRequest,
    MfaVerifyRequest,
    RefreshRequest,
    RegisterRequest,
)

router = APIRouter()


def _tokens_dict(tokens: AuthTokens) -> dict:
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
        "mfa_required": tokens.mfa_required,
        "mfa_token": tokens.mfa_token,
    }


@router.post("/auth/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(
    body: RegisterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.register(
        tenant_id=tenant_id,
        email=body.email,
        password=body.password,
        display_name=body.display_name,
        locale=body.locale,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"tenant_id": tenant_id, "correlation_id": correlation_id}}


@router.post("/auth/login", tags=["Auth"])
async def login(
    body: LoginRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.login(
        tenant_id=tenant_id,
        email=body.email,
        password=body.password,
        mfa_code=body.mfa_code,
        mfa_token=body.mfa_token,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": _tokens_dict(result.unwrap()), "meta": {"tenant_id": tenant_id}}


@router.post("/auth/refresh", tags=["Auth"])
async def refresh(
    body: RefreshRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.refresh(
        tenant_id=tenant_id,
        refresh_token=body.refresh_token,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": _tokens_dict(result.unwrap()), "meta": {"tenant_id": tenant_id}}


@router.post("/auth/logout", tags=["Auth"])
async def logout(
    body: LogoutRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity.sessions.revoke"))],
    request: Request,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.logout(
        tenant_id=tenant_id,
        user_id=user["sub"],
        refresh_token=body.refresh_token,
        revoke_all=body.revoke_all,
        correlation_id=correlation_id,
        ip_address=get_client_ip(request),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"tenant_id": tenant_id}}


@router.get("/users/me", tags=["Users"])
async def get_me(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity.users.read"))],
):
    svc = get_identity_service()
    result = await svc.get_me(tenant_id, user["sub"])
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/users/me/mfa/setup", tags=["Users", "MFA"])
async def mfa_setup(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity.mfa.manage"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.setup_mfa(
        tenant_id=tenant_id,
        user_id=user["sub"],
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/users/me/mfa/verify", tags=["Users", "MFA"])
async def mfa_verify(
    body: MfaVerifyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity.mfa.manage"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    svc = get_identity_service()
    result = await svc.verify_mfa_setup(
        tenant_id=tenant_id,
        user_id=user["sub"],
        code=body.code,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/identity/health", tags=["Monitoring"])
async def identity_health():
    return {"status": "ok", "context": "identity", "version": "0.1.0"}


@router.post("/identity/personas/education/seed", tags=["Identity", "RBAC"])
async def seed_education_personas(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity.roles.write"))],
):
    result = await get_identity_service().seed_education_personas(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/identity/personas/clinic/seed", tags=["Identity", "RBAC"])
async def seed_clinic_personas(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity.roles.write"))],
):
    result = await get_identity_service().seed_clinic_personas(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/identity/personas/hospital/seed", tags=["Identity", "RBAC"])
async def seed_hospital_personas(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity.roles.write"))],
):
    result = await get_identity_service().seed_hospital_personas(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/identity/roles", tags=["Identity", "RBAC"])
async def list_roles(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity.roles.read"))],
):
    result = await get_identity_service().list_roles(tenant_id)
    return {"data": result.unwrap()}


@router.post("/identity/users/{user_id}/roles", tags=["Identity", "RBAC"])
async def assign_user_roles(
    user_id: str,
    body: AssignRolesRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("identity.roles.write"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_identity_service().assign_user_roles(
        tenant_id=tenant_id,
        user_id=user_id,
        role_codes=body.role_codes,
        correlation_id=correlation_id,
        actor_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
