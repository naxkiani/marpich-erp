"""P215-Z aggregates — supreme intelligence / master control / enterprise brain invariants."""
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
class QuantumSupremeCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.quantum_master_intelligence_architecture_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "quantum.supreme.quantum_master_intelligence_architecture_is_missing", "SupremeCoreActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumMasterControlRoot(AggregateRoot):
    tenant_id: str; control_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.supreme_control_plane_is_missing")
        return _mk(cls, tenant_id, "control_ref", control_ref, "quantum.supreme.supreme_control_plane_is_missing", "IntelligenceUnifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EnterpriseBrainRoot(AggregateRoot):
    tenant_id: str; brain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, brain_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.enterprise_quantum_brain_is_missing")
        return _mk(cls, tenant_id, "brain_ref", brain_ref, "quantum.supreme.enterprise_quantum_brain_is_missing", "MasterDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousDecisionNexusRoot(AggregateRoot):
    tenant_id: str; nexus_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, nexus_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.autonomous_intelligence_nexus_is_missing")
        return _mk(cls, tenant_id, "nexus_ref", nexus_ref, "quantum.supreme.autonomous_intelligence_nexus_is_missing", "AutonomousActionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntelligenceFederationRoot(AggregateRoot):
    tenant_id: str; federation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, federation_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.intelligence_federation_is_missing")
        return _mk(cls, tenant_id, "federation_ref", federation_ref, "quantum.supreme.intelligence_federation_is_missing", "IntelligenceUnifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EvolutionIntelligenceRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.evolution_intelligence_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.supreme.evolution_intelligence_is_missing", "EvolutionExpansionDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupremeTrustGovernanceRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.trust_architecture_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "quantum.supreme.trust_architecture_is_missing", "TrustValidationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupremeKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.supreme.knowledge_graph_integration_is_missing", "IntelligenceUnifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SupremeDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.supreme.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.supreme.digital_twin_integration_is_missing", "EvolutionCycleCompletedEvent")
    def is_missing(self)->bool: return not self.present
