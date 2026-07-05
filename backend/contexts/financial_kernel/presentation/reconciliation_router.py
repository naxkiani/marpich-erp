"""Enterprise Reconciliation Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    CreateReconciliationRunRequest,
    ManualMatchRequest,
    RejectReconciliationRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

reconciliation_router = APIRouter(
    prefix="/financial-kernel/reconciliation", tags=["Reconciliation"]
)


@reconciliation_router.get("/catalog")
async def list_reconciliation_catalog(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_reconciliation_catalog()
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs")
async def list_reconciliation_runs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
    reconciliation_type: str | None = Query(None),
):
    result = await get_financial_kernel_service().list_reconciliation_runs(
        tenant_id, reconciliation_type=reconciliation_type
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs", status_code=status.HTTP_201_CREATED)
async def create_reconciliation_run(
    body: CreateReconciliationRunRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().create_reconciliation_run(
        tenant_id=tenant_id,
        reconciliation_type=body.reconciliation_type,
        reconciliation_date=body.reconciliation_date,
        reference_id=body.reference_id,
        reference_label=body.reference_label or body.reconciliation_type,
        left_items=body.left_items,
        right_items=body.right_items,
        period_id=body.period_id,
        actor_id=user.get("sub", "system"),
        auto_match=body.auto_match,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}")
async def get_reconciliation_run(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_reconciliation_run(tenant_id, run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs/{run_id}/auto-match")
async def run_automatic_match(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().run_automatic_match(
        tenant_id, run_id, actor_id=user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs/{run_id}/manual-match")
async def apply_manual_match(
    run_id: str,
    body: ManualMatchRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().apply_reconciliation_manual_match(
        tenant_id=tenant_id,
        run_id=run_id,
        left_item=body.left_item,
        right_item=body.right_item,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}/exceptions")
async def get_reconciliation_exceptions(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_reconciliation_exceptions(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}/ai-suggestions")
async def get_reconciliation_ai_suggestions(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_reconciliation_ai_suggestions(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}/difference-analysis")
async def get_difference_analysis(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_reconciliation_difference_analysis(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}/report")
async def get_reconciliation_report(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_reconciliation_report(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs/{run_id}/submit")
async def submit_reconciliation_for_approval(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().submit_reconciliation_for_approval(
        tenant_id, run_id, actor_id=user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs/{run_id}/approve")
async def approve_reconciliation(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().approve_reconciliation(
        tenant_id, run_id, actor_id=user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.post("/runs/{run_id}/reject")
async def reject_reconciliation(
    run_id: str,
    body: RejectReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.journals.post"))],
):
    result = await get_financial_kernel_service().reject_reconciliation(
        tenant_id,
        run_id,
        actor_id=user.get("sub", "system"),
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@reconciliation_router.get("/runs/{run_id}/audit")
async def list_reconciliation_audit_history(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_reconciliation_audit_history(
        tenant_id, run_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
