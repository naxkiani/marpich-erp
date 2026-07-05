"""Enterprise Bank Reconciliation API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_bank_reconciliation_service
from contexts.treasury.presentation.bank_reconciliation_schemas import (
    BankApiImportRequest,
    CreateBankReconciliationRequest,
    ImportStatementRequest,
    ManualMatchRequest,
    RejectReconciliationRequest,
)

bank_reconciliation_router = APIRouter(
    prefix="/treasury/bank-reconciliation",
    tags=["Enterprise Bank Reconciliation"],
)


@bank_reconciliation_router.get("/catalog")
async def reconciliation_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_bank_reconciliation_service().list_catalog()).unwrap()}


@bank_reconciliation_router.get("/workflow")
async def reconciliation_workflow(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_bank_reconciliation_service().list_workflow()).unwrap()}


@bank_reconciliation_router.get("/dashboard")
async def reconciliation_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_bank_reconciliation_service().get_dashboard(tenant_id)).unwrap()}


@bank_reconciliation_router.post("/statements/import", status_code=status.HTTP_201_CREATED)
async def import_statement(
    body: ImportStatementRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_bank_reconciliation_service().import_statement(
        tenant_id=tenant_id,
        treasury_account_id=body.treasury_account_id,
        source=body.source,
        statement_date=body.statement_date,
        statement_balance=body.statement_balance,
        items=[i.model_dump() for i in body.items],
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.post("/statements/bank-api", status_code=status.HTTP_201_CREATED)
async def import_bank_api(
    body: BankApiImportRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_bank_reconciliation_service().import_from_bank_api(
        tenant_id=tenant_id,
        treasury_account_id=body.treasury_account_id,
        statement_date=body.statement_date,
        api_payload=body.api_payload,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/statements")
async def list_statements(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_bank_reconciliation_service().list_statements(tenant_id)).unwrap()}


@bank_reconciliation_router.post("", status_code=status.HTTP_201_CREATED)
async def create_reconciliation(
    body: CreateBankReconciliationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_bank_reconciliation_service().create_reconciliation(
        tenant_id=tenant_id,
        treasury_account_id=body.treasury_account_id,
        reconciliation_date=body.reconciliation_date,
        statement_balance=body.statement_balance,
        statement_items=[i.model_dump() for i in body.statement_items],
        book_items=[i.model_dump() for i in body.book_items] if body.book_items else None,
        statement_import_id=body.statement_import_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("")
async def list_reconciliations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    return {"data": (await get_bank_reconciliation_service().list_reconciliations(tenant_id)).unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}")
async def get_reconciliation(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_reconciliation(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.post("/{reconciliation_id}/match")
async def manual_match(
    reconciliation_id: str,
    body: ManualMatchRequest,
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_bank_reconciliation_service().manual_match_items(
        reconciliation_id,
        statement_item=body.statement_item,
        book_item=body.book_item,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}/exceptions")
async def exception_queue(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_exceptions(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}/outstanding")
async def outstanding_transactions(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_outstanding(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}/ai-suggestions")
async def ai_suggestions(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_ai_suggestions(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}/report")
async def reconciliation_report(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_report(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.post("/{reconciliation_id}/submit")
async def submit_reconciliation(
    reconciliation_id: str,
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.write"))],
):
    result = await get_bank_reconciliation_service().submit_for_approval(
        reconciliation_id, actor_id=str(user.get("id", user.get("sub")))
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.post("/{reconciliation_id}/approve")
async def approve_reconciliation(
    reconciliation_id: str,
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.approve"))],
):
    result = await get_bank_reconciliation_service().approve(
        reconciliation_id, actor_id=str(user.get("id", user.get("sub")))
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.post("/{reconciliation_id}/reject")
async def reject_reconciliation(
    reconciliation_id: str,
    body: RejectReconciliationRequest,
    user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.approve"))],
):
    result = await get_bank_reconciliation_service().reject(
        reconciliation_id,
        actor_id=str(user.get("id", user.get("sub"))),
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@bank_reconciliation_router.get("/{reconciliation_id}/audit")
async def reconciliation_audit(
    reconciliation_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.reconciliation.read"))],
):
    result = await get_bank_reconciliation_service().get_audit_trail(reconciliation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
