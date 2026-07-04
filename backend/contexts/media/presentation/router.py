"""Media FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.media.container import get_media_service
from contexts.media.presentation.schemas import (
    CompleteUploadRequest,
    RegisterAssetRequest,
    TranscodeRequest,
)

router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/assets", status_code=status.HTTP_201_CREATED)
async def register_asset(
    body: RegisterAssetRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("media.assets.write"))],
):
    result = await get_media_service().register_upload(
        tenant_id=tenant_id,
        file_name=body.file_name,
        content_type=body.content_type,
        metadata=body.metadata,
        created_by=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/assets/{asset_id}/complete")
async def complete_upload(
    asset_id: str,
    body: CompleteUploadRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("media.assets.write"))],
):
    result = await get_media_service().complete_upload(
        tenant_id, correlation_id, asset_id, body.checksum
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/assets/{asset_id}")
async def get_asset(
    asset_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("media.assets.read"))],
):
    result = await get_media_service().get_asset(tenant_id, asset_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/assets/{asset_id}/transcode", status_code=status.HTTP_202_ACCEPTED)
async def request_transcode(
    asset_id: str,
    body: TranscodeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("media.assets.write"))],
):
    result = await get_media_service().request_transcode(
        tenant_id, correlation_id, asset_id, body.profile
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/assets/{asset_id}/variants/{profile}")
async def get_variant(
    asset_id: str,
    profile: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_media_service().get_variant(tenant_id, asset_id, profile)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.delete("/assets/{asset_id}", status_code=status.HTTP_200_OK)
async def delete_asset(
    asset_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("media.assets.delete"))],
):
    result = await get_media_service().delete_asset(tenant_id, correlation_id, asset_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
