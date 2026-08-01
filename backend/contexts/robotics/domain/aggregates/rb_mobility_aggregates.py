"""P216-H aggregates — autonomous mobility / connected vehicles / drones invariants."""
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
class ConnectedVehicleRoot(AggregateRoot):
    tenant_id: str; vehicle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, vehicle_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.connected_vehicle_platform_is_missing")
        return _mk(cls, tenant_id, "vehicle_ref", vehicle_ref, "robotics.mobility.connected_vehicle_platform_is_missing", "VehicleConnectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousNavigationRoot(AggregateRoot):
    tenant_id: str; navigation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, navigation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.autonomous_navigation_platform_is_missing")
        return _mk(cls, tenant_id, "navigation_ref", navigation_ref, "robotics.mobility.autonomous_navigation_platform_is_missing", "NavigationUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DroneIntelligenceRoot(AggregateRoot):
    tenant_id: str; drone_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, drone_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.drone_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "drone_ref", drone_ref, "robotics.mobility.drone_intelligence_platform_is_missing", "DroneTakeoffEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FleetMobilityRoot(AggregateRoot):
    tenant_id: str; fleet_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fleet_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.fleet_mobility_platform_is_missing")
        return _mk(cls, tenant_id, "fleet_ref", fleet_ref, "robotics.mobility.fleet_mobility_platform_is_missing", "FleetOptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartTransportationRoot(AggregateRoot):
    tenant_id: str; transportation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, transportation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.smart_transportation_platform_is_missing")
        return _mk(cls, tenant_id, "transportation_ref", transportation_ref, "robotics.mobility.smart_transportation_platform_is_missing", "TrafficCongestionDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MobilityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.mobility_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.mobility.mobility_digital_twin_is_missing", "NavigationUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TransportationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.transportation_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.mobility.transportation_knowledge_graph_is_missing", "FleetOptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MobilitySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.mobility.security_architecture_is_missing", "EmergencyRouteActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MobilityObservabilityRoot(AggregateRoot):
    tenant_id: str; observability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, observability_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.mobility.observability_platform_is_missing")
        return _mk(cls, tenant_id, "observability_ref", observability_ref, "robotics.mobility.observability_platform_is_missing", "MissionStartedEvent")
    def is_missing(self)->bool: return not self.present
