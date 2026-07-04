"""Feature flag FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.feature_flags.container import get_feature_flag_service
from contexts.feature_flags.presentation.schemas import (
    AbTestRequest,
    CreateFlagRequest,
    EmergencyDisableRequest,
    EvaluateRequest,
    RollbackRequest,
    RolloutRequest,
    UpdateFlagRequest,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])


@router.get("")
async def list_flags(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.read"))],
):
    return {"data": (await get_feature_flag_service().list_flags(tenant_id)).unwrap()}


@router.get("/dashboard")
async def get_dashboard(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.dashboard.read"))],
):
    return {"data": (await get_feature_flag_service().get_dashboard(tenant_id)).unwrap()}


@router.get("/{key}")
async def get_flag(
    key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.read"))],
):
    result = await get_feature_flag_service().get_flag(tenant_id, key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/{key}/history")
async def get_history(
    key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.read"))],
):
    result = await get_feature_flag_service().get_history(tenant_id, key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_flag(
    body: CreateFlagRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.write"))],
):
    result = await get_feature_flag_service().create_flag(
        tenant_id=tenant_id,
        key=body.key,
        name=body.name,
        default_enabled=body.default_enabled,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.patch("/{key}")
async def update_flag(
    key: str,
    body: UpdateFlagRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.write"))],
):
    result = await get_feature_flag_service().update_flag(
        tenant_id=tenant_id,
        key=key,
        default_enabled=body.default_enabled,
        tenant_rules=body.tenant_rules,
        organization_rules=body.organization_rules,
        user_rules=body.user_rules,
        environment_rules=body.environment_rules,
        country_rules=body.country_rules,
        industry_rules=body.industry_rules,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/evaluate")
async def evaluate_flags(
    body: EvaluateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.evaluate"))],
):
    return {"data": (await get_feature_flag_service().evaluate(tenant_id, body.flags, body.context)).unwrap()}


@router.post("/{key}/rollout")
async def update_rollout(
    key: str,
    body: RolloutRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.write"))],
):
    result = await get_feature_flag_service().update_rollout(
        tenant_id, key, body.percentage, body.stage, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{key}/ab-test")
async def configure_ab_test(
    key: str,
    body: AbTestRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.write"))],
):
    result = await get_feature_flag_service().configure_ab_test(
        tenant_id, key, body.variants, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{key}/emergency-disable")
async def emergency_disable(
    key: str,
    body: EmergencyDisableRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.admin"))],
):
    result = await get_feature_flag_service().emergency_disable(
        tenant_id, key, body.reason, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{key}/emergency-enable")
async def emergency_enable(
    key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.admin"))],
):
    result = await get_feature_flag_service().emergency_enable(tenant_id, key, correlation_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{key}/rollback")
async def rollback_flag(
    key: str,
    body: RollbackRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("feature_flags.admin"))],
):
    result = await get_feature_flag_service().rollback(
        tenant_id, key, body.target_version, correlation_id
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
