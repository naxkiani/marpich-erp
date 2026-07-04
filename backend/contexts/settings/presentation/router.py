"""Settings FastAPI router."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.settings.container import get_settings_service
from contexts.settings.presentation.schemas import ToggleFeatureRequest, UpdateBrandingRequest, UpdateConfigRequest

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/config")
async def get_all_config(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.config.read"))],
):
    result = await get_settings_service().get_settings(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()["config"]}


@router.get("/config/{key}")
async def get_config_key(
    key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.config.read"))],
):
    result = await get_settings_service().get_config_key(tenant_id, key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.put("/config/{key}")
async def update_config(
    key: str,
    body: UpdateConfigRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.config.write"))],
):
    result = await get_settings_service().update_config(tenant_id, key, body.value, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()["config"], "meta": {"correlation_id": correlation_id}}


@router.get("/features")
async def list_features(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.features.read"))],
):
    result = await get_settings_service().list_features(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.put("/features/{key}")
async def toggle_feature(
    key: str,
    body: ToggleFeatureRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.features.write"))],
):
    result = await get_settings_service().toggle_feature(tenant_id, key, body.enabled, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/branding")
async def get_branding(tenant_id: Annotated[str, Depends(get_tenant_id)]):
    result = await get_settings_service().get_settings(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()["branding"]}


@router.put("/branding")
async def update_branding(
    body: UpdateBrandingRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("settings.branding.write"))],
):
    branding: dict[str, Any] = body.model_dump(exclude_none=True)
    result = await get_settings_service().update_branding(tenant_id, branding, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
