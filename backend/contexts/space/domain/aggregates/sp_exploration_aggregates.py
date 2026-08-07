"""P218-L aggregates — exploration intelligence invariants."""
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
class ExplorationPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.space_exploration_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.exploration.space_exploration_platform_is_missing", "ExplorationMissionCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LunarOperationsRoot(AggregateRoot):
    tenant_id: str; lunar_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lunar_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.lunar_operations_platform_is_missing")
        return _mk(cls, tenant_id, "lunar_ref", lunar_ref, "space.exploration.lunar_operations_platform_is_missing", "LandingCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MarsOperationsRoot(AggregateRoot):
    tenant_id: str; mars_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mars_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.mars_operations_platform_is_missing")
        return _mk(cls, tenant_id, "mars_ref", mars_ref, "space.exploration.mars_operations_platform_is_missing", "SurfaceMissionStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DeepSpaceRoot(AggregateRoot):
    tenant_id: str; deep_space_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, deep_space_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.deep_space_exploration_platform_is_missing")
        return _mk(cls, tenant_id, "deep_space_ref", deep_space_ref, "space.exploration.deep_space_exploration_platform_is_missing", "MissionReplannedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ExplorationAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.exploration_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.exploration.exploration_ai_is_missing", "HazardDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomyRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.autonomous_exploration_is_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "space.exploration.autonomous_exploration_is_missing", "SampleCollectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ExplorationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.exploration_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.exploration.exploration_digital_twin_is_missing", "HabitatActivatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ExplorationGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.governance_and_safety_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.exploration.governance_and_safety_is_missing", "ExplorationMissionCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ExplorationSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.exploration.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.exploration.security_architecture_is_missing", "ScientificTargetIdentifiedEvent")
    def is_missing(self) -> bool: return not self.present
