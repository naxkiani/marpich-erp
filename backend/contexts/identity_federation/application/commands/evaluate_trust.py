"""Evaluate trust hierarchy command — produces facts, never Permit/Deny."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.identity_federation.application.dto.trust_facts import TrustFactsDTO
from contexts.identity_federation.domain.services import trust_management_engine


@dataclass(frozen=True, slots=True)
class EvaluateTrustCommand:
    tenant_id: str
    subject_id: str
    subject_kind: str = "human"
    organization_trust: int = 50
    partner_trust: int = 50
    identity_trust: int = 50
    device_trust: int = 50
    context: dict | None = None


async def handle_evaluate_trust(command: EvaluateTrustCommand) -> TrustFactsDTO:
    hierarchy = trust_management_engine.evaluate_trust_hierarchy(
        organization_trust=command.organization_trust,
        partner_trust=command.partner_trust,
        identity_trust=command.identity_trust,
        device_trust=command.device_trust,
    )
    ctx = command.context or {}
    return TrustFactsDTO(
        tenant_id=command.tenant_id,
        subject_id=command.subject_id,
        subject_kind=command.subject_kind,
        trust_score=float(hierarchy["composite_trust_score"]),
        risk_score=float(ctx.get("risk_score") or 0.0),
        federation_session_id=ctx.get("federation_session_id"),
        identity_link_id=ctx.get("identity_link_id"),
        provider_id=ctx.get("provider_id"),
        zero_trust_level=str(hierarchy["trust_level"]),
        attributes={
            "hierarchy": hierarchy["hierarchy"],
            "weakest_link": hierarchy["weakest_link"],
        },
        reason_codes=["federation.trust.evaluated"],
    )
