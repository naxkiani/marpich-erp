"""Enterprise Financial Validation Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import ValidateTransactionRequest
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

financial_validation_router = APIRouter(
    prefix="/financial-kernel/validation", tags=["Financial Validation"]
)


@financial_validation_router.get("/catalog")
async def list_validation_catalog(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().list_validation_catalog()
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_validation_router.post("/validate")
async def validate_transaction(
    body: ValidateTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().validate_transaction(
        tenant_id=tenant_id,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        lines=body.lines,
        currency=body.currency,
        base_currency=body.base_currency,
        exchange_rate=body.exchange_rate,
        period_id=body.period_id,
        idempotency_key=body.idempotency_key,
        posting_mode=body.posting_mode,
        requires_approval=body.requires_approval,
        journal_entry_type=body.journal_entry_type,
        user_permissions=user.get("permissions"),
        actor_id=user.get("sub", "system"),
        persist=body.persist,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_validation_router.get("/runs")
async def list_validation_runs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().list_validation_runs(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@financial_validation_router.get("/runs/{run_id}")
async def get_validation_run(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().get_validation_run(tenant_id, run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@financial_validation_router.get("/runs/{run_id}/audit")
async def list_validation_audit(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.read"))],
):
    result = await get_financial_kernel_service().list_validation_audit_history(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
