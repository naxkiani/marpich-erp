"""Federation trust facts for peer modules (AuthZ, twins, PEPs).

EIFTP supplies facts only — never Permit/Deny (that is IAuthorizationEvaluator).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class FederationTrustFacts:
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

    def to_dict(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "subject_id": self.subject_id,
            "subject_kind": self.subject_kind,
            "trust_score": self.trust_score,
            "risk_score": self.risk_score,
            "federation_session_id": self.federation_session_id,
            "identity_link_id": self.identity_link_id,
            "provider_id": self.provider_id,
            "zero_trust_level": self.zero_trust_level,
            "attributes": dict(self.attributes),
            "reason_codes": list(self.reason_codes),
        }

    @classmethod
    def from_payload(cls, data: dict) -> FederationTrustFacts:
        return cls(
            tenant_id=str(data.get("tenant_id") or ""),
            subject_id=str(data.get("subject_id") or ""),
            subject_kind=str(data.get("subject_kind") or "human"),
            trust_score=float(data.get("trust_score") or 0.0),
            risk_score=float(data.get("risk_score") or 0.0),
            federation_session_id=data.get("federation_session_id"),
            identity_link_id=data.get("identity_link_id"),
            provider_id=data.get("provider_id"),
            zero_trust_level=str(data.get("zero_trust_level") or "unknown"),
            attributes=dict(data.get("attributes") or {}),
            reason_codes=list(data.get("reason_codes") or []),
        )


class IFederationTrustFacts(Protocol):
    """Cross-module port — implemented by identity_federation adapters only."""

    async def get_trust_facts(
        self,
        tenant_id: str,
        *,
        subject_id: str,
        federation_session_id: str | None = None,
    ) -> FederationTrustFacts: ...

    async def evaluate_trust(
        self,
        tenant_id: str,
        *,
        subject_id: str,
        subject_kind: str = "human",
        context: dict | None = None,
    ) -> FederationTrustFacts: ...
