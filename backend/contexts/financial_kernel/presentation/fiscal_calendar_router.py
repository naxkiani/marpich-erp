"""Enterprise Fiscal Calendar API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.financial_kernel.container import get_financial_kernel_service
from contexts.financial_kernel.presentation.schemas import (
    ApproveCloseActionRequest,
    CreateCalendarFiscalYearRequest,
    CreateFiscalCalendarRequest,
    PeriodCloseActionRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

fiscal_calendar_router = APIRouter(
    prefix="/financial-kernel/fiscal-calendar", tags=["Fiscal Calendar"]
)


@fiscal_calendar_router.post("/calendars", status_code=status.HTTP_201_CREATED)
async def create_fiscal_calendar(
    body: CreateFiscalCalendarRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.write"))],
):
    result = await get_financial_kernel_service().create_fiscal_calendar(
        tenant_id=tenant_id,
        name=body.name,
        organization_id=body.organization_id,
        description=body.description,
        fiscal_year_start_month=body.fiscal_year_start_month,
        is_default=body.is_default,
        actor_id=_user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.get("/calendars")
async def list_fiscal_calendars(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.read"))],
):
    result = await get_financial_kernel_service().list_fiscal_calendars(tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.get("/calendars/{calendar_id}")
async def get_fiscal_calendar(
    calendar_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.read"))],
):
    result = await get_financial_kernel_service().get_fiscal_calendar(calendar_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.post("/calendars/{calendar_id}/fiscal-years", status_code=status.HTTP_201_CREATED)
async def create_calendar_fiscal_year(
    calendar_id: str,
    body: CreateCalendarFiscalYearRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.write"))],
):
    result = await get_financial_kernel_service().create_calendar_fiscal_year(
        tenant_id=tenant_id,
        calendar_id=calendar_id,
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
        organization_id=body.organization_id,
        actor_id=_user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.post("/fiscal-years/{fiscal_year_id}/generate-periods", status_code=status.HTTP_201_CREATED)
async def generate_fiscal_periods(
    fiscal_year_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.write"))],
):
    result = await get_financial_kernel_service().generate_calendar_periods(
        tenant_id=tenant_id,
        fiscal_year_id=fiscal_year_id,
        actor_id=_user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.post("/fiscal-years/{fiscal_year_id}/adjustment-period", status_code=status.HTTP_201_CREATED)
async def create_adjustment_period(
    fiscal_year_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.write"))],
):
    result = await get_financial_kernel_service().create_adjustment_period(
        tenant_id=tenant_id,
        fiscal_year_id=fiscal_year_id,
        actor_id=_user.get("sub", "system"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.post("/periods/{period_id}/close-request", status_code=status.HTTP_201_CREATED)
async def request_period_close(
    period_id: str,
    body: PeriodCloseActionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.close"))],
):
    result = await get_financial_kernel_service().request_period_close_action(
        tenant_id=tenant_id,
        period_id=period_id,
        action_type=body.action_type,
        requester_id=_user.get("sub", "system"),
        reason=body.reason,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@fiscal_calendar_router.post("/close-requests/{request_id}/approve")
async def approve_period_close(
    request_id: str,
    body: ApproveCloseActionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.approve"))],
):
    result = await get_financial_kernel_service().approve_period_close_action(
        tenant_id=tenant_id,
        request_id=request_id,
        approver_id=body.approver_id or _user.get("sub", "approver"),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@fiscal_calendar_router.post("/periods/{period_id}/lock")
async def lock_fiscal_period(
    period_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.lock"))],
):
    result = await get_financial_kernel_service().lock_fiscal_period(
        period_id, actor_id=_user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.post("/periods/{period_id}/unlock")
async def unlock_fiscal_period(
    period_id: str,
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.lock"))],
):
    result = await get_financial_kernel_service().unlock_fiscal_period(
        period_id, actor_id=_user.get("sub", "system")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.get("/audit-log")
async def list_calendar_audit_log(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.read"))],
):
    return {"data": (await get_financial_kernel_service().list_fiscal_calendar_audit_log(tenant_id)).unwrap()}


@fiscal_calendar_router.get("/periods/{period_id}/closing-assistant")
async def get_closing_assistant(
    period_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.read"))],
):
    result = await get_financial_kernel_service().get_closing_assistant(tenant_id, period_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@fiscal_calendar_router.get("/periods/{period_id}/ai-closing-checklist")
async def get_ai_closing_checklist(
    period_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("financial_kernel.fiscal_calendar.read"))],
):
    result = await get_financial_kernel_service().get_ai_closing_checklist(tenant_id, period_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
