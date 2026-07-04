"""Enterprise Cost Centers API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.financial_kernel.container import get_cost_center_service
from contexts.financial_kernel.presentation.cost_center_schemas import (
    CreateAllocationRequest,
    CreateCostCenterRequest,
    CreateProfitCenterRequest,
    SplitAllocationRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

cost_centers_router = APIRouter(
    prefix="/financial-kernel/cost-centers",
    tags=["Cost Centers"],
)


@cost_centers_router.post("", status_code=status.HTTP_201_CREATED)
async def create_cost_center(
    body: CreateCostCenterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.write"))],
):
    result = await get_cost_center_service().create_cost_center(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        center_type=body.center_type,
        parent_id=body.parent_id,
        profit_center_id=body.profit_center_id,
        manager_id=body.manager_id,
        metadata=body.metadata,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@cost_centers_router.get("")
async def list_cost_centers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.read"))],
    center_type: str | None = Query(default=None),
):
    result = await get_cost_center_service().list_cost_centers(tenant_id, center_type=center_type)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@cost_centers_router.get("/profitability")
async def profitability_analysis(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.analyze"))],
    cost_center_code: str | None = Query(default=None),
    profit_center_code: str | None = Query(default=None),
):
    result = await get_cost_center_service().profitability_analysis(
        tenant_id,
        cost_center_code=cost_center_code,
        profit_center_code=profit_center_code,
    )
    return {"data": result.unwrap()}


@cost_centers_router.post("/profit-centers", status_code=status.HTTP_201_CREATED)
async def create_profit_center(
    body: CreateProfitCenterRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.write"))],
):
    result = await get_cost_center_service().create_profit_center(
        tenant_id=tenant_id,
        code=body.code,
        name=body.name,
        business_unit_id=body.business_unit_id,
        metadata=body.metadata,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@cost_centers_router.get("/profit-centers/list")
async def list_profit_centers(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.read"))],
):
    return {"data": (await get_cost_center_service().list_profit_centers(tenant_id)).unwrap()}


@cost_centers_router.post("/allocations", status_code=status.HTTP_201_CREATED)
async def create_allocation(
    body: CreateAllocationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.allocate"))],
):
    key = body.idempotency_key or f"{body.source_context}:{body.source_document_id}:{body.cost_center_code}"
    result = await get_cost_center_service().create_allocation(
        tenant_id=tenant_id,
        allocation_type=body.allocation_type,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        idempotency_key=key,
        cost_center_code=body.cost_center_code,
        account_code=body.account_code,
        amount=body.amount,
        currency=body.currency,
        profit_center_code=body.profit_center_code,
        period_id=body.period_id,
        description=body.description,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@cost_centers_router.post("/allocations/split", status_code=status.HTTP_201_CREATED)
async def split_allocation(
    body: SplitAllocationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.allocate"))],
):
    result = await get_cost_center_service().split_allocation(
        tenant_id=tenant_id,
        allocation_type=body.allocation_type,
        source_context=body.source_context,
        source_document_id=body.source_document_id,
        account_code=body.account_code,
        total_amount=body.total_amount,
        cost_center_codes=body.cost_center_codes,
        weights=body.weights,
        currency=body.currency,
        period_id=body.period_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@cost_centers_router.get("/allocations/list")
async def list_allocations(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.read"))],
    allocation_type: str | None = Query(default=None),
    cost_center_code: str | None = Query(default=None),
):
    result = await get_cost_center_service().list_allocations(
        tenant_id,
        allocation_type=allocation_type,
        cost_center_code=cost_center_code,
    )
    return {"data": result.unwrap()}


@cost_centers_router.get("/{center_id}")
async def get_cost_center(
    center_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.cost_centers.read"))],
):
    result = await get_cost_center_service().get_cost_center(tenant_id, center_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
