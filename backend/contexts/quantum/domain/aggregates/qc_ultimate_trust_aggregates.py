"""P215-Y aggregates — ultimate governance / alignment / ethics / trust invariants."""
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
class QuantumUltimateGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.ultimate_quantum_governance_platform_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "quantum.ultimate_trust.ultimate_quantum_governance_platform_is_missing", "GovernanceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntelligenceAlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.intelligence_alignment_framework_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "quantum.ultimate_trust.intelligence_alignment_framework_is_missing", "AlignmentVerifiedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumEthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.quantum_ethics_civilization_layer_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "quantum.ultimate_trust.quantum_ethics_civilization_layer_is_missing", "EthicsApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QuantumTrustAssuranceRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.trust_architecture_platform_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "quantum.ultimate_trust.trust_architecture_platform_is_missing", "TrustEstablishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernanceEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.governance_evolution_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.ultimate_trust.governance_evolution_is_missing", "GovernancePolicyCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernanceAssuranceRoot(AggregateRoot):
    tenant_id: str; assurance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, assurance_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.autonomous_governance_assurance_is_missing")
        return _mk(cls, tenant_id, "assurance_ref", assurance_ref, "quantum.ultimate_trust.autonomous_governance_assurance_is_missing", "GovernanceDeviationDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateTrustKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.ultimate_trust.knowledge_graph_integration_is_missing", "GovernanceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class UltimateGovernanceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.ultimate_trust.digital_twin_integration_is_missing", "AlignmentRecoveryCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResponsibleIntelligenceRoot(AggregateRoot):
    tenant_id: str; responsible_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, responsible_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.ultimate_trust.responsible_intelligence_framework_is_missing")
        return _mk(cls, tenant_id, "responsible_ref", responsible_ref, "quantum.ultimate_trust.responsible_intelligence_framework_is_missing", "EthicsValidationCompletedEvent")
    def is_missing(self)->bool: return not self.present
