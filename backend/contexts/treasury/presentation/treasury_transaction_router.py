"""Treasury Transaction Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_treasury_transaction_service
from contexts.treasury.presentation.treasury_transaction_schemas import (
    ApproveTransactionRequest,
    CreateTreasuryTransactionRequest,
    RejectTransactionRequest,
)

treasury_transaction_router = APIRouter(
    prefix="/treasury/transactions",
    tags=["Treasury Transaction Engine"],
)


@treasury_transaction_router.get("/catalog")
async def transaction_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    return {"data": (await get_treasury_transaction_service().list_catalog()).unwrap()}


@treasury_transaction_router.get("/workflow")
async def transaction_workflow(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    return {"data": (await get_treasury_transaction_service().list_workflow()).unwrap()}


@treasury_transaction_router.get("/posting-rules")
async def transaction_posting_rules(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    return {"data": (await get_treasury_transaction_service().list_posting_rule_map()).unwrap()}


@treasury_transaction_router.get("/dashboard")
async def transaction_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    return {"data": (await get_treasury_transaction_service().get_dashboard(tenant_id)).unwrap()}


@treasury_transaction_router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    body: CreateTreasuryTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.write"))],
):
    result = await get_treasury_transaction_service().create_transaction(
        tenant_id=tenant_id,
        transaction_type=body.transaction_type,
        amount=body.amount,
        currency=body.currency,
        reference=body.reference,
        description=body.description,
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        metadata=body.metadata,
        auto_submit=body.auto_submit,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_transaction_router.get("")
async def list_transactions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    return {"data": (await get_treasury_transaction_service().list_transactions(tenant_id)).unwrap()}


@treasury_transaction_router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.read"))],
):
    result = await get_treasury_transaction_service().get_transaction(transaction_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@treasury_transaction_router.post("/{transaction_id}/submit")
async def submit_transaction(
    transaction_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.write"))],
):
    result = await get_treasury_transaction_service().submit_transaction(
        transaction_id, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_transaction_router.post("/{transaction_id}/approve")
async def approve_transaction(
    transaction_id: str,
    body: ApproveTransactionRequest,
    user: Annotated[dict, Depends(require_permissions("treasury.transactions.approve"))],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
):
    result = await get_treasury_transaction_service().approve_transaction(
        transaction_id,
        approver_id=str(user.get("id", user.get("sub", "system"))),
        correlation_id=correlation_id,
        comment=body.comment,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_transaction_router.post("/{transaction_id}/reject")
async def reject_transaction(
    transaction_id: str,
    body: RejectTransactionRequest,
    user: Annotated[dict, Depends(require_permissions("treasury.transactions.approve"))],
):
    result = await get_treasury_transaction_service().reject_transaction(
        transaction_id,
        approver_id=str(user.get("id", user.get("sub", "system"))),
        comment=body.comment,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@treasury_transaction_router.post("/{transaction_id}/cancel")
async def cancel_transaction(
    transaction_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.transactions.write"))],
):
    result = await get_treasury_transaction_service().cancel_transaction(transaction_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
