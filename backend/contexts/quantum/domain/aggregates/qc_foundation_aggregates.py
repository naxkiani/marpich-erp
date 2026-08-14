"""P215-A aggregates — quantum foundation invariants."""
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
class QuantumPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.enterprise_quantum_computing_foundation_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "quantum.foundation.enterprise_quantum_computing_foundation_is_missing", "QuantumPlatformCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumAIRoot(AggregateRoot):
    tenant_id: str; qai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, qai_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.quantum_ai_platform_is_missing")
        return _mk(cls, tenant_id, "qai_ref", qai_ref, "quantum.foundation.quantum_ai_platform_is_missing", "QuantumAIModelCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class HybridComputingRoot(AggregateRoot):
    tenant_id: str; hybrid_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hybrid_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.hybrid_computing_architecture_is_missing")
        return _mk(cls, tenant_id, "hybrid_ref", hybrid_ref, "quantum.foundation.hybrid_computing_architecture_is_missing", "CapabilityExpandedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AlgorithmFactoryRoot(AggregateRoot):
    tenant_id: str; algorithm_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, algorithm_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.quantum_algorithm_platform_is_missing")
        return _mk(cls, tenant_id, "algorithm_ref", algorithm_ref, "quantum.foundation.quantum_algorithm_platform_is_missing", "AlgorithmRegisteredEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SimulationRoot(AggregateRoot):
    tenant_id: str; simulation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, simulation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.quantum_simulation_platform_is_missing")
        return _mk(cls, tenant_id, "simulation_ref", simulation_ref, "quantum.foundation.quantum_simulation_platform_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ResearchRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.quantum_research_platform_is_missing")
        return _mk(cls, tenant_id, "research_ref", research_ref, "quantum.foundation.quantum_research_platform_is_missing", "ExperimentExecutedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.foundation.quantum_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.foundation.quantum_digital_twin_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present
