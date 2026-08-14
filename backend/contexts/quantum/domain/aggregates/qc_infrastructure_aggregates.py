"""P215-D aggregates — quantum infrastructure invariants."""
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
class InfrastructurePlatformRoot(AggregateRoot):
    tenant_id: str; infra_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, infra_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.quantum_infrastructure_platform_is_missing")
        return _mk(cls, tenant_id, "infra_ref", infra_ref, "quantum.infrastructure.quantum_infrastructure_platform_is_missing", "QuantumInfrastructureCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class HardwareAbstractionRoot(AggregateRoot):
    tenant_id: str; hardware_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hardware_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.hardware_abstraction_layer_is_missing")
        return _mk(cls, tenant_id, "hardware_ref", hardware_ref, "quantum.infrastructure.hardware_abstraction_layer_is_missing", "QuantumProcessorRegisteredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumCloudRoot(AggregateRoot):
    tenant_id: str; cloud_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cloud_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.quantum_cloud_architecture_is_missing")
        return _mk(cls, tenant_id, "cloud_ref", cloud_ref, "quantum.infrastructure.quantum_cloud_architecture_is_missing", "QuantumResourceProvisionedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ResourceFabricRoot(AggregateRoot):
    tenant_id: str; resource_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, resource_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.quantum_resource_fabric_is_missing")
        return _mk(cls, tenant_id, "resource_ref", resource_ref, "quantum.infrastructure.quantum_resource_fabric_is_missing", "QuantumResourceAllocatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class WorkloadOrchestrationRoot(AggregateRoot):
    tenant_id: str; workload_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, workload_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.workload_orchestration_is_missing")
        return _mk(cls, tenant_id, "workload_ref", workload_ref, "quantum.infrastructure.workload_orchestration_is_missing", "QuantumWorkloadScheduledEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class HybridComputeRoot(AggregateRoot):
    tenant_id: str; hybrid_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hybrid_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.hybrid_computing_architecture_is_missing")
        return _mk(cls, tenant_id, "hybrid_ref", hybrid_ref, "quantum.infrastructure.hybrid_computing_architecture_is_missing", "QuantumExecutionCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class InfraSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.zero_trust_security_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "quantum.infrastructure.zero_trust_security_is_missing", "QuantumInfrastructurePolicyAppliedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class InfraTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.infrastructure.digital_twin_integration_is_missing", "InfrastructureOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class InfraKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.infrastructure.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.infrastructure.knowledge_graph_integration_is_missing", "QuantumInfrastructureHealthObservedEvent")
    def is_missing(self)->bool: return not self.present
