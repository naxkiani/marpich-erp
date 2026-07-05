"""Enterprise Bank master data API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.treasury.container import get_bank_account_service
from contexts.treasury.presentation.bank_account_schemas import CreateBankRequest, CreateBranchRequest

banks_router = APIRouter(prefix="/treasury/banks", tags=["Bank Management"])


@banks_router.post("", status_code=status.HTTP_201_CREATED)
async def create_bank(
    body: CreateBankRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().create_bank(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        country=body.country,
        organization_id=body.organization_id,
        swift_bic=body.swift_bic,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@banks_router.get("")
async def list_banks(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
    organization_id: str | None = Query(None),
):
    return {"data": (await get_bank_account_service().list_banks(tenant_id, organization_id)).unwrap()}


@banks_router.get("/{bank_id}")
async def get_bank(
    bank_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
):
    result = await get_bank_account_service().get_bank(tenant_id, bank_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@banks_router.post("/{bank_id}/branches", status_code=status.HTTP_201_CREATED)
async def create_branch(
    bank_id: str,
    body: CreateBranchRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.write"))],
):
    result = await get_bank_account_service().create_branch(
        tenant_id=tenant_id,
        bank_id=bank_id,
        code=body.code,
        name=body.name,
        organization_id=body.organization_id,
        address=body.address,
        routing_number=body.routing_number,
        swift_bic=body.swift_bic,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@banks_router.get("/{bank_id}/branches")
async def list_branches(
    bank_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.bank_accounts.read"))],
    organization_id: str | None = Query(None),
):
    result = await get_bank_account_service().list_branches(tenant_id, bank_id, organization_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
