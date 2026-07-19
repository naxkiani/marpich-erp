"""Trust facts DTO — maps 1:1 to shared FederationTrustFacts port contract."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.application.ports.identity_federation import FederationTrustFacts


@dataclass(frozen=True, slots=True)
class TrustFactsDTO:
    tenant_id: str
    subject_id: str
    subject_kind: str = "human"
    trust_score: float = 0.0
    risk_score: float = 0.0
    federation_session_id: str | None = None
    identity_link_id: str | None = None
    provider_id: str | None = None
    zero_trust_level: str = "unknown"
    attributes: dict = field(default_factory=dict)
    reason_codes: list[str] = field(default_factory=list)

    def to_port(self) -> FederationTrustFacts:
        return FederationTrustFacts(
            tenant_id=self.tenant_id,
            subject_id=self.subject_id,
            subject_kind=self.subject_kind,
            trust_score=self.trust_score,
            risk_score=self.risk_score,
            federation_session_id=self.federation_session_id,
            identity_link_id=self.identity_link_id,
            provider_id=self.provider_id,
            zero_trust_level=self.zero_trust_level,
            attributes=dict(self.attributes),
            reason_codes=list(self.reason_codes),
        )

    def to_dict(self) -> dict:
        return self.to_port().to_dict()
