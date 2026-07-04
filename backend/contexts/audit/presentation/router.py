"""Audit FastAPI router."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.audit.container import get_audit_service
from contexts.audit.presentation.schemas import CreateExportRequest, RecordEntryRequest
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/entries")
async def query_entries(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("audit.entries.read"))],
    event_name: Annotated[str | None, Query()] = None,
    severity: Annotated[str | None, Query()] = None,
    actor_id: Annotated[str | None, Query()] = None,
    date_from: Annotated[str | None, Query()] = None,
    date_to: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    parsed_from = datetime.fromisoformat(date_from) if date_from else None
    parsed_to = datetime.fromisoformat(date_to) if date_to else None
    result = await get_audit_service().query_entries(
        tenant_id,
        event_name=event_name,
        severity=severity,
        actor_id=actor_id,
        date_from=parsed_from,
        date_to=parsed_to,
        limit=limit,
        offset=offset,
    )
    return {"data": result.unwrap()}


@router.get("/entries/{entry_id}")
async def get_entry(
    entry_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("audit.entries.read"))],
):
    result = await get_audit_service().get_entry(tenant_id, entry_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/entries", status_code=status.HTTP_201_CREATED)
async def record_entry(
    body: RecordEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("audit.entries.write"))],
):
    result = await get_audit_service().record_direct(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        action=body.action,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
        actor_id=user["sub"],
        severity=body.severity,
        payload=body.payload,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/exports", status_code=status.HTTP_202_ACCEPTED)
async def create_export(
    body: CreateExportRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("audit.exports.write"))],
):
    filters = {
        k: v
        for k, v in {
            "event_name": body.event_name,
            "severity": body.severity,
            "actor_id": body.actor_id,
            "date_from": body.date_from,
            "date_to": body.date_to,
        }.items()
        if v is not None
    }
    result = await get_audit_service().create_export(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        export_format=body.format,
        filters=filters,
        requested_by=user["sub"],
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/exports/{export_id}")
async def get_export(
    export_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("audit.exports.read"))],
):
    result = await get_audit_service().get_export(tenant_id, export_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/stats")
async def get_stats(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("audit.entries.read"))],
):
    result = await get_audit_service().get_stats(tenant_id)
    return {"data": result.unwrap()}
