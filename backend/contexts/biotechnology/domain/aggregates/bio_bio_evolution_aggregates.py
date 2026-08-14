"""P217-X aggregates — biotechnology ultimate bio evolution invariants."""
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
class FutureBioArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.future_bio_architecture_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "biotechnology.bio_evolution.future_bio_architecture_is_missing", "BioEvolutionPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PostBiologicalIntelligenceRoot(AggregateRoot):
    tenant_id: str; intelligence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intelligence_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.post_biological_intelligence_is_missing")
        return _mk(cls, tenant_id, "intelligence_ref", intelligence_ref, "biotechnology.bio_evolution.post_biological_intelligence_is_missing", "FutureStatePredictedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanBioAiConvergenceRoot(AggregateRoot):
    tenant_id: str; convergence_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, convergence_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.human_bio_ai_convergence_is_missing")
        return _mk(cls, tenant_id, "convergence_ref", convergence_ref, "biotechnology.bio_evolution.human_bio_ai_convergence_is_missing", "ConvergenceAchievedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioSingularityFrameworkRoot(AggregateRoot):
    tenant_id: str; singularity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, singularity_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.bio_singularity_framework_is_missing")
        return _mk(cls, tenant_id, "singularity_ref", singularity_ref, "biotechnology.bio_evolution.bio_singularity_framework_is_missing", "HumanSingularityOversightRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateBioDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.ultimate_bio_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_evolution.ultimate_bio_digital_twin_is_missing", "EvolutionPathCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.evolution_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_evolution.evolution_knowledge_graph_is_missing", "FutureStatePredictedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureIntelligenceAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.future_intelligence_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_evolution.future_intelligence_agents_are_missing", "EvolutionPathCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.bio_evolution_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "biotechnology.bio_evolution.bio_evolution_is_missing", "EvolutionPathCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateBioGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.ultimate_bio_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_evolution.ultimate_bio_governance_is_missing", "SingularityGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ConvergenceSafetyRoot(AggregateRoot):
    tenant_id: str; safety_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.convergence_safety_is_missing")
        return _mk(cls, tenant_id, "safety_ref", safety_ref, "biotechnology.bio_evolution.convergence_safety_is_missing", "SafetyReviewRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioEvolutionSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_evolution.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_evolution.security_architecture_is_missing", "SingularityGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
