"""Permission Registry API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.permission_registry.container import get_permission_registry_service
from contexts.permission_registry.presentation.schemas import (
    AssignRoleRequest,
    CreatePermissionSetRequest,
    CreateRoleRequest,
    RegisterPermissionsRequest,
)

permission_registry_router = APIRouter(
    prefix="/permissions",
    tags=["Permission Registry"],
)


@permission_registry_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    return {"data": (await get_permission_registry_service().list_catalog()).unwrap()}


@permission_registry_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    return {"data": (await get_permission_registry_service().get_dependency_map()).unwrap()}


@permission_registry_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.write"))],
):
    return {"data": (await get_permission_registry_service().seed(tenant_id)).unwrap()}


@permission_registry_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    return {"data": (await get_permission_registry_service().get_dashboard(tenant_id)).unwrap()}


@permission_registry_router.get("")
async def list_permissions(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
    module: Annotated[str | None, Query()] = None,
):
    return {"data": (await get_permission_registry_service().list_permissions(module=module)).unwrap()}


@permission_registry_router.post("/register")
async def register_permissions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterPermissionsRequest,
    _user: Annotated[dict, Depends(require_permissions("permissions.write"))],
):
    result = await get_permission_registry_service().register_permissions(
        tenant_id,
        module=body.module,
        permissions=[p.model_dump() for p in body.permissions],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.get("/roles")
async def list_roles(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    return {"data": (await get_permission_registry_service().list_roles(tenant_id)).unwrap()}


@permission_registry_router.post("/roles")
async def create_role(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateRoleRequest,
    _user: Annotated[dict, Depends(require_permissions("permissions.roles.write"))],
):
    result = await get_permission_registry_service().create_role(
        tenant_id,
        code=body.code,
        name=body.name,
        description=body.description,
        permission_codes=body.permission_codes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.get("/roles/{role_ref}")
async def get_role(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    role_ref: str,
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    result = await get_permission_registry_service().get_role(tenant_id, role_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.post("/roles/{role_ref}/bindings")
async def assign_role(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    role_ref: str,
    body: AssignRoleRequest,
    user: Annotated[dict, Depends(require_permissions("permissions.roles.write"))],
):
    result = await get_permission_registry_service().assign_role(
        tenant_id,
        role_ref=role_ref,
        principal_id=body.principal_id,
        scope_type=body.scope_type,
        scope_id=body.scope_id,
        granted_by=str(user.get("sub")),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.delete("/role-bindings/{binding_ref}")
async def revoke_binding(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    binding_ref: str,
    _user: Annotated[dict, Depends(require_permissions("permissions.roles.write"))],
):
    result = await get_permission_registry_service().revoke_binding(tenant_id, binding_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.get("/role-bindings")
async def list_bindings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
    principal_id: Annotated[str | None, Query()] = None,
):
    return {"data": (await get_permission_registry_service().list_bindings(tenant_id, principal_id=principal_id)).unwrap()}


@permission_registry_router.get("/sets")
async def list_permission_sets(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    return {"data": (await get_permission_registry_service().list_permission_sets(tenant_id)).unwrap()}


@permission_registry_router.post("/sets")
async def create_permission_set(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreatePermissionSetRequest,
    _user: Annotated[dict, Depends(require_permissions("permissions.write"))],
):
    result = await get_permission_registry_service().create_permission_set(
        tenant_id,
        module=body.module,
        name=body.name,
        description=body.description,
        permission_codes=body.permission_codes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@permission_registry_router.get("/principals/{principal_id}/permissions")
async def resolve_principal_permissions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    principal_id: str,
    _user: Annotated[dict, Depends(require_permissions("permissions.read"))],
):
    result = await get_permission_registry_service().resolve_principal_permissions(tenant_id, principal_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
