"""P218-J aggregates — mission intelligence invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class MissionIntelPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.mission_intel.mission_intelligence_platform_is_missing", "MissionCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionPlanningRoot(AggregateRoot):
    tenant_id: str; planning_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, planning_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_planning_platform_is_missing")
        return _mk(cls, tenant_id, "planning_ref", planning_ref, "space.mission_intel.mission_planning_platform_is_missing", "MissionPlanGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionExecutionRoot(AggregateRoot):
    tenant_id: str; execution_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, execution_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_execution_platform_is_missing")
        return _mk(cls, tenant_id, "execution_ref", execution_ref, "space.mission_intel.mission_execution_platform_is_missing", "MissionExecutionStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionLifecycleRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_lifecycle_is_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "space.mission_intel.mission_lifecycle_is_missing", "MissionMilestoneReachedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.mission_intel.mission_ai_is_missing", "MissionAnomalyDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionResourcesRoot(AggregateRoot):
    tenant_id: str; resources_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resources_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_resource_management_is_missing")
        return _mk(cls, tenant_id, "resources_ref", resources_ref, "space.mission_intel.mission_resource_management_is_missing", "MissionReplannedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.mission_intel.mission_digital_twin_is_missing", "MissionMilestoneReachedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.mission_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.mission_intel.mission_governance_is_missing", "MissionReadinessReviewedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MissionSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission_intel.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.mission_intel.security_architecture_is_missing", "MissionLaunchAuthorizedEvent")
    def is_missing(self) -> bool: return not self.present
