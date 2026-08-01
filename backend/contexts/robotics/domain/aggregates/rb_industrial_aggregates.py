"""P216-F aggregates — industrial automation / smart factory invariants."""
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
class SmartFactoryRoot(AggregateRoot):
    tenant_id: str; factory_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, factory_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.smart_factory_platform_is_missing")
        return _mk(cls, tenant_id, "factory_ref", factory_ref, "robotics.industrial.smart_factory_platform_is_missing", "ProductionOrderCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IndustrialAutomationRoot(AggregateRoot):
    tenant_id: str; automation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, automation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.industrial_automation_platform_is_missing")
        return _mk(cls, tenant_id, "automation_ref", automation_ref, "robotics.industrial.industrial_automation_platform_is_missing", "ProductionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousManufacturingRoot(AggregateRoot):
    tenant_id: str; autonomous_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomous_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.autonomous_manufacturing_platform_is_missing")
        return _mk(cls, tenant_id, "autonomous_ref", autonomous_ref, "robotics.industrial.autonomous_manufacturing_platform_is_missing", "FactoryOptimisationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ManufacturingExecutionRoot(AggregateRoot):
    tenant_id: str; mes_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mes_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.manufacturing_execution_intelligence_is_missing")
        return _mk(cls, tenant_id, "mes_ref", mes_ref, "robotics.industrial.manufacturing_execution_intelligence_is_missing", "ProductionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FactoryDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.factory_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.industrial.factory_digital_twin_is_missing", "FactoryOptimisationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PredictiveMaintenanceRoot(AggregateRoot):
    tenant_id: str; maintenance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, maintenance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.predictive_maintenance_is_missing")
        return _mk(cls, tenant_id, "maintenance_ref", maintenance_ref, "robotics.industrial.predictive_maintenance_is_missing", "MachineFailureDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IndustrialKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.industrial_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.industrial.industrial_knowledge_graph_is_missing", "ProductionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IndustrialCybersecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.industrial_cybersecurity_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.industrial.industrial_cybersecurity_is_missing", "MachineFailureDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IndustrialAnalyticsRoot(AggregateRoot):
    tenant_id: str; analytics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, analytics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.industrial.industrial_analytics_platform_is_missing")
        return _mk(cls, tenant_id, "analytics_ref", analytics_ref, "robotics.industrial.industrial_analytics_platform_is_missing", "FactoryOptimisationCompletedEvent")
    def is_missing(self)->bool: return not self.present
