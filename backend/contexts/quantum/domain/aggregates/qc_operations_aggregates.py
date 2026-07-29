"""P215-N aggregates — quantum operations / AIOps / self-healing invariants."""
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
class QuantumOperationsPlatformRoot(AggregateRoot):
    tenant_id: str; operations_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, operations_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.quantum_operations_platform_is_missing")
        return _mk(cls, tenant_id, "operations_ref", operations_ref, "quantum.operations.quantum_operations_platform_is_missing", "QuantumResourceRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumAIOpsPlatformRoot(AggregateRoot):
    tenant_id: str; aiops_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, aiops_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.quantum_aiops_platform_is_missing")
        return _mk(cls, tenant_id, "aiops_ref", aiops_ref, "quantum.operations.quantum_aiops_platform_is_missing", "AnomalyDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ObservabilityIntelligenceRoot(AggregateRoot):
    tenant_id: str; observability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, observability_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.observability_intelligence_is_missing")
        return _mk(cls, tenant_id, "observability_ref", observability_ref, "quantum.operations.observability_intelligence_is_missing", "TelemetryReceivedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IncidentAutomationRoot(AggregateRoot):
    tenant_id: str; incident_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, incident_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.incident_automation_is_missing")
        return _mk(cls, tenant_id, "incident_ref", incident_ref, "quantum.operations.incident_automation_is_missing", "IncidentCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SelfHealingInfrastructureRoot(AggregateRoot):
    tenant_id: str; healing_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, healing_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.self_healing_infrastructure_is_missing")
        return _mk(cls, tenant_id, "healing_ref", healing_ref, "quantum.operations.self_healing_infrastructure_is_missing", "SelfHealingExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousManagementRoot(AggregateRoot):
    tenant_id: str; autonomous_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomous_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.autonomous_management_is_missing")
        return _mk(cls, tenant_id, "autonomous_ref", autonomous_ref, "quantum.operations.autonomous_management_is_missing", "QuantumRecoveryStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ReliabilityEngineeringRoot(AggregateRoot):
    tenant_id: str; reliability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reliability_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.reliability_engineering_is_missing")
        return _mk(cls, tenant_id, "reliability_ref", reliability_ref, "quantum.operations.reliability_engineering_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PerformanceIntelligenceRoot(AggregateRoot):
    tenant_id: str; performance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, performance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.performance_intelligence_is_missing")
        return _mk(cls, tenant_id, "performance_ref", performance_ref, "quantum.operations.performance_intelligence_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OperationsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.operations.knowledge_graph_integration_is_missing", "QuantumResourceRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OperationsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.operations.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.operations.digital_twin_integration_is_missing", "SelfHealingExecutedEvent")
    def is_missing(self)->bool: return not self.present
