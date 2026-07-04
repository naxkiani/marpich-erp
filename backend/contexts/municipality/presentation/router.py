"""Municipality FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.municipality.container import get_municipality_service
from contexts.municipality.presentation.schemas import (
    ApplyPermitRequest,
    CloseServiceRequestRequest,
    IssueUtilityBillRequest,
    OpenServiceRequestRequest,
    RegisterUtilityAccountRequest,
)

router = APIRouter(prefix="/municipality", tags=["Municipality"])


@router.post("/permits", status_code=status.HTTP_201_CREATED)
async def apply_permit(
    body: ApplyPermitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.permits.write"))],
):
    result = await get_municipality_service().apply_permit(
        tenant_id=tenant_id,
        applicant_name=body.applicant_name,
        permit_type=body.permit_type,
        description=body.description,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/permits/{permit_id}/issue")
async def issue_permit(
    permit_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.permits.issue"))],
):
    result = await get_municipality_service().issue_permit(
        tenant_id=tenant_id, permit_id=permit_id, correlation_id=correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/permits")
async def list_permits(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.permits.read"))],
):
    return {"data": (await get_municipality_service().list_permits(tenant_id)).unwrap()}


@router.post("/service-requests", status_code=status.HTTP_201_CREATED)
async def open_service_request(
    body: OpenServiceRequestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.services.write"))],
):
    result = await get_municipality_service().open_service_request(
        tenant_id=tenant_id,
        citizen_name=body.citizen_name,
        category=body.category,
        description=body.description,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/service-requests/{request_id}/close")
async def close_service_request(
    request_id: str,
    body: CloseServiceRequestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.services.write"))],
):
    result = await get_municipality_service().close_service_request(
        tenant_id=tenant_id,
        request_id=request_id,
        resolution=body.resolution,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/utilities/accounts", status_code=status.HTTP_201_CREATED)
async def register_utility_account(
    body: RegisterUtilityAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.utilities.write"))],
):
    result = await get_municipality_service().register_utility_account(
        tenant_id=tenant_id,
        account_number=body.account_number,
        holder_name=body.holder_name,
        utility_type=body.utility_type,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/utilities/accounts/{account_id}/bill", status_code=status.HTTP_201_CREATED)
async def issue_utility_bill(
    account_id: str,
    body: IssueUtilityBillRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("municipality.utilities.bill"))],
):
    result = await get_municipality_service().issue_utility_bill(
        tenant_id=tenant_id,
        account_id=account_id,
        amount=body.amount,
        period=body.period,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
