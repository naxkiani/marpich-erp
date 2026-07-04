"""Analytics FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.analytics.container import get_analytics_service
from contexts.analytics.presentation.schemas import CreateAlertRequest
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/metrics")
async def list_metrics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.metrics.read"))],
):
    result = await get_analytics_service().list_metrics(tenant_id)
    return {"data": result.unwrap()}


@router.get("/metrics/{metric_key}/timeseries")
async def get_timeseries(
    metric_key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.metrics.read"))],
):
    result = await get_analytics_service().get_timeseries(tenant_id, metric_key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/dashboards")
async def list_dashboards(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
):
    result = await get_analytics_service().list_dashboards(tenant_id)
    return {"data": result.unwrap()}


@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(
    dashboard_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
):
    result = await get_analytics_service().get_dashboard(tenant_id, dashboard_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/alerts", status_code=status.HTTP_201_CREATED)
async def create_alert(
    body: CreateAlertRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.alerts.write"))],
):
    result = await get_analytics_service().create_alert(
        tenant_id=tenant_id,
        metric_key=body.metric_key,
        name=body.name,
        threshold=body.threshold,
        operator=body.operator,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/alerts")
async def list_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.alerts.write"))],
):
    result = await get_analytics_service().list_alerts(tenant_id)
    return {"data": result.unwrap()}


@router.get("/events/summary")
async def get_events_summary(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.events.read"))],
):
    result = await get_analytics_service().get_events_summary(tenant_id)
    return {"data": result.unwrap()}
