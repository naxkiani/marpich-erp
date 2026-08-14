"""P218-C aggregates — space DDD bounded-context invariants."""
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
        if not present: raise ValueError("space.domain.space_core_domain_is_missing")
        return _mk(cls, tenant_id, "domain_ref", domain_ref, "space.domain.space_core_domain_is_missing", "MissionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BoundedContextMapRoot(AggregateRoot):
    tenant_id: str; map_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, map_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.bounded_context_map_is_missing")
        return _mk(cls, tenant_id, "map_ref", map_ref, "space.domain.bounded_context_map_is_missing", "MissionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionManagementDomainRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "space.domain.aggregates_are_missing", "MissionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalOperationsDomainRoot(AggregateRoot):
    tenant_id: str; orbit_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, orbit_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "orbit_ref", orbit_ref, "space.domain.aggregates_are_missing", "OrbitUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteFleetDomainRoot(AggregateRoot):
    tenant_id: str; satellite_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, satellite_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "satellite_ref", satellite_ref, "space.domain.aggregates_are_missing", "SatelliteActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceAIDomainRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.domain.aggregates_are_missing", "PredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ScientificResearchDomainRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "research_ref", research_ref, "space.domain.aggregates_are_missing", "DiscoveryValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceEconomyDomainRoot(AggregateRoot):
    tenant_id: str; economy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, economy_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "economy_ref", economy_ref, "space.domain.aggregates_are_missing", "ContractSignedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceSecurityDomainRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.domain.aggregates_are_missing", "ThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceDigitalTwinDomainRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.domain.aggregates_are_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.domain.aggregates_are_missing", "SimulationExecutedEvent")
    def is_missing(self)->bool: return not self.present
