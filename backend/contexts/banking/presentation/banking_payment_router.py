"""Banking Payment Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_payment_platform_service
from contexts.banking.presentation.banking_payment_schemas import (
    ApproveTransferRequest,
    BeneficiaryRequest,
    BulkTransferRequest,
    CreateTransferRequest,
    ExecuteTransferRequest,
    ScheduleTransferRequest,
    StandingOrderRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_payment_router = APIRouter(
    prefix="/banking/payments",
    tags=["Banking Payment Platform"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_payment_router.get("/catalog")
async def payment_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    return {"data": (await get_banking_payment_platform_service().list_catalog()).unwrap()}


@banking_payment_router.get("/policy-keys")
async def payment_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    return {"data": (await get_banking_payment_platform_service().list_policy_keys()).unwrap()}


@banking_payment_router.get("/dashboard")
async def payment_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    return {"data": (await get_banking_payment_platform_service().get_dashboard(tenant_id)).unwrap()}


@banking_payment_router.post("/beneficiaries", status_code=status.HTTP_201_CREATED)
async def add_beneficiary(
    body: BeneficiaryRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().add_beneficiary(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers", status_code=status.HTTP_201_CREATED)
async def create_transfer(
    body: CreateTransferRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().create_transfer(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.get("/transfers")
async def list_transfers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    return {"data": (await get_banking_payment_platform_service().list_transfers(tenant_id)).unwrap()}


@banking_payment_router.get("/transfers/{transfer_id}")
async def get_transfer(
    transfer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    result = await get_banking_payment_platform_service().get_transfer(transfer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers/{transfer_id}/submit")
async def submit_transfer(
    transfer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().submit_transfer(transfer_id=transfer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers/{transfer_id}/approve")
async def approve_transfer(
    transfer_id: str,
    body: ApproveTransferRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.execute"))],
):
    result = await get_banking_payment_platform_service().approve_transfer(
        transfer_id=transfer_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers/{transfer_id}/schedule")
async def schedule_transfer(
    transfer_id: str,
    body: ScheduleTransferRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().schedule_transfer(
        transfer_id=transfer_id, scheduled_at=body.scheduled_at
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers/{transfer_id}/execute")
async def execute_transfer(
    transfer_id: str,
    body: ExecuteTransferRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.execute"))],
):
    result = await get_banking_payment_platform_service().execute_transfer(
        transfer_id=transfer_id, approver_id=body.approver_id
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/transfers/{transfer_id}/fraud-check")
async def fraud_check(
    transfer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    result = await get_banking_payment_platform_service().run_fraud_check(transfer_id=transfer_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def create_bulk_transfer(
    body: BulkTransferRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().create_bulk_transfer(
        tenant_id=tenant_id,
        source_account_id=body.source_account_id,
        transfer_type=body.transfer_type,
        items=[i.model_dump() for i in body.items],
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.post("/standing-orders", status_code=status.HTTP_201_CREATED)
async def create_standing_order(
    body: StandingOrderRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.write"))],
):
    result = await get_banking_payment_platform_service().create_standing_order(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_payment_router.get("/transfers/{transfer_id}/audit")
async def get_audit_trail(
    transfer_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.transfers.read"))],
):
    result = await get_banking_payment_platform_service().get_audit_trail(transfer_id)
    _raise(result)
    return {"data": result.unwrap()}
