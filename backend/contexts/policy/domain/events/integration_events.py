"""Policy integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class VersionSubmittedIntegration(IntegrationEvent):
    policy_id: str
    version: int
    domain: str
    policy_key: str

    @property
    def event_name(self) -> str:
        return "policy.version.submitted"

    @property
    def source_context(self) -> str:
        return "policy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "domain": self.domain,
            "policy_key": self.policy_key,
        }


@dataclass(frozen=True, kw_only=True)
class VersionActivatedIntegration(IntegrationEvent):
    policy_id: str
    version: int
    domain: str
    policy_key: str

    @property
    def event_name(self) -> str:
        return "policy.version.activated"

    @property
    def source_context(self) -> str:
        return "policy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "domain": self.domain,
            "policy_key": self.policy_key,
        }


@dataclass(frozen=True, kw_only=True)
class VersionRolledBackIntegration(IntegrationEvent):
    policy_id: str
    from_version: int
    to_version: int
    reason: str

    @property
    def event_name(self) -> str:
        return "policy.version.rolled_back"

    @property
    def source_context(self) -> str:
        return "policy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "reason": self.reason,
        }


@dataclass(frozen=True, kw_only=True)
class EvaluationDeniedIntegration(IntegrationEvent):
    domain: str
    policy_key: str
    reason: str

    @property
    def event_name(self) -> str:
        return "policy.evaluation.denied"

    @property
    def source_context(self) -> str:
        return "policy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "domain": self.domain,
            "policy_key": self.policy_key,
            "reason": self.reason,
        }


@dataclass(frozen=True, kw_only=True)
class SimulationExecutedIntegration(IntegrationEvent):
    domain: str
    policy_key: str
    version_count: int

    @property
    def event_name(self) -> str:
        return "policy.simulation.executed"

    @property
    def source_context(self) -> str:
        return "policy"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "domain": self.domain,
            "policy_key": self.policy_key,
            "version_count": self.version_count,
        }
