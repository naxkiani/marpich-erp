"""EstablishTrust command — tactical CQRS write (P200-B4)."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.domain.factories import TrustRelationshipFactory
from contexts.identity_federation.domain.ports.federation_repositories import (
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.specifications import ActiveTrustSpec


@dataclass(frozen=True, slots=True)
class EstablishTrustCommand:
    tenant_id: str
    trust_ref: str
    source_entity_type: str
    source_entity_id: str
    target_entity_type: str
    target_entity_id: str
    trust_score: int = 50
    correlation_id: str = ""


async def handle_establish_trust(
    command: EstablishTrustCommand,
    *,
    trusts: ITrustRelationshipRepository,
) -> dict:
    trust = TrustRelationshipFactory.create_pending(
        tenant_id=command.tenant_id,
        trust_ref=command.trust_ref,
        source_entity_type=command.source_entity_type,
        source_entity_id=command.source_entity_id,
        target_entity_type=command.target_entity_type,
        target_entity_id=command.target_entity_id,
        trust_score=command.trust_score,
    )
    trust.grant(correlation_id=command.correlation_id)
    if not ActiveTrustSpec().is_satisfied_by(trust):
        raise ValueError("trust.active_spec_failed")
    await trusts.save(trust)
    events = [e.event_name for e in trust.clear_events()]
    return {**trust.to_dict(), "domain_events": events}
