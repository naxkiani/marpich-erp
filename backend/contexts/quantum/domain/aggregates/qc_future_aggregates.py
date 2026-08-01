"""P215-X aggregates — future / post-QGI / singularity evolution invariants."""
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
class FutureArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.future_quantum_architecture_platform_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "quantum.future.future_quantum_architecture_platform_is_missing", "FutureArchitectureCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PostQGIEvolutionRoot(AggregateRoot):
    tenant_id: str; post_qgi_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, post_qgi_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.post_qgi_evolution_framework_is_missing")
        return _mk(cls, tenant_id, "post_qgi_ref", post_qgi_ref, "quantum.future.post_qgi_evolution_framework_is_missing", "IntelligenceExpansionTriggeredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumSingularityEvolutionRoot(AggregateRoot):
    tenant_id: str; singularity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, singularity_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.singularity_evolution_engine_is_missing")
        return _mk(cls, tenant_id, "singularity_ref", singularity_ref, "quantum.future.singularity_evolution_engine_is_missing", "SingularityMilestoneReachedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureScenarioRoot(AggregateRoot):
    tenant_id: str; scenario_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scenario_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.future_scenario_simulator_is_missing")
        return _mk(cls, tenant_id, "scenario_ref", scenario_ref, "quantum.future.future_scenario_simulator_is_missing", "EvolutionScenarioGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntelligenceExpansionRoot(AggregateRoot):
    tenant_id: str; expansion_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, expansion_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.intelligence_expansion_platform_is_missing")
        return _mk(cls, tenant_id, "expansion_ref", expansion_ref, "quantum.future.intelligence_expansion_platform_is_missing", "CapabilityExpansionDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MEOSEvolutionGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.meos_evolution_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.future.meos_evolution_governance_is_missing", "SingularityProgressUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.future.knowledge_graph_integration_is_missing", "FutureCapabilityDiscoveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.future.digital_twin_integration_is_missing", "FutureTransformationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ArchitectureSimulatorRoot(AggregateRoot):
    tenant_id: str; simulator_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, simulator_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.future.future_architecture_simulator_is_missing")
        return _mk(cls, tenant_id, "simulator_ref", simulator_ref, "quantum.future.future_architecture_simulator_is_missing", "EvolutionScenarioCompletedEvent")
    def is_missing(self)->bool: return not self.present
