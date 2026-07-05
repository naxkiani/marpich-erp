"""Deposit Management API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_deposit_management_service
from contexts.banking.presentation.banking_deposit_schemas import (
    AccrueInterestRequest,
    ApproveDepositRequest,
    ApproveTransactionRequest,
    DepositTransactionRequest,
    GenerateStatementRequest,
    OpenDepositRequest,
    PostInterestRequest,
    ProfitRuleRequest,
    RenewDepositRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_deposit_router = APIRouter(
    prefix="/banking/deposits",
    tags=["Banking Deposit Management"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_deposit_router.get("/catalog")
async def deposit_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().list_catalog()).unwrap()}


@banking_deposit_router.get("/policy-keys")
async def deposit_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().list_policy_keys()).unwrap()}


@banking_deposit_router.get("/dashboard")
async def deposit_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().get_dashboard(tenant_id)).unwrap()}


@banking_deposit_router.post("/open", status_code=status.HTTP_201_CREATED)
async def open_deposit(
    body: OpenDepositRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.write"))],
):
    result = await get_banking_deposit_management_service().open_deposit(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.get("")
async def list_deposits(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().list_deposits(tenant_id)).unwrap()}


@banking_deposit_router.get("/{deposit_id}")
async def get_deposit(
    deposit_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    result = await get_banking_deposit_management_service().get_deposit(deposit_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/{deposit_id}/approve")
async def approve_deposit(
    deposit_id: str,
    body: ApproveDepositRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.approve"))],
):
    result = await get_banking_deposit_management_service().approve_deposit(
        deposit_id=deposit_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    body: DepositTransactionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.deposits.write"))],
):
    result = await get_banking_deposit_management_service().create_deposit_transaction(
        tenant_id=tenant_id,
        deposit_id=body.deposit_id,
        transaction_type=body.transaction_type,
        amount=body.amount,
        actor_id=user.get("sub"),
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/transactions/{transaction_id}/approve")
async def approve_transaction(
    transaction_id: str,
    body: ApproveTransactionRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.approve"))],
):
    result = await get_banking_deposit_management_service().approve_transaction(
        transaction_id=transaction_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/interest/accrue")
async def accrue_interest(
    body: AccrueInterestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.write"))],
):
    result = await get_banking_deposit_management_service().accrue_interest(
        tenant_id=tenant_id, deposit_id=body.deposit_id, days=body.days
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/interest/post")
async def post_interest(
    body: PostInterestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.approve"))],
):
    result = await get_banking_deposit_management_service().post_accrued_interest(
        tenant_id=tenant_id, deposit_id=body.deposit_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/{deposit_id}/maturity")
async def process_maturity(
    deposit_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.approve"))],
):
    result = await get_banking_deposit_management_service().process_maturity(deposit_id=deposit_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/{deposit_id}/renew")
async def renew_deposit(
    deposit_id: str,
    body: RenewDepositRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.approve"))],
):
    result = await get_banking_deposit_management_service().renew_deposit(
        deposit_id=deposit_id,
        tenure_months=body.tenure_months,
        interest_rate_annual=body.interest_rate_annual,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/{deposit_id}/certificate", status_code=status.HTTP_201_CREATED)
async def issue_certificate(
    deposit_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.write"))],
):
    result = await get_banking_deposit_management_service().issue_certificate(
        tenant_id=tenant_id, deposit_id=deposit_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/{deposit_id}/statement", status_code=status.HTTP_201_CREATED)
async def generate_statement(
    deposit_id: str,
    body: GenerateStatementRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    result = await get_banking_deposit_management_service().generate_statement(
        tenant_id=tenant_id, deposit_id=deposit_id, period_days=body.period_days
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.post("/profit-rules", status_code=status.HTTP_201_CREATED)
async def create_profit_rule(
    body: ProfitRuleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.write"))],
):
    result = await get_banking_deposit_management_service().create_profit_rule(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_deposit_router.get("/profit-rules/list")
async def list_profit_rules(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().list_profit_rules(tenant_id)).unwrap()}


@banking_deposit_router.get("/{deposit_id}/audit")
async def deposit_audit(
    deposit_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.deposits.read"))],
):
    return {"data": (await get_banking_deposit_management_service().get_audit_trail(deposit_id)).unwrap()}
