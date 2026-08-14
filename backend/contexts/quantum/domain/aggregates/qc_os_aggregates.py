"""P215-T aggregates — quantum OS / control plane / intelligence core invariants."""
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
class QuantumOperatingSystemRoot(AggregateRoot):
    tenant_id: str; os_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, os_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.quantum_operating_system_is_missing")
        return _mk(cls, tenant_id, "os_ref", os_ref, "quantum.os.quantum_operating_system_is_missing", "QuantumSystemStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumControlPlaneRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.quantum_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_ref", control_ref, "quantum.os.quantum_control_plane_is_missing", "PolicyExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.autonomous_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.os.autonomous_governance_is_missing", "AutonomousDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.quantum_intelligence_core_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "quantum.os.quantum_intelligence_core_is_missing", "AutonomousDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResourceOrchestrationRoot(AggregateRoot):
    tenant_id: str; orchestration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, orchestration_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.resource_orchestration_is_missing")
        return _mk(cls, tenant_id, "orchestration_ref", orchestration_ref, "quantum.os.resource_orchestration_is_missing", "ResourceAllocatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PolicyEngineBindingRoot(AggregateRoot):
    tenant_id: str; policy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.policy_engine_is_missing")
        return _mk(cls, tenant_id, "policy_ref", policy_ref, "quantum.os.policy_engine_is_missing", "PolicyExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AgentManagementRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.agent_management_is_missing")
        return _mk(cls, tenant_id, "agent_ref", agent_ref, "quantum.os.agent_management_is_missing", "AutonomousDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.os.knowledge_graph_integration_is_missing", "ResourceAllocatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.os.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.os.digital_twin_integration_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present
