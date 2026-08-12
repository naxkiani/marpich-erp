"""Accounting FastAPI router — hospital billings + AR invoices."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.accounting.container import get_accounting_service
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/accounting", tags=["Accounting"])


@router.get("/billings")
async def list_billings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().list_billings(tenant_id)
    return {"data": result.unwrap()}


@router.get("/billings/by-encounter/{encounter_id}")
async def get_billing_by_encounter(
    encounter_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().find_by_encounter(tenant_id, encounter_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/billings/{billing_id}")
async def get_billing(
    billing_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().get_billing(tenant_id, billing_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/invoices")
async def list_invoices(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.invoice.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_accounting_service().list_invoices(tenant_id, limit=limit, offset=offset)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/invoices/by-order/{order_id}")
async def get_invoice_by_order(
    order_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.invoice.read"))],
):
    result = await get_accounting_service().find_invoice_by_order(tenant_id, order_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/invoices/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.invoice.read"))],
):
    result = await get_accounting_service().get_invoice(tenant_id, invoice_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/invoices/{invoice_id}/issue")
async def issue_invoice(
    invoice_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.invoice.write"))],
):
    result = await get_accounting_service().issue_invoice(
        tenant_id=tenant_id,
        invoice_id=invoice_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
