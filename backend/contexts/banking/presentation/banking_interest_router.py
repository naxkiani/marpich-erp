"""Interest Calculation Engine API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.banking.container import get_banking_interest_calculation_service
from contexts.banking.presentation.banking_interest_schemas import (
    CalculateInterestRequest,
    CreateRateProfileRequest,
    RateChangeRequest,
    SimulateInterestRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_interest_router = APIRouter(
    prefix="/banking/interest",
    tags=["Banking Interest Calculation"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_interest_router.get("/catalog")
async def interest_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    return {"data": (await get_banking_interest_calculation_service().list_catalog()).unwrap()}


@banking_interest_router.get("/policy-keys")
async def interest_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    return {"data": (await get_banking_interest_calculation_service().list_policy_keys()).unwrap()}


@banking_interest_router.get("/dashboard")
async def interest_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    return {"data": (await get_banking_interest_calculation_service().get_dashboard(tenant_id)).unwrap()}


@banking_interest_router.post("/profiles", status_code=status.HTTP_201_CREATED)
async def create_rate_profile(
    body: CreateRateProfileRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.write"))],
):
    result = await get_banking_interest_calculation_service().create_rate_profile(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.get("/profiles")
async def list_rate_profiles(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    return {"data": (await get_banking_interest_calculation_service().list_rate_profiles(tenant_id)).unwrap()}


@banking_interest_router.get("/profiles/{profile_id}")
async def get_rate_profile(
    profile_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    result = await get_banking_interest_calculation_service().get_rate_profile(profile_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.post("/profiles/{profile_id}/rate-changes", status_code=status.HTTP_201_CREATED)
async def record_rate_change(
    profile_id: str,
    body: RateChangeRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.interest.write"))],
):
    result = await get_banking_interest_calculation_service().record_rate_change(
        profile_id=profile_id,
        changed_by=body.changed_by or user.get("sub"),
        **{k: v for k, v in body.model_dump().items() if k != "changed_by"},
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.get("/profiles/{profile_id}/rate-history")
async def list_rate_history(
    profile_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    result = await get_banking_interest_calculation_service().list_rate_history(profile_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.post("/calculate", status_code=status.HTTP_201_CREATED)
async def calculate_interest(
    body: CalculateInterestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.interest.write"))],
):
    result = await get_banking_interest_calculation_service().calculate(
        tenant_id=tenant_id, actor_id=user.get("sub"), **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.post("/simulate", status_code=status.HTTP_201_CREATED)
async def simulate_interest(
    body: SimulateInterestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    result = await get_banking_interest_calculation_service().simulate(
        tenant_id=tenant_id, actor_id=user.get("sub"), **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.get("/audit")
async def list_audit_history(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
    source_ref: Annotated[str | None, Query()] = None,
):
    result = await get_banking_interest_calculation_service().list_audit_history(
        tenant_id, source_ref=source_ref
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_interest_router.get("/audit/{audit_id}")
async def get_audit(
    audit_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.interest.read"))],
):
    result = await get_banking_interest_calculation_service().get_audit(audit_id)
    _raise(result)
    return {"data": result.unwrap()}
