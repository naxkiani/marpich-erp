"""Enterprise Loan Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_loan_management_service
from contexts.banking.presentation.banking_loan_schemas import (
    ApplyLoanRequest,
    ApproveLoanRequest,
    CollateralRequest,
    CreditRiskAnalysisRequest,
    DisburseLoanRequest,
    EarlyCloseLoanRequest,
    GuarantorRequest,
    PayInstallmentRequest,
    RestructureLoanRequest,
    SettleLoanRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_loan_router = APIRouter(
    prefix="/banking/loans",
    tags=["Banking Loan Management"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_loan_router.get("/catalog")
async def loan_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    return {"data": (await get_banking_loan_management_service().list_catalog()).unwrap()}


@banking_loan_router.get("/policy-keys")
async def loan_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    return {"data": (await get_banking_loan_management_service().list_policy_keys()).unwrap()}


@banking_loan_router.get("/dashboard")
async def loan_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    return {"data": (await get_banking_loan_management_service().get_dashboard(tenant_id)).unwrap()}


@banking_loan_router.post("/apply", status_code=status.HTTP_201_CREATED)
async def apply_loan(
    body: ApplyLoanRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().apply_loan(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.get("")
async def list_loans(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    return {"data": (await get_banking_loan_management_service().list_loans(tenant_id)).unwrap()}


@banking_loan_router.get("/{loan_id}")
async def get_loan(
    loan_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    result = await get_banking_loan_management_service().get_loan(loan_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/submit")
async def submit_loan(
    loan_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().submit_loan(loan_id=loan_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/approve")
async def approve_loan(
    loan_id: str,
    body: ApproveLoanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.approve"))],
):
    result = await get_banking_loan_management_service().approve_loan(
        loan_id=loan_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/collateral", status_code=status.HTTP_201_CREATED)
async def add_collateral(
    loan_id: str,
    body: CollateralRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().add_collateral(
        tenant_id=tenant_id, loan_id=loan_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/guarantors", status_code=status.HTTP_201_CREATED)
async def add_guarantor(
    loan_id: str,
    body: GuarantorRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().add_guarantor(
        tenant_id=tenant_id, loan_id=loan_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/credit-risk", status_code=status.HTTP_201_CREATED)
async def analyze_credit_risk(
    loan_id: str,
    body: CreditRiskAnalysisRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().analyze_credit_risk(
        tenant_id=tenant_id, loan_id=loan_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/disburse")
async def disburse_loan(
    loan_id: str,
    body: DisburseLoanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.approve"))],
):
    result = await get_banking_loan_management_service().disburse_loan(
        loan_id=loan_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.get("/{loan_id}/schedule")
async def get_schedule(
    loan_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    result = await get_banking_loan_management_service().get_schedule(loan_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/installments/pay")
async def pay_installment(
    loan_id: str,
    body: PayInstallmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.write"))],
):
    result = await get_banking_loan_management_service().pay_installment(
        tenant_id=tenant_id,
        loan_id=loan_id,
        installment_id=body.installment_id,
        approver_id=body.approver_id,
        days_overdue=body.days_overdue,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/restructure")
async def restructure_loan(
    loan_id: str,
    body: RestructureLoanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.approve"))],
):
    result = await get_banking_loan_management_service().restructure_loan(
        loan_id=loan_id,
        tenure_months=body.tenure_months,
        interest_rate_annual=body.interest_rate_annual,
        approver_id=body.approver_id,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/settle")
async def settle_loan(
    loan_id: str,
    body: SettleLoanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.approve"))],
):
    result = await get_banking_loan_management_service().settle_loan(
        loan_id=loan_id, settlement_amount=body.settlement_amount, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.post("/{loan_id}/early-close")
async def early_close_loan(
    loan_id: str,
    body: EarlyCloseLoanRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.approve"))],
):
    result = await get_banking_loan_management_service().early_close_loan(
        loan_id=loan_id, closure_amount=body.closure_amount, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_loan_router.get("/{loan_id}/audit")
async def get_audit_trail(
    loan_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.lending.read"))],
):
    result = await get_banking_loan_management_service().get_audit_trail(loan_id)
    _raise(result)
    return {"data": result.unwrap()}
