"""Banking Customer and Account API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_customer_account_service
from contexts.banking.presentation.banking_customer_account_schemas import (
    CreateCustomerRequest,
    CreateKycRequest,
    CreateProductRequest,
    OpenAccountRequest,
    OverdraftCheckRequest,
    TransitionStatusRequest,
    UpdateKycStatusRequest,
    UpdateRiskRatingRequest,
    VerifyKycRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_customer_account_router = APIRouter(
    prefix="/banking",
    tags=["Banking Customer & Account"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_customer_account_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_catalog()).unwrap()}


@banking_customer_account_router.get("/account-status-workflow")
async def account_status_workflow(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_status_workflow()).unwrap()}


@banking_customer_account_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().get_dashboard(tenant_id)).unwrap()}


@banking_customer_account_router.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(
    body: CreateCustomerRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.customers.write"))],
):
    result = await get_banking_customer_account_service().create_customer(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/customers")
async def list_customers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_customers(tenant_id)).unwrap()}


@banking_customer_account_router.get("/customers/{customer_id}")
async def get_customer(
    customer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    result = await get_banking_customer_account_service().get_customer(customer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/customers/{customer_id}/submit")
async def submit_customer(
    customer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.customers.write"))],
):
    result = await get_banking_customer_account_service().submit_customer_approval(customer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/customers/{customer_id}/approve")
async def approve_customer(
    customer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.approve"))],
):
    result = await get_banking_customer_account_service().approve_customer(customer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/customers/{customer_id}/reject")
async def reject_customer(
    customer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.approve"))],
):
    result = await get_banking_customer_account_service().reject_customer(customer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.patch("/customers/{customer_id}/kyc-status")
async def update_kyc_status(
    customer_id: str,
    body: UpdateKycStatusRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_customer_account_service().update_customer_kyc_status(
        customer_id, body.status
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.patch("/customers/{customer_id}/risk-rating")
async def update_risk_rating(
    customer_id: str,
    body: UpdateRiskRatingRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.risk.write"))],
):
    result = await get_banking_customer_account_service().update_customer_risk_rating(
        customer_id, body.rating
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/customers/{customer_id}/kyc", status_code=status.HTTP_201_CREATED)
async def create_kyc(
    customer_id: str,
    body: CreateKycRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.write"))],
):
    result = await get_banking_customer_account_service().create_kyc(
        tenant_id=tenant_id, customer_id=customer_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/customers/{customer_id}/kyc")
async def list_kyc(
    customer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_kyc(customer_id)).unwrap()}


@banking_customer_account_router.post("/kyc/{kyc_id}/verify")
async def verify_kyc(
    kyc_id: str,
    body: VerifyKycRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.kyc.verify"))],
):
    result = await get_banking_customer_account_service().verify_kyc(
        kyc_id=kyc_id, verified_by=body.verified_by
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    body: CreateProductRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.products.write"))],
):
    result = await get_banking_customer_account_service().create_product(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/products")
async def list_products(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_products(tenant_id)).unwrap()}


@banking_customer_account_router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def open_account(
    body: OpenAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.accounts.write"))],
):
    result = await get_banking_customer_account_service().open_account(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/accounts")
async def list_accounts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().list_accounts(tenant_id)).unwrap()}


@banking_customer_account_router.get("/accounts/{account_id}")
async def get_account(
    account_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    result = await get_banking_customer_account_service().get_account(account_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/accounts/{account_id}/approve")
async def approve_account(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.approve"))],
):
    result = await get_banking_customer_account_service().approve_account(
        account_id=account_id, actor_id=user.get("sub")
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/accounts/{account_id}/reject")
async def reject_account(
    account_id: str,
    user: Annotated[dict, Depends(require_permissions("banking.approve"))],
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
):
    result = await get_banking_customer_account_service().reject_account(
        account_id=account_id, actor_id=user.get("sub")
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/accounts/{account_id}/status")
async def transition_status(
    account_id: str,
    body: TransitionStatusRequest,
    user: Annotated[dict, Depends(require_permissions("banking.accounts.write"))],
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
):
    result = await get_banking_customer_account_service().transition_account_status(
        account_id=account_id,
        new_status=body.status,
        actor_id=user.get("sub"),
        reason=body.reason,
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/accounts/{account_id}/minimum-balance")
async def check_minimum_balance(
    account_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    result = await get_banking_customer_account_service().evaluate_minimum_balance(account_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.post("/accounts/{account_id}/overdraft-check")
async def check_overdraft(
    account_id: str,
    body: OverdraftCheckRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    result = await get_banking_customer_account_service().evaluate_overdraft(
        account_id, body.amount
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_customer_account_router.get("/accounts/{account_id}/audit")
async def account_audit_trail(
    account_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.read"))],
):
    return {"data": (await get_banking_customer_account_service().get_account_audit_trail(account_id)).unwrap()}
