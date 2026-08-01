"""P216-C aggregates — robotics DDD bounded-context invariants."""
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
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj

@dataclass(eq=False, kw_only=True)
class CoreDomainRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.robotics_core_domain_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "robotics.domain.robotics_core_domain_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BoundedContextMapRoot(AggregateRoot):
    tenant_id: str; map_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, map_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.bounded_context_map_is_missing")
        return _mk(cls, tenant_id, "map_ref", map_ref, "robotics.domain.bounded_context_map_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RobotLifecycleDomainRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "robotics.domain.aggregates_are_missing", "RobotActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousMachineDomainRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "robotics.domain.aggregates_are_missing", "AutonomousDecisionExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PhysicalAIDomainRoot(AggregateRoot):
    tenant_id: str; physical_ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, physical_ai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "physical_ai_ref", physical_ai_ref, "robotics.domain.aggregates_are_missing", "PhysicalAIUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionDomainRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "robotics.domain.aggregates_are_missing", "MissionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FleetDomainRoot(AggregateRoot):
    tenant_id: str; fleet_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fleet_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "fleet_ref", fleet_ref, "robotics.domain.aggregates_are_missing", "FleetOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalTwinDomainRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.domain.aggregates_are_missing", "DigitalTwinSynchronizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SafetyDomainRoot(AggregateRoot):
    tenant_id: str; safety_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "safety_ref", safety_ref, "robotics.domain.aggregates_are_missing", "SafetyViolationDetectedEvent")
    def is_missing(self)->bool: return not self.present
