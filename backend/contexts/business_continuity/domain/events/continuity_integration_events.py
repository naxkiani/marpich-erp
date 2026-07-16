"""Enterprise Business Continuity Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class ContinuityPlanCreatedIntegration(IntegrationEvent):
    plan_ref: str
    plan_type: str
    criticality_tier: str

    @property
    def event_name(self) -> str:
        return "continuity.plan.created"

    @property
    def source_context(self) -> str:
        return "business_continuity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "plan_ref": self.plan_ref,
            "plan_type": self.plan_type,
            "criticality_tier": self.criticality_tier,
        }


@dataclass(frozen=True, kw_only=True)
class FailoverInitiatedIntegration(IntegrationEvent):
    failover_ref: str
    source_system: str
    target_system: str

    @property
    def event_name(self) -> str:
        return "continuity.failover.initiated"

    @property
    def source_context(self) -> str:
        return "business_continuity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "failover_ref": self.failover_ref,
            "source_system": self.source_system,
            "target_system": self.target_system,
        }


@dataclass(frozen=True, kw_only=True)
class FailoverCompletedIntegration(IntegrationEvent):
    failover_ref: str
    status: str

    @property
    def event_name(self) -> str:
        return "continuity.failover.completed"

    @property
    def source_context(self) -> str:
        return "business_continuity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"failover_ref": self.failover_ref, "status": self.status}


@dataclass(frozen=True, kw_only=True)
class RecoveryTestCompletedIntegration(IntegrationEvent):
    test_ref: str
    plan_ref: str
    passed: bool

    @property
    def event_name(self) -> str:
        return "continuity.test.completed"

    @property
    def source_context(self) -> str:
        return "business_continuity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "test_ref": self.test_ref,
            "plan_ref": self.plan_ref,
            "passed": self.passed,
        }


@dataclass(frozen=True, kw_only=True)
class EmergencyOpsActivatedIntegration(IntegrationEvent):
    plan_ref: str
    title: str

    @property
    def event_name(self) -> str:
        return "continuity.emergency_ops.activated"

    @property
    def source_context(self) -> str:
        return "business_continuity"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"plan_ref": self.plan_ref, "title": self.title}
