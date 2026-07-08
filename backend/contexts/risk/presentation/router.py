"""Enterprise Risk Platform API."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.identity.presentation.dependencies import get_correlation_id, get_tenant_id, require_permissions
from contexts.risk.container import get_risk_service
from contexts.risk.presentation.schemas import PredictRiskRequest, RegisterRiskRequest

risk_router = APIRouter(prefix="/risk", tags=["Enterprise Risk Platform"])


@risk_router.get("/catalog")
async def catalog(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().list_catalog()).unwrap()}


@risk_router.get("/dependency-map")
async def dependency_map(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().get_dependency_map()).unwrap()}


@risk_router.post("/seed")
async def seed(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.write"))],
):
    return {"data": (await get_risk_service().seed(tenant_id)).unwrap()}


@risk_router.get("/dashboard")
async def dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().get_dashboard(tenant_id)).unwrap()}


@risk_router.get("/register")
async def list_register(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().list_register(tenant_id)).unwrap()}


@risk_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_risk(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: RegisterRiskRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("risk.write"))],
):
    result = await get_risk_service().register_risk(
        tenant_id,
        title=body.title,
        category=body.category,
        likelihood=body.likelihood,
        impact=body.impact,
        owner_id=body.owner_id or user.get("sub", ""),
        source_module=body.source_module,
        mitigation_plan=body.mitigation_plan,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@risk_router.post("/register/{risk_ref}/escalate")
async def escalate_risk(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    risk_ref: str,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.write"))],
):
    result = await get_risk_service().escalate_risk(tenant_id, risk_ref, correlation_id=correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@risk_router.get("/matrix")
async def get_matrix(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().get_matrix(tenant_id)).unwrap()}


@risk_router.get("/heatmap")
async def get_heatmap(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().get_heatmap(tenant_id)).unwrap()}


@risk_router.post("/predict")
async def predict(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    body: PredictRiskRequest,
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {
        "data": (
            await get_risk_service().predict(
                tenant_id, category=body.category, correlation_id=correlation_id
            )
        ).unwrap(),
        "meta": {"correlation_id": correlation_id},
    }


@risk_router.get("/predictions")
async def list_predictions(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("risk.read"))],
):
    return {"data": (await get_risk_service().list_predictions(tenant_id)).unwrap()}
