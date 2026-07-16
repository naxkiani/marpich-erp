"""Branch Banking Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.banking.container import get_banking_branch_platform_service
from contexts.banking.presentation.banking_branch_schemas import (
    AddExtensionRequest,
    CashLimitRequest,
    CloseBranchRequest,
    CreateOfficeRequest,
    EmployeeAssignmentRequest,
    OpenBranchRequest,
    RecordKPIRequest,
    VaultMovementRequest,
)
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

banking_branch_router = APIRouter(
    prefix="/banking/branches",
    tags=["Branch Banking Platform"],
)


def _raise(result) -> None:
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)


@banking_branch_router.get("/catalog")
async def branch_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_catalog()).unwrap()}


@banking_branch_router.get("/policy-keys")
async def branch_policy_keys(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_policy_keys()).unwrap()}


@banking_branch_router.get("/dashboard")
async def branch_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().get_dashboard(tenant_id)).unwrap()}


@banking_branch_router.get("/analytics")
async def branch_analytics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().get_analytics(tenant_id)).unwrap()}


@banking_branch_router.post("/offices", status_code=status.HTTP_201_CREATED)
async def create_office(
    body: CreateOfficeRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.write"))],
):
    result = await get_banking_branch_platform_service().create_office(
        tenant_id=tenant_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.get("/offices")
async def list_offices(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_offices(tenant_id)).unwrap()}


@banking_branch_router.get("/offices/{office_id}")
async def get_office(
    office_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    result = await get_banking_branch_platform_service().get_office(office_id=office_id)
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.post("/offices/{office_id}/extensions", status_code=status.HTTP_201_CREATED)
async def add_extension(
    office_id: str,
    body: AddExtensionRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.write"))],
):
    result = await get_banking_branch_platform_service().add_extension(
        office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.post("/offices/{office_id}/open")
async def open_branch(
    office_id: str,
    body: OpenBranchRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.operate"))],
):
    result = await get_banking_branch_platform_service().open_branch(
        office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.post("/offices/{office_id}/close")
async def close_branch(
    office_id: str,
    body: CloseBranchRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.operate"))],
):
    result = await get_banking_branch_platform_service().close_branch(
        office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.post("/offices/{office_id}/vault/movements")
async def vault_movement(
    office_id: str,
    body: VaultMovementRequest,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.operate"))],
):
    result = await get_banking_branch_platform_service().vault_movement(
        office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.post("/offices/{office_id}/cash-limits", status_code=status.HTTP_201_CREATED)
async def set_cash_limit(
    office_id: str,
    body: CashLimitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.write"))],
):
    result = await get_banking_branch_platform_service().set_cash_limit(
        tenant_id=tenant_id, office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.get("/offices/{office_id}/cash-limits")
async def list_cash_limits(
    office_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_cash_limits(office_id=office_id)).unwrap()}


@banking_branch_router.post("/offices/{office_id}/assignments", status_code=status.HTTP_201_CREATED)
async def assign_employee(
    office_id: str,
    body: EmployeeAssignmentRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.write"))],
):
    result = await get_banking_branch_platform_service().assign_employee(
        tenant_id=tenant_id, office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.get("/offices/{office_id}/assignments")
async def list_assignments(
    office_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_assignments(office_id=office_id)).unwrap()}


@banking_branch_router.post("/offices/{office_id}/kpis", status_code=status.HTTP_201_CREATED)
async def record_kpi(
    office_id: str,
    body: RecordKPIRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.write"))],
):
    result = await get_banking_branch_platform_service().record_kpi(
        tenant_id=tenant_id, office_id=office_id, **body.model_dump()
    )
    _raise(result)
    return {"data": result.unwrap()}


@banking_branch_router.get("/offices/{office_id}/kpis")
async def list_kpis(
    office_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    return {"data": (await get_banking_branch_platform_service().list_kpis(office_id=office_id)).unwrap()}


@banking_branch_router.get("/offices/{office_id}/audit")
async def office_audit(
    office_id: str,
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("banking.branch.read"))],
):
    result = await get_banking_branch_platform_service().get_office_audit(office_id=office_id)
    _raise(result)
    return {"data": result.unwrap()}
