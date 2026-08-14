"""P216-G aggregates — autonomous logistics / warehouse automation invariants."""
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
class AutonomousWarehouseRoot(AggregateRoot):
    tenant_id: str; warehouse_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, warehouse_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.autonomous_warehouse_platform_is_missing")
        return _mk(cls, tenant_id, "warehouse_ref", warehouse_ref, "robotics.logistics.autonomous_warehouse_platform_is_missing", "WarehouseOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupplyChainRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.supply_chain_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.logistics.supply_chain_robotics_platform_is_missing", "PickingMissionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MaterialFlowRoot(AggregateRoot):
    tenant_id: str; flow_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, flow_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.intelligent_material_flow_platform_is_missing")
        return _mk(cls, tenant_id, "flow_ref", flow_ref, "robotics.logistics.intelligent_material_flow_platform_is_missing", "WarehouseOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class WarehouseDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.warehouse_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.logistics.warehouse_digital_twin_is_missing", "WarehouseOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiLogisticsRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.ai_logistics_intelligence_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "robotics.logistics.ai_logistics_intelligence_is_missing", "WarehouseOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupplyChainKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.supply_chain_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.logistics.supply_chain_knowledge_graph_is_missing", "ShipmentDispatchedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TransportCoordinationRoot(AggregateRoot):
    tenant_id: str; transport_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, transport_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.transport_coordination_platform_is_missing")
        return _mk(cls, tenant_id, "transport_ref", transport_ref, "robotics.logistics.transport_coordination_platform_is_missing", "ShipmentDispatchedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class WarehouseSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.warehouse_security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.logistics.warehouse_security_architecture_is_missing", "PickingMissionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrderFulfilmentRoot(AggregateRoot):
    tenant_id: str; fulfilment_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fulfilment_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.logistics.intelligent_material_flow_platform_is_missing")
        return _mk(cls, tenant_id, "fulfilment_ref", fulfilment_ref, "robotics.logistics.intelligent_material_flow_platform_is_missing", "PackingCompletedEvent")
    def is_missing(self)->bool: return not self.present
