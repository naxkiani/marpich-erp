"""P219-A aggregates — civilization mission / vision / strategy invariants."""
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
class CivilizationMissionRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.civilization_os_mission_framework_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "civilization.mission.civilization_os_mission_framework_is_missing", "CivilizationStrategyCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationVisionRoot(AggregateRoot):
    tenant_id: str; vision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, vision_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.civilization_os_vision_framework_is_missing")
        return _mk(cls, tenant_id, "vision_ref", vision_ref, "civilization.mission.civilization_os_vision_framework_is_missing", "CivilizationVisionDefinedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicScopeRoot(AggregateRoot):
    tenant_id: str; scope_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scope_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.strategic_civilization_scope_is_missing")
        return _mk(cls, tenant_id, "scope_ref", scope_ref, "civilization.mission.strategic_civilization_scope_is_missing", "StrategicScopePublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CapabilityFrameworkRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.civilization_os_capability_framework_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "civilization.mission.civilization_os_capability_framework_is_missing", "CapabilityFrameworkPublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicPillarsRoot(AggregateRoot):
    tenant_id: str; pillars_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, pillars_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.strategic_pillars_framework_is_missing")
        return _mk(cls, tenant_id, "pillars_ref", pillars_ref, "civilization.mission.strategic_pillars_framework_is_missing", "PillarsFrameworkPublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class MaturityModelRoot(AggregateRoot):
    tenant_id: str; maturity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, maturity_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.maturity_model_is_missing")
        return _mk(cls, tenant_id, "maturity_ref", maturity_ref, "civilization.mission.maturity_model_is_missing", "CivilizationReadinessImprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionRoadmapRoot(AggregateRoot):
    tenant_id: str; roadmap_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.future_evolution_roadmap_is_missing")
        return _mk(cls, tenant_id, "roadmap_ref", roadmap_ref, "civilization.mission.future_evolution_roadmap_is_missing", "CivilizationRoadmapUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceStrategyRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.governance_framework_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "civilization.mission.governance_framework_is_missing", "CivilizationStrategyCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IntegrationStrategyRoot(AggregateRoot):
    tenant_id: str; integration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, integration_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.mission.meos_integration_strategy_is_missing")
        return _mk(cls, tenant_id, "integration_ref", integration_ref, "civilization.mission.meos_integration_strategy_is_missing", "IntegrationStrategyAlignedEvent")
    def is_missing(self) -> bool: return not self.present
