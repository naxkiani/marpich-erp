"""Banking Settlement Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_settlement_engine_service
from contexts.banking.presentation.banking_settlement_schemas import (
    ApproveAdjustmentRequest,
    ApproveReconciliationRequest,
    CreateAdjustmentRequest,
    CreateReconciliationRequest,
    CreateSettlementBatchRequest,
    GenerateReportRequest,
    RaiseExceptionRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_settlement_router = APIRouter(
    prefix="/banking/settlement",
    tags=["Banking Settlement Engine"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_settlement_router.get("/catalog")
async def settlement_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    return {"data": (await get_banking_settlement_engine_service().list_catalog()).unwrap()}


@banking_settlement_router.get("/policy-keys")
async def settlement_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    return {"data": (await get_banking_settlement_engine_service().list_policy_keys()).unwrap()}


@banking_settlement_router.get("/dashboard")
async def settlement_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    return {"data": (await get_banking_settlement_engine_service().get_dashboard(tenant_id)).unwrap()}


@banking_settlement_router.post("/batches", status_code=status.HTTP_201_CREATED)
async def create_settlement_batch(
    body: CreateSettlementBatchRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().create_settlement_batch(
        tenant_id=tenant_id,
        settlement_type=body.settlement_type,
        currency=body.currency,
        items=[i.model_dump() for i in body.items],
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.get("/batches")
async def list_settlement_batches(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    return {"data": (await get_banking_settlement_engine_service().list_batches(tenant_id)).unwrap()}


@banking_settlement_router.get("/batches/{batch_id}")
async def get_settlement_batch(
    batch_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    result = await get_banking_settlement_engine_service().get_batch(batch_id=batch_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/batches/{batch_id}/submit")
async def submit_settlement_batch(
    batch_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().submit_batch(batch_id=batch_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/batches/{batch_id}/clear")
async def clear_settlement_batch(
    batch_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.execute"))],
):
    result = await get_banking_settlement_engine_service().run_clearing(batch_id=batch_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/batches/{batch_id}/settle")
async def settle_batch(
    batch_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.execute"))],
):
    result = await get_banking_settlement_engine_service().settle_batch(batch_id=batch_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/reconciliation/runs", status_code=status.HTTP_201_CREATED)
async def create_reconciliation_run(
    body: CreateReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().create_reconciliation_run(
        tenant_id=tenant_id,
        settlement_account=body.settlement_account,
        statement_items=body.statement_items,
        book_items=body.book_items,
        use_completed_transfers=body.use_completed_transfers,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/reconciliation/runs/{run_id}/match")
async def auto_match_reconciliation(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().auto_match_reconciliation(run_id=run_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/reconciliation/runs/{run_id}/analyze-differences")
async def analyze_reconciliation_differences(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    result = await get_banking_settlement_engine_service().analyze_reconciliation_differences(run_id=run_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/reconciliation/runs/{run_id}/approve")
async def approve_reconciliation(
    run_id: str,
    body: ApproveReconciliationRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.approve"))],
):
    result = await get_banking_settlement_engine_service().approve_reconciliation(
        run_id=run_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.get("/reconciliation/runs/{run_id}/audit")
async def reconciliation_audit(
    run_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    result = await get_banking_settlement_engine_service().get_reconciliation_audit(run_id=run_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/exceptions", status_code=status.HTTP_201_CREATED)
async def raise_settlement_exception(
    body: RaiseExceptionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().raise_exception(
        tenant_id=tenant_id,
        source_type=body.source_type,
        source_id=body.source_id,
        reason=body.reason,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/exceptions/{exception_id}/retry")
async def retry_settlement_exception(
    exception_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.execute"))],
):
    result = await get_banking_settlement_engine_service().retry_exception(exception_id=exception_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/adjustments", status_code=status.HTTP_201_CREATED)
async def create_settlement_adjustment(
    body: CreateAdjustmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.write"))],
):
    result = await get_banking_settlement_engine_service().create_adjustment(
        tenant_id=tenant_id,
        run_id=body.run_id,
        amount=body.amount,
        currency=body.currency,
        reason=body.reason,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/adjustments/{adjustment_id}/approve")
async def approve_settlement_adjustment(
    adjustment_id: str,
    body: ApproveAdjustmentRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.approve"))],
):
    result = await get_banking_settlement_engine_service().approve_adjustment(
        adjustment_id=adjustment_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_settlement_router.post("/reports", status_code=status.HTTP_201_CREATED)
async def generate_settlement_report(
    body: GenerateReportRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.settlement.read"))],
):
    result = await get_banking_settlement_engine_service().generate_report(
        tenant_id=tenant_id, report_type=body.report_type
    )
    _raise(result)
    return {"data": result.unwrap()}
