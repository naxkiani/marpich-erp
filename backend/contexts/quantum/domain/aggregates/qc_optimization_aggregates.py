"""P215-G aggregates — quantum optimization/scientific intelligence invariants."""
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
class OptimizationPlatformRoot(AggregateRoot):
    tenant_id: str; optimization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, optimization_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.quantum_optimization_platform_is_missing")
        return _mk(cls, tenant_id, "optimization_ref", optimization_ref, "quantum.optimization.quantum_optimization_platform_is_missing", "OptimizationProblemCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SimulationPlatformRoot(AggregateRoot):
    tenant_id: str; simulation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, simulation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.simulation_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "simulation_ref", simulation_ref, "quantum.optimization.simulation_intelligence_platform_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ScientificComputingRoot(AggregateRoot):
    tenant_id: str; scientific_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scientific_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.scientific_computing_platform_is_missing")
        return _mk(cls, tenant_id, "scientific_ref", scientific_ref, "quantum.optimization.scientific_computing_platform_is_missing", "SimulationStartedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DiscoveryIntelligenceRoot(AggregateRoot):
    tenant_id: str; discovery_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, discovery_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.discovery_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "discovery_ref", discovery_ref, "quantum.optimization.discovery_intelligence_platform_is_missing", "DiscoveryGeneratedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class DecisionOptimizationRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.decision_optimization_engine_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "quantum.optimization.decision_optimization_engine_is_missing", "SolutionValidatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class OptTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.optimization.digital_twin_integration_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class OptKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.optimization.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.optimization.knowledge_graph_integration_is_missing", "ScientificDiscoveryGeneratedEvent")
    def is_missing(self)->bool: return not self.present
