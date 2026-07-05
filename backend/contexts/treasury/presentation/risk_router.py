"""Enterprise Treasury Risk Platform API routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.treasury.container import get_risk_service
from contexts.treasury.presentation.risk_schemas import (
    CreateRiskLimitRequest,
    RunStressTestRequest,
    UpdateRiskLimitRequest,
)

risk_router = APIRouter(
    prefix="/treasury/risk",
    tags=["Enterprise Treasury Risk Platform"],
)


@risk_router.get("/catalog")
async def risk_catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().list_catalog()).unwrap()}


@risk_router.get("/scenarios")
async def stress_scenarios(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().list_scenarios()).unwrap()}


@risk_router.get("/dashboard")
async def risk_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().get_dashboard(tenant_id)).unwrap()}


@risk_router.get("/exposures")
async def exposure_monitoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().get_exposures(tenant_id)).unwrap()}


@risk_router.get("/limits")
async def list_risk_limits(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().list_limits(tenant_id)).unwrap()}


@risk_router.post("/limits", status_code=status.HTTP_201_CREATED)
async def create_risk_limit(
    body: CreateRiskLimitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.write"))],
):
    result = await get_risk_service().create_limit(
        tenant_id=tenant_id,
        risk_type=body.risk_type,
        name=body.name,
        threshold_value=body.threshold_value,
        threshold_unit=body.threshold_unit,
        currency=body.currency,
        description=body.description,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@risk_router.patch("/limits/{limit_id}")
async def update_risk_limit(
    limit_id: str,
    body: UpdateRiskLimitRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.write"))],
):
    result = await get_risk_service().update_limit(
        limit_id,
        tenant_id=tenant_id,
        threshold_value=body.threshold_value,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@risk_router.get("/alerts")
async def list_risk_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
    alert_status: str | None = Query(default=None, alias="status"),
):
    return {"data": (await get_risk_service().list_alerts(tenant_id, alert_status)).unwrap()}


@risk_router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(require_permissions("treasury.risk.write"))],
):
    result = await get_risk_service().acknowledge_alert(
        alert_id,
        tenant_id=tenant_id,
        actor_id=str(user.get("id", user.get("sub"))),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@risk_router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.write"))],
):
    result = await get_risk_service().resolve_alert(alert_id, tenant_id=tenant_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@risk_router.post("/stress-tests", status_code=status.HTTP_201_CREATED)
async def run_stress_test(
    body: RunStressTestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.write"))],
):
    result = await get_risk_service().run_stress_test_scenario(tenant_id, body.scenario)
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@risk_router.get("/stress-tests")
async def list_stress_tests(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.read"))],
):
    return {"data": (await get_risk_service().list_stress_tests(tenant_id)).unwrap()}


@risk_router.post("/ai/scoring")
async def ai_risk_scoring(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("treasury.risk.analyze"))],
):
    result = await get_risk_service().run_ai_risk_scoring(
        tenant_id,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
