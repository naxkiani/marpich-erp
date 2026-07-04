"""Compliance FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.compliance.container import get_compliance_service
from contexts.compliance.presentation.schemas import CreateReportRequest, ResolveViolationRequest
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/domains")
async def list_domains(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.read"))],
):
    return {"data": (await get_compliance_service().list_domains()).unwrap()}


@router.get("/controls")
async def list_controls(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.read"))],
    domain: Annotated[str | None, Query()] = None,
):
    return {"data": (await get_compliance_service().list_controls(tenant_id, domain=domain)).unwrap()}


@router.get("/violations")
async def query_violations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.violations.read"))],
    domain: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    severity: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_compliance_service().query_violations(
        tenant_id, domain=domain, status=status, severity=severity, limit=limit, offset=offset
    )
    return {"data": result.unwrap()}


@router.get("/violations/{violation_id}")
async def get_violation(
    violation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.violations.read"))],
):
    result = await get_compliance_service().get_violation(tenant_id, violation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/violations/{violation_id}/resolve")
async def resolve_violation(
    violation_id: str,
    body: ResolveViolationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("compliance.violations.write"))],
):
    result = await get_compliance_service().resolve_violation(
        tenant_id, violation_id, actor_id=user.get("sub"), notes=body.notes
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/dashboard")
async def get_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.dashboard.read"))],
):
    return {"data": (await get_compliance_service().get_dashboard(tenant_id)).unwrap()}


@router.get("/alerts")
async def get_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.alerts.read"))],
):
    return {"data": (await get_compliance_service().get_alerts(tenant_id)).unwrap()}


@router.get("/retention/status")
async def get_retention_status(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.retention.read"))],
):
    result = await get_compliance_service().get_retention_status(tenant_id)
    return {"data": result.unwrap()}


@router.post("/reports", status_code=status.HTTP_202_ACCEPTED)
async def create_report(
    body: CreateReportRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("compliance.reports.write"))],
):
    filters = {k: v for k, v in {"date_from": body.date_from, "date_to": body.date_to}.items() if v}
    result = await get_compliance_service().create_report(
        tenant_id=tenant_id,
        report_type=body.report_type,
        domain=body.domain,
        export_format=body.format,
        filters=filters,
        requested_by=user.get("sub"),
        correlation_id=correlation_id,
    )
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/reports")
async def list_reports(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.reports.read"))],
):
    return {"data": (await get_compliance_service().list_reports(tenant_id)).unwrap()}


@router.get("/reports/{report_id}")
async def get_report(
    report_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("compliance.reports.read"))],
):
    result = await get_compliance_service().get_report(tenant_id, report_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
