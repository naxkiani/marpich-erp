"""P215-U aggregates — autonomous intelligence / self-healing / evolution invariants."""
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
class QuantumAutonomousIntelligenceRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.quantum_autonomous_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "quantum.evolution.quantum_autonomous_intelligence_platform_is_missing", "AutonomousDecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SelfHealingEcosystemRoot(AggregateRoot):
    tenant_id: str; healing_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, healing_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.self_healing_ecosystem_is_missing")
        return _mk(cls, tenant_id, "healing_ref", healing_ref, "quantum.evolution.self_healing_ecosystem_is_missing", "HealingProcessStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousAgentsRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.autonomous_agents_is_missing")
        return _mk(cls, tenant_id, "agent_ref", agent_ref, "quantum.evolution.autonomous_agents_is_missing", "AutonomousDecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionIntelligenceRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.evolution_intelligence_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.evolution.evolution_intelligence_is_missing", "EvolutionCycleCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SingularityReadinessRoot(AggregateRoot):
    tenant_id: str; singularity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, singularity_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.singularity_readiness_framework_is_missing")
        return _mk(cls, tenant_id, "singularity_ref", singularity_ref, "quantum.evolution.singularity_readiness_framework_is_missing", "SingularityAssessmentCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SelfOptimizationRoot(AggregateRoot):
    tenant_id: str; optimization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, optimization_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.self_optimization_is_missing")
        return _mk(cls, tenant_id, "optimization_ref", optimization_ref, "quantum.evolution.self_optimization_is_missing", "OptimizationExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.evolution.knowledge_graph_integration_is_missing", "CapabilityUpgradeDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.evolution.digital_twin_integration_is_missing", "EvolutionCycleCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousGovernanceEvolutionRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.evolution.autonomous_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.evolution.autonomous_governance_is_missing", "AutonomousDecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present
