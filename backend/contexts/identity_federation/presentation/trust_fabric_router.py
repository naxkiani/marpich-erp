"""Trust Fabric REST surface — continuous, explainable trust facts (P200-B6)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.trust_fabric_commands import (
    AddTrustEvidenceCommand,
    ApproveTrustCommand,
    CreateTrustRelationshipCommand,
    EvaluateTrustContinuousCommand,
    RevokeTrustCommand,
    handle_add_trust_evidence,
    handle_approve_trust,
    handle_create_trust_relationship,
    handle_evaluate_trust_continuous,
    handle_revoke_trust,
)
from contexts.identity_federation.application.queries.trust_fabric_queries import (
    GetRiskProfileQuery,
    GetTrustEvidenceQuery,
    GetTrustHistoryQuery,
    GetTrustScoreQuery,
    GetTrustStatusQuery,
    handle_get_risk_profile,
    handle_get_trust_evidence,
    handle_get_trust_fabric_surface,
    handle_get_trust_graph_catalog,
    handle_get_trust_history,
    handle_get_trust_score,
    handle_get_trust_status,
)
from contexts.identity_federation.container import get_trust_relationship_repository

trust_fabric_router = APIRouter(prefix="/federation/trust-fabric", tags=["federation-trust-fabric"])


@trust_fabric_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def trust_fabric_surface() -> dict:
    return {"data": handle_get_trust_fabric_surface()}


@trust_fabric_router.get(
    "/graph/catalog",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def trust_graph_catalog() -> dict:
    return {"data": handle_get_trust_graph_catalog()}


@trust_fabric_router.post(
    "/relationships",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def create_relationship(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_create_trust_relationship(
            CreateTrustRelationshipCommand(
                tenant_id=tenant_id,
                trust_ref=body.get("trust_ref"),
                source_entity_type=str(body.get("source_entity_type") or "organization"),
                source_entity_id=str(body.get("source_entity_id") or ""),
                target_entity_type=str(body.get("target_entity_type") or "organization"),
                target_entity_id=str(body.get("target_entity_id") or ""),
                trust_score=int(body.get("trust_score") or 50),
                trust_type=str(body.get("trust_type") or "enterprise"),
                auto_grant=bool(body.get("auto_grant") or False),
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.post(
    "/relationships/{trust_ref}/approve",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def approve_relationship(
    trust_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_approve_trust(
            ApproveTrustCommand(
                tenant_id=tenant_id,
                trust_ref=trust_ref,
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.post(
    "/relationships/{trust_ref}/evaluate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def evaluate_continuous(
    trust_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_evaluate_trust_continuous(
            EvaluateTrustContinuousCommand(
                tenant_id=tenant_id,
                trust_ref=trust_ref,
                inputs=dict(body.get("inputs") or {}),
                zero_trust_ctx=dict(body.get("zero_trust_ctx") or {}),
                persist_history=bool(body.get("persist_history", True)),
            ),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.post(
    "/relationships/{trust_ref}/evidence",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def add_evidence(
    trust_ref: str,
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_add_trust_evidence(
            AddTrustEvidenceCommand(
                tenant_id=tenant_id,
                trust_ref=trust_ref,
                evidence_type=str(body.get("evidence_type") or "authn"),
                payload=dict(body.get("payload") or {}),
                actor_id=body.get("actor_id"),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.post(
    "/relationships/{trust_ref}/revoke",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def revoke_relationship(
    trust_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_revoke_trust(
            RevokeTrustCommand(
                tenant_id=tenant_id,
                trust_ref=trust_ref,
                reason=str(body.get("reason") or "revoked"),
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.get(
    "/relationships/{trust_ref}/status",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_status(
    trust_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_trust_status(
            GetTrustStatusQuery(tenant_id=tenant_id, trust_ref=trust_ref),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.post(
    "/relationships/{trust_ref}/score",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_score(
    trust_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_get_trust_score(
            GetTrustScoreQuery(
                tenant_id=tenant_id,
                trust_ref=trust_ref,
                inputs=dict(body.get("inputs") or {}) or None,
            ),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@trust_fabric_router.get(
    "/relationships/{trust_ref}/history",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_history(
    trust_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_trust_history(
        GetTrustHistoryQuery(tenant_id=tenant_id, trust_ref=trust_ref, limit=min(limit, 100))
    )
    return {"data": result}


@trust_fabric_router.get(
    "/relationships/{trust_ref}/evidence",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_evidence(
    trust_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    result = await handle_get_trust_evidence(
        GetTrustEvidenceQuery(tenant_id=tenant_id, trust_ref=trust_ref, limit=min(limit, 100))
    )
    return {"data": result}


@trust_fabric_router.get(
    "/relationships/{trust_ref}/risk",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_risk(
    trust_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_risk_profile(
            GetRiskProfileQuery(tenant_id=tenant_id, trust_ref=trust_ref),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}
