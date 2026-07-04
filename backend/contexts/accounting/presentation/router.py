"""Accounting FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.accounting.container import get_accounting_service
from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions

router = APIRouter(prefix="/accounting", tags=["Accounting"])


@router.get("/billings")
async def list_billings(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().list_billings(tenant_id)
    return {"data": result.unwrap()}


@router.get("/billings/{billing_id}")
async def get_billing(
    billing_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().get_billing(tenant_id, billing_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/billings/by-encounter/{encounter_id}")
async def get_billing_by_encounter(
    encounter_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("accounting.billing.read"))],
):
    result = await get_accounting_service().find_by_encounter(tenant_id, encounter_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
