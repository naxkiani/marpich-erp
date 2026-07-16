"""Enterprise Observability Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.enterprise_observability.container import get_enterprise_observability_service
from contexts.enterprise_observability.presentation.schemas import (
    CreateAlertRequest,
    CreateIncidentRequest,
    IngestLogRequest,
    RecordTraceRequest,
    ResolveIncidentRequest,
)
from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions

enterprise_observability_router = APIRouter(
    prefix="/enterprise-observability",
    tags=["Enterprise Observability"],
)


@enterprise_observability_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_catalog()).unwrap()}


@enterprise_observability_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_dependency_map()).unwrap()}


@enterprise_observability_router.get("/threat-map")
async def threat_map(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_threat_map(tenant_id)).unwrap()}


@enterprise_observability_router.get("/service-dependency-graph")
async def service_dependency_graph(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_service_dependency_graph()).unwrap()}


@enterprise_observability_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.write"))],
):
    return {"data": (await get_enterprise_observability_service().seed(tenant_id)).unwrap()}


@enterprise_observability_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_dashboard(tenant_id)).unwrap()}


@enterprise_observability_router.get("/operational-dashboard")
async def operational_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_operational_dashboard(tenant_id)).unwrap()}


@enterprise_observability_router.get("/health-dashboard")
async def health_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_operational_dashboard(tenant_id)).unwrap()}


@enterprise_observability_router.get("/traces")
async def list_traces(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_traces(tenant_id)).unwrap()}


@enterprise_observability_router.get("/traces/{trace_ref}")
async def get_trace(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    trace_ref: str,
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    result = await get_enterprise_observability_service().get_trace(tenant_id, trace_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@enterprise_observability_router.post("/traces")
async def record_trace(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RecordTraceRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.write"))],
):
    result = await get_enterprise_observability_service().record_trace(
        tenant_id,
        span_name=body.span_name,
        service_name=body.service_name,
        duration_ms=body.duration_ms,
        correlation_id=correlation_id,
        status=body.status,
        context_name=body.context_name,
        parent_ref=body.parent_ref,
        attributes=body.attributes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@enterprise_observability_router.get("/logs")
async def list_logs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_logs(tenant_id)).unwrap()}


@enterprise_observability_router.post("/logs")
async def ingest_log(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: IngestLogRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.write"))],
):
    return {"data": (await get_enterprise_observability_service().ingest_log(
        tenant_id,
        level=body.level,
        logger=body.logger,
        message=body.message,
        correlation_id=correlation_id,
        context_name=body.context_name,
        duration_ms=body.duration_ms,
        status=body.status,
        metadata=body.metadata,
    )).unwrap()}


@enterprise_observability_router.get("/metrics")
async def list_metrics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_metrics(tenant_id)).unwrap()}


@enterprise_observability_router.get("/health-checks")
async def health_checks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_health_checks(tenant_id)).unwrap()}


@enterprise_observability_router.get("/business-kpis")
async def business_kpis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_business_kpis(tenant_id)).unwrap()}


@enterprise_observability_router.get("/events")
async def event_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_event_monitoring(tenant_id)).unwrap()}


@enterprise_observability_router.get("/queues")
async def queue_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_queue_monitoring(tenant_id)).unwrap()}


@enterprise_observability_router.get("/api-monitoring")
async def api_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_api_monitoring(tenant_id)).unwrap()}


@enterprise_observability_router.get("/workflows")
async def workflow_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_workflow_monitoring(tenant_id)).unwrap()}


@enterprise_observability_router.get("/ai-monitoring")
async def ai_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().get_ai_monitoring(tenant_id)).unwrap()}


@enterprise_observability_router.get("/alerts")
async def list_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_alerts(tenant_id)).unwrap()}


@enterprise_observability_router.post("/alerts")
async def create_alert(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateAlertRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.write"))],
):
    return {"data": (await get_enterprise_observability_service().create_alert(
        tenant_id,
        signal=body.signal,
        metric_key=body.metric_key,
        operator=body.operator,
        threshold=body.threshold,
        severity=body.severity,
    )).unwrap()}


@enterprise_observability_router.get("/incidents")
async def list_incidents(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.read"))],
):
    return {"data": (await get_enterprise_observability_service().list_incidents(tenant_id)).unwrap()}


@enterprise_observability_router.post("/incidents")
async def create_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: CreateIncidentRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.write"))],
):
    return {"data": (await get_enterprise_observability_service().create_incident(
        tenant_id,
        title=body.title,
        severity=body.severity,
        source_signal=body.source_signal,
        summary=body.summary,
        correlation_id=body.correlation_id,
    )).unwrap()}


@enterprise_observability_router.post("/incidents/{incident_ref}/resolve")
async def resolve_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: ResolveIncidentRequest,
    _user: Annotated[dict, Depends(require_permissions("enterprise_observability.admin"))],
):
    result = await get_enterprise_observability_service().resolve_incident(
        tenant_id, incident_ref, resolution_summary=body.resolution_summary
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
