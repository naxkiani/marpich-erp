"""Enterprise Financial Audit API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_audit_service
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

financial_audit_router = APIRouter(
    prefix="/financial-kernel/audit", tags=["Financial Audit"]
)


@financial_audit_router.get("/catalog")
async def list_audit_catalog(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    return {"data": (await get_financial_audit_service().list_catalog()).unwrap()}


@financial_audit_router.get("/entries")
async def list_audit_entries(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_audit_service().list_by_tenant(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_audit_router.get("/entries/{entry_id}")
async def get_audit_entry(
    entry_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_audit_service().get_entry(tenant_id, entry_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_audit_router.get("/history")
async def get_immutable_audit_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
    resource_type: str = Query(...),
    resource_id: str = Query(...),
):
    result = await get_financial_audit_service().get_resource_history(
        tenant_id, resource_type, resource_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_audit_router.get("/verify-chain")
async def verify_audit_chain(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_audit_service().verify_chain(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_audit_router.get("/entries/{entry_id}/verify")
async def verify_audit_entry(
    entry_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_audit_service().verify_entry_tamper(tenant_id, entry_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@financial_audit_router.delete("/entries/{entry_id}")
async def delete_audit_entry_forbidden(
    entry_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.security.audit"))],
):
    result = await get_financial_audit_service().attempt_delete(entry_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_403_FORBIDDEN, result.error)
    return {"data": result.unwrap()}
