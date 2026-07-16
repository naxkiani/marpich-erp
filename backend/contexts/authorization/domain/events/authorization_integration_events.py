"""Authorization PDP integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class AccessGrantedIntegration(IntegrationEvent):
    decision_ref: str
    principal_id: str
    permission_code: str

    @property
    def event_name(self) -> str:
        return "authorization.access.granted"

    @property
    def source_context(self) -> str:
        return "authorization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "decision_ref": self.decision_ref,
            "principal_id": self.principal_id,
            "permission_code": self.permission_code,
        }


@dataclass(frozen=True, kw_only=True)
class AccessDeniedIntegration(IntegrationEvent):
    decision_ref: str
    principal_id: str
    permission_code: str
    reason_codes: list[str]

    @property
    def event_name(self) -> str:
        return "authorization.access.denied"

    @property
    def source_context(self) -> str:
        return "authorization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "decision_ref": self.decision_ref,
            "principal_id": self.principal_id,
            "permission_code": self.permission_code,
            "reason_codes": self.reason_codes,
        }


@dataclass(frozen=True, kw_only=True)
class AuthorizationDashboardGeneratedIntegration(IntegrationEvent):
    decisions_total: int
    policies_total: int

    @property
    def event_name(self) -> str:
        return "authorization.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "authorization"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "decisions_total": self.decisions_total,
            "policies_total": self.policies_total,
        }
