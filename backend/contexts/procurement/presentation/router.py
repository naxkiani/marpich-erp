"""Procurement FastAPI router — CAP-ENT-040."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.procurement.container import get_procurement_service

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.get("/requisitions")
async def list_requisitions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("procurement.requisitions.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_procurement_service().list_requisitions(
        tenant_id, limit=limit, offset=offset
    )
    return {"data": result.unwrap()}


@router.post("/requisitions/{requisition_id}/submit")
async def submit_requisition(
    requisition_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("procurement.requisitions.write"))],
):
    result = await get_procurement_service().submit_requisition(
        tenant_id=tenant_id,
        requisition_id=requisition_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/requisitions/{requisition_id}/approve")
async def approve_requisition(
    requisition_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("procurement.requisitions.write"))],
):
    result = await get_procurement_service().approve_requisition(
        tenant_id=tenant_id,
        requisition_id=requisition_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/requisitions/{requisition_id}/receive")
async def receive_goods(
    requisition_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("procurement.requisitions.write"))],
):
    result = await get_procurement_service().receive_goods(
        tenant_id=tenant_id,
        requisition_id=requisition_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
