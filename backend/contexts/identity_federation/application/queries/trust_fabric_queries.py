"""Trust Fabric queries (P200-B6)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.ports.federation_repositories import (
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services.eiftp_trust_fabric import (
    validate_trust_fabric_foundation,
)
from contexts.identity_federation.domain.services.trust_fabric_engine import get_trust_fabric_engine
from contexts.identity_federation.domain.value_objects.trust_levels import level_from_score, level_name
from contexts.identity_federation.infrastructure.persistence.trust_evidence_store import (
    get_trust_evidence_store,
)


@dataclass(frozen=True, slots=True)
class GetTrustStatusQuery:
    tenant_id: str
    trust_ref: str


@dataclass(frozen=True, slots=True)
class GetTrustScoreQuery:
    tenant_id: str
    trust_ref: str
    inputs: dict | None = None


@dataclass(frozen=True, slots=True)
class GetTrustHistoryQuery:
    tenant_id: str
    trust_ref: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetTrustEvidenceQuery:
    tenant_id: str
    trust_ref: str
    limit: int = 50


@dataclass(frozen=True, slots=True)
class GetRiskProfileQuery:
    tenant_id: str
    trust_ref: str


async def _load(trusts: ITrustRelationshipRepository, tenant_id: str, trust_ref: str):
    for t in await trusts.list_by_tenant(tenant_id):
        if t.trust_ref == trust_ref:
            return t
    return None


async def handle_get_trust_status(
    query: GetTrustStatusQuery, *, trusts: ITrustRelationshipRepository
) -> dict:
    trust = await _load(trusts, query.tenant_id, query.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    level = int((trust.metadata or {}).get("enterprise_level") or level_from_score(trust.trust_score))
    return {
        "trust_ref": trust.trust_ref,
        "status": trust.status,
        "trust_score": trust.trust_score,
        "legacy_level": trust.trust_level,
        "enterprise_level": level,
        "enterprise_level_name": level_name(level),
        "source": {"type": trust.source_entity_type, "id": trust.source_entity_id},
        "target": {"type": trust.target_entity_type, "id": trust.target_entity_id},
    }


async def handle_get_trust_score(
    query: GetTrustScoreQuery, *, trusts: ITrustRelationshipRepository
) -> dict:
    trust = await _load(trusts, query.tenant_id, query.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    evaluation = get_trust_fabric_engine().evaluate_continuous(
        inputs=query.inputs or {},
        prior_score=trust.trust_score,
    )
    return {"trust_ref": query.trust_ref, "evaluation": evaluation}


async def handle_get_trust_history(query: GetTrustHistoryQuery) -> dict:
    items = get_trust_evidence_store().list_history(
        query.tenant_id, query.trust_ref, limit=query.limit
    )
    return {"trust_ref": query.trust_ref, "history": items, "count": len(items)}


async def handle_get_trust_evidence(query: GetTrustEvidenceQuery) -> dict:
    items = get_trust_evidence_store().list_evidence(
        query.tenant_id, query.trust_ref, limit=query.limit
    )
    return {"trust_ref": query.trust_ref, "evidence": items, "count": len(items)}


async def handle_get_risk_profile(
    query: GetRiskProfileQuery, *, trusts: ITrustRelationshipRepository
) -> dict:
    trust = await _load(trusts, query.tenant_id, query.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    last = (trust.metadata or {}).get("last_evaluation") or {}
    zt = last.get("zero_trust") or {}
    return {
        "trust_ref": query.trust_ref,
        "risk_score": zt.get("risk_score"),
        "zero_trust_action": zt.get("action"),
        "weakest_link": last.get("weakest_link"),
        "factors": last.get("factors") or [],
    }


def handle_get_trust_graph_catalog() -> dict:
    return get_trust_fabric_engine().graph_catalog()


def handle_get_trust_fabric_surface() -> dict:
    return {
        "prompt": "P200-B6",
        "adr": 220,
        "graph": get_trust_fabric_engine().graph_catalog(),
        "validation": validate_trust_fabric_foundation(),
        "principles": [
            "never_trust_automatically",
            "always_verify",
            "continuous_evaluation",
            "least_trust_privilege",
            "transparent_decisions",
        ],
    }
