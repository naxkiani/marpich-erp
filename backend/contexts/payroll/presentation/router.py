"""Payroll FastAPI router — CAP-ENT-015."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.payroll.container import get_payroll_service
from contexts.payroll.presentation.schemas import CreatePayrollRunRequest

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.get("/employees")
async def list_payroll_employees(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("payroll.employees.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_payroll_service().list_employees(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.get("/runs")
async def list_payroll_runs(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("payroll.runs.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_payroll_service().list_runs(tenant_id, limit=limit, offset=offset)
    return {"data": result.unwrap()}


@router.post("/runs", status_code=status.HTTP_201_CREATED)
async def create_payroll_run(
    body: CreatePayrollRunRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("payroll.runs.write"))],
):
    # Ensure subscription is registered even if only payroll routes are hit first
    get_payroll_service()
    result = await get_payroll_service().create_and_complete_run(
        tenant_id=tenant_id,
        period_label=body.period_label,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
