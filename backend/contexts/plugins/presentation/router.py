"""Plugin platform FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.plugins.container import get_plugin_service
from contexts.plugins.presentation.schemas import (
    InstallPluginRequest,
    InvokePluginRequest,
    RegisterPluginRequest,
    SubmitListingRequest,
    UpgradePluginRequest,
)

router = APIRouter(prefix="/plugins", tags=["Plugins"])


@router.get("")
async def list_plugins(
    _user: Annotated[dict, Depends(require_permissions("plugins.read"))],
):
    return {"data": (await get_plugin_service().list_plugins()).unwrap()}


@router.get("/installed")
async def list_installed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.read"))],
):
    return {"data": (await get_plugin_service().list_installed(tenant_id)).unwrap()}


@router.get("/marketplace/listings")
async def marketplace_listings(
    _user: Annotated[dict, Depends(require_permissions("plugins.marketplace.read"))],
    plugin_type: str | None = Query(None, alias="type"),
    trust: str | None = Query(None),
    q: str | None = Query(None),
):
    return {
        "data": (
            await get_plugin_service().list_marketplace(
                plugin_type=plugin_type, trust_level=trust, query=q
            )
        ).unwrap()
    }


@router.get("/marketplace/dashboard")
async def marketplace_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.marketplace.read"))],
):
    return {"data": (await get_plugin_service().get_marketplace_dashboard(tenant_id)).unwrap()}


@router.get("/marketplace/listings/{plugin_id}")
async def marketplace_listing_detail(
    plugin_id: str,
    _user: Annotated[dict, Depends(require_permissions("plugins.marketplace.read"))],
):
    result = await get_plugin_service().get_plugin(plugin_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/marketplace/submissions", status_code=status.HTTP_201_CREATED)
async def submit_listing(
    body: SubmitListingRequest,
    _user: Annotated[dict, Depends(require_permissions("plugins.publish"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    plugin_id: str = Query(...),
):
    result = await get_plugin_service().submit_listing(
        plugin_id=plugin_id,
        version=body.version,
        package_checksum=body.package_checksum,
        public_key_fingerprint=body.public_key_fingerprint,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/{plugin_id}")
async def get_plugin(
    plugin_id: str,
    _user: Annotated[dict, Depends(require_permissions("plugins.read"))],
):
    result = await get_plugin_service().get_plugin(plugin_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/{plugin_id}/upgrade-path")
async def upgrade_path(
    plugin_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.read"))],
):
    result = await get_plugin_service().get_upgrade_path(tenant_id, plugin_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_plugin(
    body: RegisterPluginRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.publish"))],
):
    result = await get_plugin_service().register_plugin(
        plugin_id=body.plugin_id,
        plugin_type=body.plugin_type,
        display_name=body.display_name,
        description=body.description,
        publisher_id=body.publisher_id,
        publisher_name=body.publisher_name,
        version=body.version,
        permissions=body.permissions,
        extension_points=body.extension_points,
        sandbox_profile=body.sandbox_profile,
        trust_level=body.trust_level,
        signature_algorithm=body.signature_algorithm,
        public_key_fingerprint=body.public_key_fingerprint,
        package_checksum=body.package_checksum,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{plugin_id}/install", status_code=status.HTTP_201_CREATED)
async def install_plugin(
    plugin_id: str,
    body: InstallPluginRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.install"))],
):
    result = await get_plugin_service().install_plugin(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        granted_permissions=body.granted_permissions,
        config=body.config,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{plugin_id}/upgrade")
async def upgrade_plugin(
    plugin_id: str,
    body: UpgradePluginRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.install"))],
):
    result = await get_plugin_service().upgrade_plugin(
        tenant_id=tenant_id,
        plugin_id=plugin_id,
        target_version=body.target_version,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.delete("/{plugin_id}/install")
async def uninstall_plugin(
    plugin_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.install"))],
):
    result = await get_plugin_service().uninstall_plugin(
        tenant_id=tenant_id, plugin_id=plugin_id, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{plugin_id}/verify")
async def verify_plugin(
    plugin_id: str,
    _user: Annotated[dict, Depends(require_permissions("plugins.admin"))],
):
    result = await get_plugin_service().verify_plugin(plugin_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/invoke")
async def invoke_plugin(
    body: InvokePluginRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("plugins.invoke"))],
):
    result = await get_plugin_service().invoke_plugin(
        tenant_id=tenant_id,
        plugin_id=body.plugin_id,
        extension_point=body.extension_point,
        payload=body.payload,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
