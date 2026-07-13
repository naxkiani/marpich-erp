"""Data isolation integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class PrincipalSyncedIntegration(IntegrationEvent):
    synced_count: int
    created_count: int

    @property
    def event_name(self) -> str:
        return "data_isolation.principal.synced"

    @property
    def source_context(self) -> str:
        return "data_isolation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"synced_count": self.synced_count, "created_count": self.created_count}


@dataclass(frozen=True, kw_only=True)
class RlsVerifiedIntegration(IntegrationEvent):
    tenant_id_checked: str
    policies_checked: int
    passed: bool

    @property
    def event_name(self) -> str:
        return "data_isolation.rls.verified"

    @property
    def source_context(self) -> str:
        return "data_isolation"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "tenant_id_checked": self.tenant_id_checked,
            "policies_checked": self.policies_checked,
            "passed": self.passed,
        }
