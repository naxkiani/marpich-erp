"""Policy FastAPI router."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.policy.container import get_policy_service
from contexts.policy.presentation.schemas import (
    CreatePolicyRequest,
    CreateVersionRequest,
    EvaluateRequest,
    RollbackRequest,
    RunTestsRequest,
    SimulateRequest,
    UpdateDraftVersionRequest,
)

router = APIRouter(prefix="/policies", tags=["Policy Engine"])


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@router.get("/domains")
async def list_domains(
    _tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.read"))],
):
    result = await get_policy_service().list_domains()
    return {"data": result.unwrap()}


@router.get("")
async def list_policies(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.read"))],
    domain: Annotated[str | None, Query()] = None,
):
    result = await get_policy_service().list_policies(tenant_id, domain=domain)
    return {"data": result.unwrap()}


@router.get("/{policy_id}")
async def get_policy(
    policy_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.read"))],
):
    result = await get_policy_service().get_policy(tenant_id, policy_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/{policy_id}/versions")
async def list_versions(
    policy_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.read"))],
):
    result = await get_policy_service().list_versions(tenant_id, policy_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/{policy_id}/history")
async def get_history(
    policy_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.read"))],
):
    result = await get_policy_service().get_history(tenant_id, policy_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_policy(
    body: CreatePolicyRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("policies.write"))],
):
    from datetime import UTC

    effective_from = _parse_dt(body.effective_from) or datetime.now(UTC)
    result = await get_policy_service().create_policy(
        tenant_id=tenant_id,
        domain=body.domain,
        key=body.key,
        name=body.name,
        description=body.description,
        effective_from=effective_from,
        priority=body.priority,
        conditions=body.conditions,
        rules=body.rules,
        exceptions=body.exceptions,
        expires_at=_parse_dt(body.expires_at),
        approval_required=body.approval_required,
        actor_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{policy_id}/versions", status_code=status.HTTP_201_CREATED)
async def create_version(
    policy_id: str,
    body: CreateVersionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("policies.write"))],
):
    from datetime import UTC

    effective_from = _parse_dt(body.effective_from) or datetime.now(UTC)
    result = await get_policy_service().create_version(
        tenant_id=tenant_id,
        policy_id=policy_id,
        effective_from=effective_from,
        priority=body.priority,
        conditions=body.conditions,
        rules=body.rules,
        exceptions=body.exceptions,
        expires_at=_parse_dt(body.expires_at),
        approval_required=body.approval_required,
        actor_id=user.get("sub"),
        change_reason=body.change_reason,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.patch("/{policy_id}/versions/{version}")
async def update_draft_version(
    policy_id: str,
    version: int,
    body: UpdateDraftVersionRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.write"))],
):
    result = await get_policy_service().update_draft_version(
        tenant_id=tenant_id,
        policy_id=policy_id,
        version=version,
        effective_from=_parse_dt(body.effective_from),
        expires_at=_parse_dt(body.expires_at),
        priority=body.priority,
        conditions=body.conditions,
        rules=body.rules,
        exceptions=body.exceptions,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.post("/evaluate")
async def evaluate_policy(
    body: EvaluateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.evaluate"))],
):
    result = await get_policy_service().evaluate(
        tenant_id=tenant_id,
        domain=body.domain,
        policy_key=body.policy_key,
        facts=body.facts,
        as_of=_parse_dt(body.as_of),
    )
    return {"data": result.unwrap()}


@router.post("/simulate")
async def simulate_policy(
    body: SimulateRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.simulate"))],
):
    result = await get_policy_service().simulate(
        tenant_id=tenant_id,
        domain=body.domain,
        policy_key=body.policy_key,
        facts=body.facts,
        candidate_versions=body.candidate_versions,
        as_of=_parse_dt(body.as_of),
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{policy_id}/test")
async def run_policy_tests(
    policy_id: str,
    body: RunTestsRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("policies.test"))],
    version: Annotated[int, Query(ge=1)] = 1,
):
    test_cases = [tc.model_dump() for tc in body.test_cases]
    result = await get_policy_service().run_tests(tenant_id, policy_id, version, test_cases)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/{policy_id}/versions/{version}/submit-approval")
async def submit_approval(
    policy_id: str,
    version: int,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("policies.write"))],
):
    result = await get_policy_service().submit_approval(
        tenant_id=tenant_id,
        policy_id=policy_id,
        version=version,
        correlation_id=correlation_id,
        actor_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{policy_id}/versions/{version}/activate")
async def activate_version(
    policy_id: str,
    version: int,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("policies.admin"))],
):
    result = await get_policy_service().activate_version(
        tenant_id, policy_id, version, actor_id=user.get("sub")
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/{policy_id}/rollback")
async def rollback_policy(
    policy_id: str,
    body: RollbackRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("policies.admin"))],
):
    result = await get_policy_service().rollback(
        tenant_id=tenant_id,
        policy_id=policy_id,
        target_version=body.target_version,
        reason=body.reason,
        correlation_id=correlation_id,
        actor_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
