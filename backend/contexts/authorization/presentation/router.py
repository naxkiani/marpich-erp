"""Authorization PDP API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.authorization.container import get_authorization_service
from contexts.authorization.presentation.schemas import (
    AuthorizationBatchCheckRequest,
    AuthorizationCheckRequest,
    AuthorizationSimulateRequest,
)
from contexts.identity.presentation.dependencies import get_current_user, get_tenant_id, require_permissions

authorization_router = APIRouter(
    prefix="/authorization",
    tags=["Authorization"],
)


def _resolve_principal_id(body_principal_id: str | None, user: dict) -> str:
    if body_principal_id and body_principal_id != user.get("sub"):
        if "*" not in user.get("permissions", []):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot evaluate other principals")
        return body_principal_id
    return str(user.get("sub"))


@authorization_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.read"))],
):
    return {"data": (await get_authorization_service().list_catalog()).unwrap()}


@authorization_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.read"))],
):
    return {"data": (await get_authorization_service().get_dependency_map()).unwrap()}


@authorization_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.write"))],
):
    return {"data": (await get_authorization_service().seed(tenant_id)).unwrap()}


@authorization_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.read"))],
):
    return {"data": (await get_authorization_service().get_dashboard(tenant_id)).unwrap()}


@authorization_router.post("/check")
async def check_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AuthorizationCheckRequest,
    user: Annotated[dict, Depends(get_current_user)],
):
    principal_id = _resolve_principal_id(body.principal_id, user)
    result = await get_authorization_service().check_access(
        tenant_id,
        principal_id=principal_id,
        resource=body.resource,
        action=body.action,
        permission_code=body.permission_code,
        context=body.context,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@authorization_router.post("/check/batch")
async def check_access_batch(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AuthorizationBatchCheckRequest,
    user: Annotated[dict, Depends(get_current_user)],
):
    principal_id = _resolve_principal_id(body.principal_id, user)
    return {
        "data": (
            await get_authorization_service().check_access_batch(
                tenant_id,
                principal_id=principal_id,
                checks=body.checks,
                simulate=body.simulate,
            )
        ).unwrap()
    }


@authorization_router.post("/simulate")
async def simulate_access(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: AuthorizationSimulateRequest,
    user: Annotated[dict, Depends(require_permissions("authorization.simulate"))],
):
    principal_id = body.principal_id or str(user.get("sub"))
    result = await get_authorization_service().check_access(
        tenant_id,
        principal_id=principal_id,
        resource=body.resource,
        action=body.action,
        permission_code=body.permission_code,
        context=body.context,
        simulate=True,
        record=False,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@authorization_router.get("/policies/abac")
async def list_abac_policies(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.read"))],
):
    return {"data": (await get_authorization_service().list_abac_policies(tenant_id)).unwrap()}


@authorization_router.get("/decisions")
async def list_decisions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("authorization.read"))],
):
    return {"data": (await get_authorization_service().list_decisions(tenant_id)).unwrap()}
