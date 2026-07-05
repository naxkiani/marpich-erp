"""Enterprise Subledger Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    PostSubledgerEntryRequest,
    RunSubledgerReconciliationRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

subledger_router = APIRouter(
    prefix="/financial-kernel/subledgers", tags=["Subledgers"]
)


@subledger_router.get("/catalog")
async def list_subledger_catalog(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_subledger_catalog()
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("")
async def list_subledgers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_subledgers(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@subledger_router.post("/entries", status_code=status.HTTP_201_CREATED)
async def post_subledger_entry(
    body: PostSubledgerEntryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().post_subledger_entry(
        tenant_id=tenant_id,
        subledger_type=body.subledger_type,
        source_document_id=body.source_document_id,
        amount=body.amount,
        entry_date=body.entry_date,
        currency=body.currency,
        reference=body.reference,
        counterparty=body.counterparty,
        description=body.description,
        dimensions=body.dimensions,
        account_mappings=body.account_mappings,
        idempotency_key=body.idempotency_key,
        correlation_id=correlation_id,
        organization_id=body.organization_id,
        branch_id=body.branch_id,
        tax_amount=body.tax_amount,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/entries/{entry_id}")
async def get_subledger_entry(
    entry_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_subledger_entry(tenant_id, entry_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@subledger_router.post("/entries/{entry_id}/reverse")
async def reverse_subledger_entry(
    entry_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().reverse_subledger_entry(
        tenant_id=tenant_id,
        entry_id=entry_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/reconciliations/{reconciliation_id}")
async def get_subledger_reconciliation(
    reconciliation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_subledger_reconciliation(
        tenant_id, reconciliation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/types/{subledger_type}")
async def get_subledger_by_type(
    subledger_type: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_subledger_by_type(
        tenant_id, subledger_type
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/{subledger_id}")
async def get_subledger(
    subledger_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_subledger(tenant_id, subledger_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/{subledger_id}/entries")
async def list_subledger_entries(
    subledger_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_subledger_entries(
        tenant_id, subledger_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@subledger_router.post("/{subledger_id}/reconcile", status_code=status.HTTP_201_CREATED)
async def run_subledger_reconciliation(
    subledger_id: str,
    body: RunSubledgerReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().run_subledger_reconciliation(
        tenant_id=tenant_id,
        subledger_id=subledger_id,
        reconciliation_date=body.reconciliation_date,
        period_id=body.period_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@subledger_router.get("/{subledger_id}/reconciliations")
async def list_subledger_reconciliations(
    subledger_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_subledger_reconciliations(
        tenant_id, subledger_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
