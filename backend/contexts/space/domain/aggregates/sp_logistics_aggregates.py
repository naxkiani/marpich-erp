"""P218-O aggregates — logistics intelligence invariants."""
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
class LogisticsPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.space_logistics_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.logistics.space_logistics_platform_is_missing", "CargoCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousCargoRoot(AggregateRoot):
    tenant_id: str; cargo_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cargo_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.autonomous_cargo_systems_is_missing")
        return _mk(cls, tenant_id, "cargo_ref", cargo_ref, "space.logistics.autonomous_cargo_systems_is_missing", "CargoDeliveredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SupplyChainRoot(AggregateRoot):
    tenant_id: str; supply_chain_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, supply_chain_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.orbital_supply_chain_is_missing")
        return _mk(cls, tenant_id, "supply_chain_ref", supply_chain_ref, "space.logistics.orbital_supply_chain_is_missing", "SupplyChainDisruptedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class InterplanetaryTransportRoot(AggregateRoot):
    tenant_id: str; interplanetary_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, interplanetary_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.interplanetary_transportation_is_missing")
        return _mk(cls, tenant_id, "interplanetary_ref", interplanetary_ref, "space.logistics.interplanetary_transportation_is_missing", "ShipmentLaunchedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LogisticsAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.logistics_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.logistics.logistics_ai_is_missing", "RouteOptimizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LogisticsRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.robotics_integration_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "space.logistics.robotics_integration_is_missing", "InventoryUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LogisticsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.logistics.digital_twin_is_missing", "TransportScheduledEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LogisticsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.logistics.knowledge_graph_is_missing", "CargoAllocatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LogisticsSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.logistics.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.logistics.security_architecture_is_missing", "EmergencyRouteActivatedEvent")
    def is_missing(self) -> bool: return not self.present
