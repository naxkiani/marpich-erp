"""Identity risk platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity_risk.container import get_identity_risk_service
from contexts.identity_risk.presentation.schemas import EvaluateRiskRequest
from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions

identity_risk_router = APIRouter(
    prefix="/identity-risk",
    tags=["Identity Risk"],
)


@identity_risk_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_risk.read"))],
):
    return {"data": (await get_identity_risk_service().list_catalog()).unwrap()}


@identity_risk_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_risk.write"))],
):
    return {"data": (await get_identity_risk_service().seed(tenant_id)).unwrap()}


@identity_risk_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_risk.read"))],
):
    return {"data": (await get_identity_risk_service().get_dashboard(tenant_id)).unwrap()}


@identity_risk_router.get("/scores")
async def list_scores(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_risk.read"))],
):
    return {"data": (await get_identity_risk_service().list_scores(tenant_id)).unwrap()}


@identity_risk_router.get("/alerts")
async def list_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("identity_risk.anomalies.read"))],
):
    return {"data": (await get_identity_risk_service().list_alerts(tenant_id)).unwrap()}


@identity_risk_router.post("/evaluate")
async def evaluate_risk(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: EvaluateRiskRequest,
    _user: Annotated[dict, Depends(require_permissions("identity_risk.score"))],
):
    result = await get_identity_risk_service().evaluate_manual(
        tenant_id,
        event_type=body.event_type,
        payload=body.payload,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}
