"""P216-A aggregates — robotics mission / vision / strategy invariants."""
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
class RoboticsMissionRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.robotics_mission_framework_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "robotics.mission.robotics_mission_framework_is_missing", "RoboticsStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsVisionRoot(AggregateRoot):
    tenant_id: str; vision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, vision_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.robotics_vision_framework_is_missing")
        return _mk(cls, tenant_id, "vision_ref", vision_ref, "robotics.mission.robotics_vision_framework_is_missing", "RoboticsVisionDefinedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class StrategicScopeRoot(AggregateRoot):
    tenant_id: str; scope_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scope_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.strategic_cyber_physical_scope_is_missing")
        return _mk(cls, tenant_id, "scope_ref", scope_ref, "robotics.mission.strategic_cyber_physical_scope_is_missing", "CyberPhysicalScopePublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CapabilityMapRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.capability_map_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "robotics.mission.capability_map_is_missing", "CyberPhysicalScopePublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OperatingModelRoot(AggregateRoot):
    tenant_id: str; model_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.operating_model_is_missing")
        return _mk(cls, tenant_id, "model_ref", model_ref, "robotics.mission.operating_model_is_missing", "RoboticsStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionRoadmapRoot(AggregateRoot):
    tenant_id: str; roadmap_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.evolution_roadmap_is_missing")
        return _mk(cls, tenant_id, "roadmap_ref", roadmap_ref, "robotics.mission.evolution_roadmap_is_missing", "RoboticsRoadmapUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernanceStrategyRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.governance_strategy_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "robotics.mission.governance_strategy_is_missing", "RoboticsStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityStrategyRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.security_strategy_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.mission.security_strategy_is_missing", "RoboticsStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BusinessValueRoot(AggregateRoot):
    tenant_id: str; value_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, value_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mission.business_value_framework_is_missing")
        return _mk(cls, tenant_id, "value_ref", value_ref, "robotics.mission.business_value_framework_is_missing", "RoboticsReadinessImprovedEvent")
    def is_missing(self)->bool: return not self.present
