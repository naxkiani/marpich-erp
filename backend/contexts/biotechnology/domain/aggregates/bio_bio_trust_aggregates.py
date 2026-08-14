"""P217-Y aggregates — biotechnology bio trust invariants."""
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
class UltimateBioGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.ultimate_bio_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.bio_trust.ultimate_bio_governance_is_missing", "BioTrustPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioIntelligenceAlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.bio_intelligence_alignment_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "biotechnology.bio_trust.bio_intelligence_alignment_is_missing", "AlignmentEvaluatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioEthicsCivilizationRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.bio_ethics_civilization_framework_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "biotechnology.bio_trust.bio_ethics_civilization_framework_is_missing", "EthicsReviewRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureBiologicalTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.future_biological_trust_architecture_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "biotechnology.bio_trust.future_biological_trust_architecture_is_missing", "TrustAttestationIssuedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TrustAssuranceRoot(AggregateRoot):
    tenant_id: str; assurance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, assurance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.trust_assurance_layer_is_missing")
        return _mk(cls, tenant_id, "assurance_ref", assurance_ref, "biotechnology.bio_trust.trust_assurance_layer_is_missing", "AlignmentEvaluatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TrustKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.trust_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_trust.trust_knowledge_graph_is_missing", "TrustPolicyPublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TrustIntelligenceAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.trust_intelligence_agents_are_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "biotechnology.bio_trust.trust_intelligence_agents_are_missing", "MisalignmentDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FinalBioTrustCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.final_bio_trust_core_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "biotechnology.bio_trust.final_bio_trust_core_is_missing", "TrustPolicyApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.bio_trust_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "biotechnology.bio_trust.bio_trust_is_missing", "TrustPolicyPublishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanTrustOversightRoot(AggregateRoot):
    tenant_id: str; oversight_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, oversight_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.human_trust_oversight_is_missing")
        return _mk(cls, tenant_id, "oversight_ref", oversight_ref, "biotechnology.bio_trust.human_trust_oversight_is_missing", "EthicsReviewRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioTrustSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_trust.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_trust.security_architecture_is_missing", "TrustGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
