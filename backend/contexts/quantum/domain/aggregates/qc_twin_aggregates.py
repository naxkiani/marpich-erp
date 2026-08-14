"""P215-L aggregates — quantum digital twin / reality modeling invariants."""
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
class QuantumDigitalTwinPlatformRoot(AggregateRoot):
    tenant_id: str; twin_platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_platform_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.quantum_digital_twin_platform_is_missing")
        return _mk(cls, tenant_id, "twin_platform_ref", twin_platform_ref, "quantum.twin.quantum_digital_twin_platform_is_missing", "QuantumTwinCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SimulationIntelligenceRoot(AggregateRoot):
    tenant_id: str; simulation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, simulation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.quantum_simulation_intelligence_is_missing")
        return _mk(cls, tenant_id, "simulation_ref", simulation_ref, "quantum.twin.quantum_simulation_intelligence_is_missing", "SimulationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RealityModelingRoot(AggregateRoot):
    tenant_id: str; reality_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reality_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.quantum_reality_modeling_is_missing")
        return _mk(cls, tenant_id, "reality_ref", reality_ref, "quantum.twin.quantum_reality_modeling_is_missing", "RealityModelUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PredictiveIntelligenceRoot(AggregateRoot):
    tenant_id: str; prediction_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, prediction_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.predictive_intelligence_is_missing")
        return _mk(cls, tenant_id, "prediction_ref", prediction_ref, "quantum.twin.predictive_intelligence_is_missing", "PredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ScenarioSimulationRoot(AggregateRoot):
    tenant_id: str; scenario_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, scenario_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.scenario_simulation_is_missing")
        return _mk(cls, tenant_id, "scenario_ref", scenario_ref, "quantum.twin.scenario_simulation_is_missing", "ScenarioValidatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionIntelligenceRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.evolution_intelligence_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.twin.evolution_intelligence_is_missing", "EvolutionImprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TwinKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.twin.knowledge_graph_integration_is_missing", "QuantumTwinCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TwinGovernanceIntegrationRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.twin.governance_integration_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.twin.governance_integration_is_missing", "TwinOptimizedEvent")
    def is_missing(self)->bool: return not self.present
