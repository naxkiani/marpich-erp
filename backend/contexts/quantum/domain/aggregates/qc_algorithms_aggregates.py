"""P215-E aggregates — quantum algorithm/software invariants."""
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
class AlgorithmPlatformRoot(AggregateRoot):
    tenant_id: str; algorithm_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, algorithm_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.quantum_algorithm_platform_is_missing")
        return _mk(cls, tenant_id, "algorithm_ref", algorithm_ref, "quantum.algorithms.quantum_algorithm_platform_is_missing", "QuantumAlgorithmCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SoftwarePlatformRoot(AggregateRoot):
    tenant_id: str; software_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, software_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.quantum_software_platform_is_missing")
        return _mk(cls, tenant_id, "software_ref", software_ref, "quantum.algorithms.quantum_software_platform_is_missing", "SoftwarePublishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ProgrammingEnvironmentRoot(AggregateRoot):
    tenant_id: str; programming_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, programming_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.quantum_programming_environment_is_missing")
        return _mk(cls, tenant_id, "programming_ref", programming_ref, "quantum.algorithms.quantum_programming_environment_is_missing", "ProgramCompiledEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class CircuitIntelligenceRoot(AggregateRoot):
    tenant_id: str; circuit_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, circuit_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.circuit_intelligence_engine_is_missing")
        return _mk(cls, tenant_id, "circuit_ref", circuit_ref, "quantum.algorithms.circuit_intelligence_engine_is_missing", "CircuitOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class OptimizationPlatformRoot(AggregateRoot):
    tenant_id: str; optimization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, optimization_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.optimization_platform_is_missing")
        return _mk(cls, tenant_id, "optimization_ref", optimization_ref, "quantum.algorithms.optimization_platform_is_missing", "OptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SoftwareLifecycleRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.software_lifecycle_management_is_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "quantum.algorithms.software_lifecycle_management_is_missing", "QuantumSoftwarePublishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AlgorithmRepositoryRoot(AggregateRoot):
    tenant_id: str; repository_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, repository_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.algorithm_repository_is_missing")
        return _mk(cls, tenant_id, "repository_ref", repository_ref, "quantum.algorithms.algorithm_repository_is_missing", "QuantumAlgorithmCatalogedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class MarketplaceRoot(AggregateRoot):
    tenant_id: str; marketplace_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, marketplace_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.quantum_marketplace_is_missing")
        return _mk(cls, tenant_id, "marketplace_ref", marketplace_ref, "quantum.algorithms.quantum_marketplace_is_missing", "SoftwarePublishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AlgorithmsTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.algorithms.digital_twin_integration_is_missing", "QuantumExecutionImprovedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AlgorithmsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.algorithms.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.algorithms.knowledge_graph_integration_is_missing", "QuantumAlgorithmCatalogedEvent")
    def is_missing(self)->bool: return not self.present
