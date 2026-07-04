"""Integration FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.integration.container import get_integration_service
from contexts.integration.presentation.schemas import (
    CreateWebhookRequest,
    RegisterConnectorRequest,
    TriggerSyncJobRequest,
)

router = APIRouter(prefix="/integrations", tags=["Integration"])


@router.post("/connectors", status_code=status.HTTP_201_CREATED)
async def register_connector(
    body: RegisterConnectorRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.connectors.write"))],
):
    result = await get_integration_service().register_connector(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        connector_type=body.connector_type,
        name=body.name,
        config=body.config,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/connectors")
async def list_connectors(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.connectors.read"))],
):
    result = await get_integration_service().list_connectors(tenant_id)
    return {"data": result.unwrap()}


@router.post("/webhooks", status_code=status.HTTP_201_CREATED)
async def create_webhook(
    body: CreateWebhookRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.webhooks.write"))],
):
    result = await get_integration_service().create_webhook(
        tenant_id=tenant_id,
        target_url=body.target_url,
        event_pattern=body.event_pattern,
        secret=body.secret,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/webhooks")
async def list_webhooks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.webhooks.read"))],
):
    result = await get_integration_service().list_webhooks(tenant_id)
    return {"data": result.unwrap()}


@router.post("/webhooks/{webhook_id}/test")
async def test_webhook(
    webhook_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.webhooks.write"))],
):
    result = await get_integration_service().test_webhook(tenant_id, correlation_id, webhook_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/sync-jobs", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync_job(
    body: TriggerSyncJobRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.sync.write"))],
):
    result = await get_integration_service().trigger_sync_job(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        connector_id=body.connector_id,
        job_type=body.job_type,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/logs")
async def list_logs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("integration.logs.read"))],
):
    result = await get_integration_service().list_logs(tenant_id)
    return {"data": result.unwrap()}
