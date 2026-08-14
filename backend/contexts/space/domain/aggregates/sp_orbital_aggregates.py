"""P218-G aggregates — orbital intelligence invariants."""
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
class OrbitalPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.space_situational_awareness_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.orbital.space_situational_awareness_is_missing", "OrbitalObjectDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SsaRoot(AggregateRoot):
    tenant_id: str; ssa_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ssa_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.space_situational_awareness_is_missing")
        return _mk(cls, tenant_id, "ssa_ref", ssa_ref, "space.orbital.space_situational_awareness_is_missing", "OrbitUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TrafficRoot(AggregateRoot):
    tenant_id: str; traffic_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, traffic_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.orbital_traffic_management_is_missing")
        return _mk(cls, tenant_id, "traffic_ref", traffic_ref, "space.orbital.orbital_traffic_management_is_missing", "ConjunctionPredictedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollisionAvoidanceRoot(AggregateRoot):
    tenant_id: str; avoidance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, avoidance_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.collision_avoidance_is_missing")
        return _mk(cls, tenant_id, "avoidance_ref", avoidance_ref, "space.orbital.collision_avoidance_is_missing", "AvoidanceManeuverRecommendedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DebrisIntelligenceRoot(AggregateRoot):
    tenant_id: str; debris_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, debris_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.space_debris_intelligence_is_missing")
        return _mk(cls, tenant_id, "debris_ref", debris_ref, "space.orbital.space_debris_intelligence_is_missing", "DebrisFragmentDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.orbital_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.orbital.orbital_digital_twin_is_missing", "OrbitUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.orbital_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.orbital.orbital_knowledge_graph_is_missing", "ConjunctionPredictedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalAiAutonomyRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.ai_autonomy_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.orbital.ai_autonomy_is_missing", "AvoidanceManeuverRecommendedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.orbital.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.orbital.security_architecture_is_missing", "ManeuverApprovedEvent")
    def is_missing(self)->bool: return not self.present
