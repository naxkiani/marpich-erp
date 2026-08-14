"""P214-X aggregates - future-evolution invariants."""
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
        if not present: raise ValueError("ai.futurearch.future_ai_architecture_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "ai.futurearch.future_ai_architecture_is_missing", "FutureArchitectureCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class PostAGIRoot(AggregateRoot):
    tenant_id: str; post_agi_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, post_agi_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.post_agi_intelligence_framework_is_missing")
        return _mk(cls, tenant_id, "post_agi_ref", post_agi_ref, "ai.futurearch.post_agi_intelligence_framework_is_missing", "PostAGIActivatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class CognitiveArchitectureRoot(AggregateRoot):
    tenant_id: str; cognitive_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cognitive_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.advanced_cognitive_architecture_is_missing")
        return _mk(cls, tenant_id, "cognitive_ref", cognitive_ref, "ai.futurearch.advanced_cognitive_architecture_is_missing", "CapabilityExpandedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SuperintelligenceGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.superintelligence_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "ai.futurearch.superintelligence_governance_is_missing", "GovernanceMaturityChangedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class IntelligenceEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.intelligence_evolution_engine_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "ai.futurearch.intelligence_evolution_engine_is_missing", "EvolutionStartedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class FutureSafetyRoot(AggregateRoot):
    tenant_id: str; safety_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.future_ai_safety_architecture_is_missing")
        return _mk(cls, tenant_id, "safety_ref", safety_ref, "ai.futurearch.future_ai_safety_architecture_is_missing", "SafetyValidatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SingularityReadinessRoot(AggregateRoot):
    tenant_id: str; readiness_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, readiness_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.singularity_readiness_framework_is_missing")
        return _mk(cls, tenant_id, "readiness_ref", readiness_ref, "ai.futurearch.singularity_readiness_framework_is_missing", "ReadinessUpdatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class UltimateDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("ai.futurearch.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "ai.futurearch.digital_twin_integration_is_missing", "ReadinessUpdatedEvent")
    def is_missing(self)->bool: return not self.present
