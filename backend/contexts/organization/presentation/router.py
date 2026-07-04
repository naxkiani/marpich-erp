"""Organization FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.organization.container import get_organization_service
from contexts.organization.presentation.schemas import AddMemberRequest, CreateUnitRequest

router = APIRouter(prefix="/organizations", tags=["Organization"])


@router.get("")
async def get_organization(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.orgs.read"))],
):
    result = await get_organization_service().get_organization(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/tree")
async def get_org_tree(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.orgs.read"))],
):
    result = await get_organization_service().get_tree(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/units", status_code=status.HTTP_201_CREATED)
async def create_unit(
    body: CreateUnitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.units.write"))],
):
    result = await get_organization_service().create_unit(
        tenant_id=tenant_id,
        parent_id=body.parent_id,
        unit_type=body.unit_type,
        code=body.code,
        name=body.name,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/units/{unit_id}/members", status_code=status.HTTP_201_CREATED)
async def add_member(
    unit_id: str,
    body: AddMemberRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.members.write"))],
):
    result = await get_organization_service().add_member(
        tenant_id=tenant_id,
        org_unit_id=unit_id,
        user_id=body.user_id,
        title=body.title,
        is_primary=body.is_primary,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.delete("/units/{unit_id}/members/{user_id}", status_code=status.HTTP_200_OK)
async def remove_member(
    unit_id: str,
    user_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.members.write"))],
):
    result = await get_organization_service().remove_member(
        tenant_id, unit_id, user_id, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/users/me/units")
async def list_my_units(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_organization_service().list_user_units(tenant_id, user["sub"])
    return {"data": result.unwrap()}


@router.get("/users/{user_id}/units")
async def list_user_units(
    user_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("organization.orgs.read"))],
):
    result = await get_organization_service().list_user_units(tenant_id, user_id)
    return {"data": result.unwrap()}
