"""Trust Fabric CQRS commands (P200-B6)."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.identity_federation.domain.factories import TrustRelationshipFactory
from contexts.identity_federation.domain.ports.federation_repositories import (
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services.trust_fabric_engine import get_trust_fabric_engine
from contexts.identity_federation.domain.value_objects.trust_levels import level_from_score
from contexts.identity_federation.infrastructure.observability import federation_trust_metrics
from contexts.identity_federation.infrastructure.persistence.trust_evidence_store import (
    get_trust_evidence_store,
)


@dataclass(frozen=True, slots=True)
class CreateTrustRelationshipCommand:
    tenant_id: str
    trust_ref: str | None = None
    source_entity_type: str = "organization"
    source_entity_id: str = ""
    target_entity_type: str = "organization"
    target_entity_id: str = ""
    trust_score: int = 50
    trust_type: str = "enterprise"
    auto_grant: bool = False
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class ApproveTrustCommand:
    tenant_id: str
    trust_ref: str
    correlation_id: str = ""


@dataclass(frozen=True, slots=True)
class EvaluateTrustContinuousCommand:
    tenant_id: str
    trust_ref: str
    inputs: dict = field(default_factory=dict)
    zero_trust_ctx: dict = field(default_factory=dict)
    persist_history: bool = True


@dataclass(frozen=True, slots=True)
class AddTrustEvidenceCommand:
    tenant_id: str
    trust_ref: str
    evidence_type: str
    payload: dict = field(default_factory=dict)
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class RevokeTrustCommand:
    tenant_id: str
    trust_ref: str
    reason: str = "revoked"
    correlation_id: str = ""


async def _get_trust(trusts: ITrustRelationshipRepository, tenant_id: str, trust_ref: str):
    for t in await trusts.list_by_tenant(tenant_id):
        if t.trust_ref == trust_ref:
            return t
    return None


async def handle_create_trust_relationship(
    command: CreateTrustRelationshipCommand,
    *,
    trusts: ITrustRelationshipRepository,
) -> dict:
    ref = command.trust_ref or trusts.next_trust_ref(command.tenant_id)
    trust = TrustRelationshipFactory.create_pending(
        tenant_id=command.tenant_id,
        trust_ref=ref,
        source_entity_type=command.source_entity_type,
        source_entity_id=command.source_entity_id,
        target_entity_type=command.target_entity_type,
        target_entity_id=command.target_entity_id,
        trust_score=command.trust_score,
    )
    trust.metadata = {**(trust.metadata or {}), "trust_type": command.trust_type}
    events: list[str] = []
    if command.auto_grant:
        trust.grant(correlation_id=command.correlation_id)
        events = [e.event_name for e in trust.clear_events()]
    await trusts.save(trust)
    federation_trust_metrics.increment("trust_relationship_created_total")
    store = get_trust_evidence_store()
    store.append_history(
        tenant_id=command.tenant_id,
        trust_ref=ref,
        trust_score=trust.trust_score,
        enterprise_level=level_from_score(trust.trust_score),
        reason="created",
    )
    return {**trust.to_dict(), "enterprise_level": level_from_score(trust.trust_score), "domain_events": events}


async def handle_approve_trust(
    command: ApproveTrustCommand,
    *,
    trusts: ITrustRelationshipRepository,
) -> dict:
    trust = await _get_trust(trusts, command.tenant_id, command.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    trust.grant(correlation_id=command.correlation_id)
    await trusts.save(trust)
    store = get_trust_evidence_store()
    store.add_evidence(
        tenant_id=command.tenant_id,
        trust_ref=command.trust_ref,
        evidence_type="agreement",
        payload={"action": "approved"},
    )
    store.append_history(
        tenant_id=command.tenant_id,
        trust_ref=command.trust_ref,
        trust_score=trust.trust_score,
        enterprise_level=level_from_score(trust.trust_score),
        reason="approved",
    )
    federation_trust_metrics.increment("trust_approved_total")
    events = [e.event_name for e in trust.clear_events()]
    return {**trust.to_dict(), "domain_events": events}


async def handle_evaluate_trust_continuous(
    command: EvaluateTrustContinuousCommand,
    *,
    trusts: ITrustRelationshipRepository,
) -> dict:
    trust = await _get_trust(trusts, command.tenant_id, command.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    fabric = get_trust_fabric_engine()
    evaluation = fabric.evaluate_continuous(
        inputs=command.inputs,
        prior_score=trust.trust_score,
        zero_trust_ctx=command.zero_trust_ctx,
    )
    trust.rescore(evaluation["trust_score"])
    trust.metadata = {
        **(trust.metadata or {}),
        "enterprise_level": evaluation["enterprise_level"],
        "last_evaluation": evaluation,
    }
    await trusts.save(trust)
    if command.persist_history:
        get_trust_evidence_store().append_history(
            tenant_id=command.tenant_id,
            trust_ref=command.trust_ref,
            trust_score=evaluation["trust_score"],
            enterprise_level=evaluation["enterprise_level"],
            reason="continuous_evaluation",
            factors=list(evaluation.get("factors") or []),
        )
    federation_trust_metrics.increment("trust_evaluated_total")
    return {
        "trust_ref": command.trust_ref,
        "status": trust.status,
        "evaluation": evaluation,
        "permit_deny": None,
    }


async def handle_add_trust_evidence(command: AddTrustEvidenceCommand) -> dict:
    entry = get_trust_evidence_store().add_evidence(
        tenant_id=command.tenant_id,
        trust_ref=command.trust_ref,
        evidence_type=command.evidence_type,
        payload=command.payload,
        actor_id=command.actor_id,
    )
    federation_trust_metrics.increment("trust_evidence_added_total")
    return entry


async def handle_revoke_trust(
    command: RevokeTrustCommand,
    *,
    trusts: ITrustRelationshipRepository,
) -> dict:
    trust = await _get_trust(trusts, command.tenant_id, command.trust_ref)
    if trust is None:
        raise ValueError("trust.not_found")
    trust.revoke(reason=command.reason, correlation_id=command.correlation_id)
    await trusts.save(trust)
    get_trust_evidence_store().append_history(
        tenant_id=command.tenant_id,
        trust_ref=command.trust_ref,
        trust_score=0,
        enterprise_level=0,
        reason=command.reason or "revoked",
    )
    federation_trust_metrics.increment("trust_revoked_total")
    events = [e.event_name for e in trust.clear_events()]
    return {**trust.to_dict(), "enterprise_level": 0, "domain_events": events}
