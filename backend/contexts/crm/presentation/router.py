"""CRM FastAPI router — CAP-ENT-001 Customer Management."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.crm.container import get_crm_service
from contexts.crm.presentation.schemas import (
    CreateContactRequest,
    CreateOpportunityRequest,
    LoseOpportunityRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/crm", tags=["CRM"])


@router.post("/contacts", status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: CreateContactRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.contacts.write"))],
):
    result = await get_crm_service().create_contact(
        tenant_id=tenant_id,
        email=str(body.email),
        full_name=body.full_name,
        company=body.company,
        phone=body.phone,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/contacts")
async def list_contacts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.contacts.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_crm_service().list_contacts(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/opportunities", status_code=status.HTTP_201_CREATED)
async def create_opportunity(
    body: CreateOpportunityRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.opportunities.write"))],
):
    result = await get_crm_service().create_opportunity(
        tenant_id=tenant_id,
        contact_id=body.contact_id,
        title=body.title,
        amount=body.amount,
        currency=body.currency,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/opportunities")
async def list_opportunities(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.opportunities.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_crm_service().list_opportunities(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/opportunities/{opportunity_id}/win")
async def win_opportunity(
    opportunity_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.opportunities.write"))],
):
    result = await get_crm_service().win_opportunity(
        tenant_id=tenant_id,
        opportunity_id=opportunity_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/opportunities/{opportunity_id}/lose")
async def lose_opportunity(
    opportunity_id: str,
    body: LoseOpportunityRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("crm.opportunities.write"))],
):
    result = await get_crm_service().lose_opportunity(
        tenant_id=tenant_id,
        opportunity_id=opportunity_id,
        correlation_id=correlation_id,
        reason=body.reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
