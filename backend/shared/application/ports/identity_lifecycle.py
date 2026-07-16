"""Identity lifecycle status facts for peer modules (P201).

EILMP supplies status/risk facts only — never Permit/Deny (Authorization PDP).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, slots=True)
class IdentityLifecycleStatus:
    tenant_id: str
    subject_ref: str
    subject_kind: str = "registration"
    status: str = "unknown"
    identity_type: str = ""
    case_ref: str | None = None
    risk_score: float = 0.0
    trust_level: str = "unknown"
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "subject_ref": self.subject_ref,
            "subject_kind": self.subject_kind,
            "status": self.status,
            "identity_type": self.identity_type,
            "case_ref": self.case_ref,
            "risk_score": self.risk_score,
            "trust_level": self.trust_level,
            "attributes": dict(self.attributes),
        }


class IIdentityLifecycleStatus(Protocol):
    async def get_registration_status(
        self, *, tenant_id: str, registration_ref: str
    ) -> IdentityLifecycleStatus | None: ...

    async def get_case_status(
        self, *, tenant_id: str, case_ref: str
    ) -> IdentityLifecycleStatus | None: ...
