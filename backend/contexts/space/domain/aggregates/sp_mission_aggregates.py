"""P218-A aggregates — space mission / vision / strategy invariants."""
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
class SpaceMissionRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.space_mission_framework_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "space.mission.space_mission_framework_is_missing", "SpaceStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceVisionRoot(AggregateRoot):
    tenant_id: str; vision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, vision_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.space_vision_framework_is_missing")
        return _mk(cls, tenant_id, "vision_ref", vision_ref, "space.mission.space_vision_framework_is_missing", "SpaceVisionDefinedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class StrategicScopeRoot(AggregateRoot):
    tenant_id: str; scope_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scope_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.strategic_space_scope_is_missing")
        return _mk(cls, tenant_id, "scope_ref", scope_ref, "space.mission.strategic_space_scope_is_missing", "StrategicScopePublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CapabilityFrameworkRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.space_capability_framework_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "space.mission.space_capability_framework_is_missing", "StrategicScopePublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ValueStreamsRoot(AggregateRoot):
    tenant_id: str; value_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, value_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.value_streams_framework_is_missing")
        return _mk(cls, tenant_id, "value_ref", value_ref, "space.mission.value_streams_framework_is_missing", "SpaceStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MaturityModelRoot(AggregateRoot):
    tenant_id: str; maturity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, maturity_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.maturity_model_is_missing")
        return _mk(cls, tenant_id, "maturity_ref", maturity_ref, "space.mission.maturity_model_is_missing", "SpaceReadinessImprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionRoadmapRoot(AggregateRoot):
    tenant_id: str; roadmap_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.future_evolution_roadmap_is_missing")
        return _mk(cls, tenant_id, "roadmap_ref", roadmap_ref, "space.mission.future_evolution_roadmap_is_missing", "SpaceRoadmapUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernanceStrategyRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.governance_framework_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.mission.governance_framework_is_missing", "SpaceStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntegrationStrategyRoot(AggregateRoot):
    tenant_id: str; integration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, integration_ref: str, present: bool = True):
        if not present: raise ValueError("space.mission.meos_integration_strategy_is_missing")
        return _mk(cls, tenant_id, "integration_ref", integration_ref, "space.mission.meos_integration_strategy_is_missing", "SpaceStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present
