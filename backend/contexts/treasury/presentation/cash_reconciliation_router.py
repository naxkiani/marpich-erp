"""Enterprise Cash Reconciliation API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_cash_reconciliation_service
from contexts.treasury.presentation.cash_reconciliation_schemas import (
    BranchClosingRequest,
    CashCountRequest,
    RejectVarianceRequest,
    ShiftClosingRequest,
)

cash_reconciliation_router = APIRouter(
    prefix="/treasury/cash-reconciliation",
    tags=["Enterprise Cash Reconciliation"],
)


@cash_reconciliation_router.get("/catalog")
async def cash_reconciliation_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    return {"data": (await get_cash_reconciliation_service().list_catalog()).unwrap()}


@cash_reconciliation_router.get("/workflow")
async def cash_reconciliation_workflow(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    return {"data": (await get_cash_reconciliation_service().list_workflow()).unwrap()}


@cash_reconciliation_router.get("/dashboard")
async def cash_reconciliation_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    return {"data": (await get_cash_reconciliation_service().get_dashboard(tenant_id)).unwrap()}


@cash_reconciliation_router.post("/counts", status_code=status.HTTP_201_CREATED)
async def perform_cash_count(
    body: CashCountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.write"))],
):
    result = await get_cash_reconciliation_service().perform_cash_count(
        tenant_id=tenant_id,
        location_id=body.location_id,
        counted_amount=body.counted_amount,
        closing_type=body.closing_type,
        counted_by=str(user.get("id", user.get("sub"))),
        notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/shift-closing", status_code=status.HTTP_201_CREATED)
async def perform_shift_closing(
    body: ShiftClosingRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.write"))],
):
    result = await get_cash_reconciliation_service().perform_cash_count(
        tenant_id=tenant_id,
        location_id=body.location_id,
        counted_amount=body.counted_amount,
        closing_type="shift_closing",
        counted_by=str(user.get("id", user.get("sub"))),
        notes=body.notes,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/branch-closing", status_code=status.HTTP_201_CREATED)
async def perform_branch_closing(
    body: BranchClosingRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.write"))],
):
    result = await get_cash_reconciliation_service().perform_branch_closing(
        tenant_id=tenant_id,
        branch_id=body.branch_id,
        location_counts=[i.model_dump() for i in body.location_counts],
        closed_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.get("/runs")
async def list_cash_reconciliation_runs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
    location_id: str | None = Query(default=None),
):
    return {"data": (await get_cash_reconciliation_service().list_runs(tenant_id, location_id)).unwrap()}


@cash_reconciliation_router.get("/runs/{run_id}")
async def get_cash_reconciliation_run(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    result = await get_cash_reconciliation_service().get_run(run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/runs/{run_id}/verify")
async def verify_cash_count(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.write"))],
):
    result = await get_cash_reconciliation_service().verify_count(
        run_id,
        tenant_id=tenant_id,
        verified_by=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/runs/{run_id}/approve")
async def approve_cash_variance(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.approve"))],
):
    result = await get_cash_reconciliation_service().approve_variance(
        run_id,
        tenant_id=tenant_id,
        manager_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/runs/{run_id}/reject")
async def reject_cash_variance(
    run_id: str,
    body: RejectVarianceRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.approve"))],
):
    result = await get_cash_reconciliation_service().reject_variance(
        run_id,
        tenant_id=tenant_id,
        manager_id=str(user.get("id", user.get("sub"))),
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.post("/runs/{run_id}/close")
async def close_cash_reconciliation(
    run_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.write"))],
):
    result = await get_cash_reconciliation_service().close_reconciliation(
        run_id,
        tenant_id=tenant_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.get("/runs/{run_id}/discrepancy-report")
async def get_discrepancy_report(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    result = await get_cash_reconciliation_service().get_discrepancy_report(run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.get("/runs/{run_id}/ai-anomalies")
async def get_ai_anomalies(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    result = await get_cash_reconciliation_service().get_ai_anomalies(run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@cash_reconciliation_router.get("/runs/{run_id}/audit")
async def cash_reconciliation_audit(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.cash_reconciliation.read"))],
):
    result = await get_cash_reconciliation_service().get_audit_trail(run_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
