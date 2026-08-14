"""Human Resources FastAPI router — CAP-ENT-010 Employee Management."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.human_resources.container import get_human_resources_service
from contexts.human_resources.presentation.schemas import (
    HireEmployeeRequest,
    TerminateEmployeeRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/human-resources", tags=["Human Resources"])


@router.post("/employees", status_code=status.HTTP_201_CREATED)
async def hire_employee(
    body: HireEmployeeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("human_resources.employees.write"))],
):
    result = await get_human_resources_service().hire_employee(
        tenant_id=tenant_id,
        email=str(body.email),
        full_name=body.full_name,
        job_title=body.job_title or "",
        department=body.department or "",
        employee_number=body.employee_number or "",
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/employees")
async def list_employees(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("human_resources.employees.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    result = await get_human_resources_service().list_employees(
        tenant_id, limit=limit, offset=offset
    )
    return {"data": result.unwrap()}


@router.get("/employees/{employee_id}")
async def get_employee(
    employee_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("human_resources.employees.read"))],
):
    result = await get_human_resources_service().get_employee(tenant_id, employee_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/employees/{employee_id}/terminate")
async def terminate_employee(
    employee_id: str,
    body: TerminateEmployeeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("human_resources.employees.write"))],
):
    result = await get_human_resources_service().terminate_employee(
        tenant_id=tenant_id,
        employee_id=employee_id,
        correlation_id=correlation_id,
        reason=body.reason or "",
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
