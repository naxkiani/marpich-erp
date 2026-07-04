"""Core Platform FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.core_platform.container import get_platform_service
from contexts.core_platform.presentation.schemas import ActivateModuleRequest, ProvisionTenantRequest
from contexts.identity.presentation.dependencies import get_correlation_id, require_permissions

router = APIRouter(prefix="/platform", tags=["Core Platform"])


@router.get("/industry-packs")
async def list_industry_packs():
    result = await get_platform_service().list_industry_packs()
    return {"data": result.unwrap()}


@router.get("/industry-packs/{pack_id}")
async def get_industry_pack(pack_id: str):
    result = await get_platform_service().get_industry_pack(pack_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/tenants", status_code=status.HTTP_201_CREATED)
async def provision_tenant(
    body: ProvisionTenantRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_platform_service().provision_tenant(
        name=body.name,
        slug=body.slug,
        industry_pack=body.industry_pack,
        correlation_id=correlation_id,
        tier=body.tier,
        optional_modules=body.optional_modules,
        locale=body.locale,
        timezone=body.timezone,
        data_region=body.data_region,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/tenants")
async def list_tenants(
    _user: Annotated[dict, Depends(require_permissions("platform.tenants.read"))],
):
    result = await get_platform_service().list_tenants()
    return {"data": result.unwrap()}


@router.get("/tenants/{slug}")
async def get_tenant(slug: str):
    result = await get_platform_service().get_tenant(slug)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/tenants/{slug}/suspend")
async def suspend_tenant(
    slug: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("platform.tenants.write"))],
):
    result = await get_platform_service().suspend_tenant(slug, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/tenants/{slug}/modules")
async def activate_module(
    slug: str,
    body: ActivateModuleRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("platform.modules.write"))],
):
    result = await get_platform_service().activate_module(slug, body.module_id, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
