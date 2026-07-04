"""Enterprise Chart of Accounts API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    ApplyCoaTemplateRequest,
    CreateCoaAccountRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

coa_router = APIRouter(prefix="/financial-kernel/coa", tags=["Chart of Accounts"])


@coa_router.get("/tree")
async def get_account_tree(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    return {"data": (await get_financial_kernel_service().get_account_tree(tenant_id)).unwrap()}


@coa_router.get("/templates")
async def list_coa_templates(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    return {"data": (await get_financial_kernel_service().list_coa_templates()).unwrap()}


@coa_router.post("/templates/apply", status_code=status.HTTP_201_CREATED)
async def apply_coa_template(
    body: ApplyCoaTemplateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().apply_coa_template(
        tenant_id=tenant_id,
        template_key=body.template_key,
        template_type=body.template_type,
        code_overrides=body.code_overrides,
        code_prefix=body.code_prefix,
        country_code=body.country_code,
        merge=body.merge,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@coa_router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_coa_account(
    body: CreateCoaAccountRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().create_account(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        account_type=body.account_type,
        account_category=body.account_category,
        account_key=body.account_key,
        parent_account_id=body.parent_account_id,
        account_group=body.account_group,
        is_posting=body.is_posting,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@coa_router.get("/accounts/{account_id}")
async def get_coa_account(
    account_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_account(account_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@coa_router.get("/accounts/{account_id}/children")
async def list_coa_account_children(
    account_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    return {
        "data": (
            await get_financial_kernel_service().list_account_children(tenant_id, account_id)
        ).unwrap()
    }


@coa_router.get("/resolve/{account_key}")
async def resolve_account_key(
    account_key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().resolve_account_code(tenant_id, account_key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": {"account_key": account_key, "code": result.unwrap()}}
