"""Enterprise Account Hierarchy API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    ApplyTreeTemplateRequest,
    BulkImportAccountsRequest,
    CreateAccountTreeRequest,
    CreateTreeVersionRequest,
    MoveAccountInTreeRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

account_hierarchy_router = APIRouter(
    prefix="/financial-kernel/account-hierarchy", tags=["Account Hierarchy"]
)


@account_hierarchy_router.post("/trees", status_code=status.HTTP_201_CREATED)
async def create_account_tree(
    body: CreateAccountTreeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().create_account_tree(
        tenant_id=tenant_id,
        name=body.name,
        description=body.description,
        tree_type=body.tree_type,
        template_key=body.template_key,
        template_type=body.template_type,
        country_code=body.country_code,
        is_default=body.is_default,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees")
async def list_account_trees(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_account_trees(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}")
async def get_account_tree_meta(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_account_tree_meta(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/structure")
async def get_hierarchy_structure(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_hierarchy_structure(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.post("/trees/{tree_id}/move")
async def move_account_in_tree(
    tree_id: str,
    body: MoveAccountInTreeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().move_account_in_tree(
        tenant_id=tenant_id,
        tree_id=tree_id,
        account_id=body.account_id,
        new_parent_id=body.new_parent_id,
        position=body.position,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.post("/trees/{tree_id}/versions", status_code=status.HTTP_201_CREATED)
async def create_tree_version(
    tree_id: str,
    body: CreateTreeVersionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().create_tree_version_snapshot(
        tenant_id=tenant_id,
        tree_id=tree_id,
        actor_id=user.get("sub", "system"),
        change_summary=body.change_summary,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/versions")
async def list_tree_versions(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_tree_versions(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/versions/{version_id}")
async def get_tree_version(
    version_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().get_tree_version(tenant_id, version_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/search")
async def search_hierarchy_accounts(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
    q: str = Query("", alias="q"),
    account_category: str | None = Query(None),
    account_type: str | None = Query(None),
    is_posting: bool | None = Query(None),
    level: int | None = Query(None),
    parent_account_id: str | None = Query(None),
):
    result = await get_financial_kernel_service().search_hierarchy_accounts(
        tenant_id,
        tree_id,
        query=q,
        account_category=account_category,
        account_type=account_type,
        is_posting=is_posting,
        level=level,
        parent_account_id=parent_account_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/validate")
async def validate_account_hierarchy(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().validate_account_hierarchy(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.post("/trees/{tree_id}/import", status_code=status.HTTP_201_CREATED)
async def bulk_import_accounts(
    tree_id: str,
    body: BulkImportAccountsRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().bulk_import_hierarchy_accounts(
        tenant_id=tenant_id,
        tree_id=tree_id,
        rows=body.rows,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/export")
async def bulk_export_accounts(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().bulk_export_hierarchy_accounts(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.post("/trees/{tree_id}/templates/apply", status_code=status.HTTP_201_CREATED)
async def apply_template_to_tree(
    tree_id: str,
    body: ApplyTreeTemplateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.write"))],
):
    result = await get_financial_kernel_service().apply_template_to_tree(
        tenant_id=tenant_id,
        tree_id=tree_id,
        template_key=body.template_key,
        template_type=body.template_type,
        code_overrides=body.code_overrides,
        code_prefix=body.code_prefix,
        country_code=body.country_code,
        merge=body.merge,
        actor_id=user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/ai-optimize")
async def ai_optimize_tree(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().ai_optimize_account_tree(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/trees/{tree_id}/visual")
async def get_visual_account_tree(
    tree_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().generate_visual_account_tree(tenant_id, tree_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@account_hierarchy_router.get("/templates")
async def list_hierarchy_templates(
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.coa.read"))],
):
    result = await get_financial_kernel_service().list_coa_templates()
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
