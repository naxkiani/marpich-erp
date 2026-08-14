"""P215-B aggregates — quantum mission/strategy invariants."""
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
class MissionRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.quantum_mission_framework_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "quantum.mission.quantum_mission_framework_is_missing", "QuantumStrategyCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class VisionRoot(AggregateRoot):
    tenant_id: str; vision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, vision_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.quantum_vision_framework_is_missing")
        return _mk(cls, tenant_id, "vision_ref", vision_ref, "quantum.mission.quantum_vision_framework_is_missing", "QuantumVisionDefinedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class StrategicScopeRoot(AggregateRoot):
    tenant_id: str; scope_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scope_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.strategic_intelligence_scope_is_missing")
        return _mk(cls, tenant_id, "scope_ref", scope_ref, "quantum.mission.strategic_intelligence_scope_is_missing", "QuantumCapabilityAddedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class MaturityRoot(AggregateRoot):
    tenant_id: str; maturity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, maturity_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.quantum_maturity_model_is_missing")
        return _mk(cls, tenant_id, "maturity_ref", maturity_ref, "quantum.mission.quantum_maturity_model_is_missing", "QuantumReadinessImprovedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class RoadmapRoot(AggregateRoot):
    tenant_id: str; roadmap_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.quantum_roadmap_is_missing")
        return _mk(cls, tenant_id, "roadmap_ref", roadmap_ref, "quantum.mission.quantum_roadmap_is_missing", "QuantumInitiativeCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class BusinessValueRoot(AggregateRoot):
    tenant_id: str; value_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, value_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.business_value_architecture_is_missing")
        return _mk(cls, tenant_id, "value_ref", value_ref, "quantum.mission.business_value_architecture_is_missing", "QuantumCapabilityAddedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class StrategicTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.mission.strategic_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.mission.strategic_digital_twin_is_missing", "QuantumReadinessImprovedEvent")
    def is_missing(self)->bool: return not self.present
