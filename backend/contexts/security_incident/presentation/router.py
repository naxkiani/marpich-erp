"""Enterprise Security Incident Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions
from contexts.security_incident.container import get_security_incident_service
from contexts.security_incident.presentation.schemas import (
    ClassifyIncidentRequest,
    CollectEvidenceRequest,
    ContainIncidentRequest,
    DetectIncidentRequest,
    InvestigateIncidentRequest,
    NotifyIncidentRequest,
    RecordLessonRequest,
    RecoverIncidentRequest,
    ResolveIncidentRequest,
    RootCauseRequest,
)

security_incident_router = APIRouter(
    prefix="/security-incidents",
    tags=["Enterprise Security Incident Platform"],
)


@security_incident_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().list_catalog()).unwrap()}


@security_incident_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().get_dependency_map()).unwrap()}


@security_incident_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.write"))],
):
    return {"data": (await get_security_incident_service().seed(tenant_id)).unwrap()}


@security_incident_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().get_dashboard(tenant_id)).unwrap()}


@security_incident_router.get("/incidents")
async def list_incidents(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().list_incidents(tenant_id)).unwrap()}


@security_incident_router.post("/incidents", status_code=status.HTTP_201_CREATED)
async def detect_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: DetectIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("incident.write"))],
):
    result = await get_security_incident_service().detect_incident(
        tenant_id,
        title=body.title,
        description=body.description,
        classification=body.classification,
        severity=body.severity,
        detected_by=user.get("sub", ""),
        source_module=body.source_module,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.get("/incidents/{incident_ref}")
async def get_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    result = await get_security_incident_service().get_incident(tenant_id, incident_ref)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@security_incident_router.post("/incidents/{incident_ref}/classify")
async def classify_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: ClassifyIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().classify_incident(
        tenant_id, incident_ref,
        classification=body.classification,
        severity=body.severity,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/investigate")
async def investigate_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: InvestigateIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().investigate_incident(
        tenant_id, incident_ref,
        assigned_to=body.assigned_to or user.get("sub", ""),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/contain")
async def contain_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: ContainIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().contain_incident(
        tenant_id, incident_ref, actions=body.actions, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/recover")
async def recover_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: RecoverIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().recover_incident(
        tenant_id, incident_ref, actions=body.actions, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/root-cause")
async def set_root_cause(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: RootCauseRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().set_root_cause(
        tenant_id, incident_ref, root_cause=body.root_cause, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/forensics")
async def run_forensics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().run_forensics(
        tenant_id, incident_ref, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/escalate")
async def escalate_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.write"))],
):
    result = await get_security_incident_service().escalate_incident(
        tenant_id, incident_ref, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/resolve")
async def resolve_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: ResolveIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().resolve_incident(
        tenant_id, incident_ref, root_cause=body.root_cause, correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.post("/incidents/{incident_ref}/evidence", status_code=status.HTTP_201_CREATED)
async def collect_evidence(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: CollectEvidenceRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("incident.respond"))],
):
    result = await get_security_incident_service().collect_evidence(
        tenant_id, incident_ref,
        evidence_type=body.evidence_type,
        description=body.description,
        collected_by=user.get("sub", ""),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.get("/incidents/{incident_ref}/evidence")
async def list_evidence(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().list_evidence(tenant_id, incident_ref)).unwrap()}


@security_incident_router.post("/incidents/{incident_ref}/lessons", status_code=status.HTTP_201_CREATED)
async def record_lesson(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: RecordLessonRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("incident.write"))],
):
    result = await get_security_incident_service().record_lesson(
        tenant_id, incident_ref,
        title=body.title,
        summary=body.summary,
        recommendations=body.recommendations,
        author_id=user.get("sub", ""),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.get("/lessons")
async def list_lessons(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().list_lessons(tenant_id)).unwrap()}


@security_incident_router.post("/incidents/{incident_ref}/notify")
async def notify_incident(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    incident_ref: str,
    body: NotifyIncidentRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.write"))],
):
    result = await get_security_incident_service().notify_incident(
        tenant_id, incident_ref,
        channel=body.channel,
        recipient=body.recipient,
        subject=body.subject,
        message=body.message,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@security_incident_router.get("/notifications")
async def list_notifications(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().list_notifications(tenant_id)).unwrap()}


@security_incident_router.get("/sla")
async def get_sla_status(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("incident.read"))],
):
    return {"data": (await get_security_incident_service().get_sla_status(tenant_id)).unwrap()}
