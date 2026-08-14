"""P217-W aggregates — biotechnology bio civilization invariants."""
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
class BioCivilizationIntelligenceRoot(AggregateRoot):
    tenant_id: str; civilization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.bio_civilization_intelligence_layer_is_missing")
        return _mk(cls, tenant_id, "civilization_ref", civilization_ref, "biotechnology.bio_civilization.bio_civilization_intelligence_layer_is_missing", "BioCivilizationPlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollectiveBiologicalNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.collective_biological_intelligence_network_is_missing")
        return _mk(cls, tenant_id, "network_ref", network_ref, "biotechnology.bio_civilization.collective_biological_intelligence_network_is_missing", "CollectiveNetworkExpandedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GlobalBioCognitiveEcosystemRoot(AggregateRoot):
    tenant_id: str; ecosystem_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ecosystem_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.global_bio_cognitive_ecosystem_is_missing")
        return _mk(cls, tenant_id, "ecosystem_ref", ecosystem_ref, "biotechnology.bio_civilization.global_bio_cognitive_ecosystem_is_missing", "CognitiveEcosystemUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanBioAiSymbiosisRoot(AggregateRoot):
    tenant_id: str; symbiosis_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, symbiosis_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.human_bio_ai_symbiosis_framework_is_missing")
        return _mk(cls, tenant_id, "symbiosis_ref", symbiosis_ref, "biotechnology.bio_civilization.human_bio_ai_symbiosis_framework_is_missing", "SymbiosisSessionRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeCivilizationRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.knowledge_civilization_platform_is_missing")
        return _mk(cls, tenant_id, "knowledge_ref", knowledge_ref, "biotechnology.bio_civilization.knowledge_civilization_platform_is_missing", "KnowledgeContributionRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MultiAgentBioSocietyRoot(AggregateRoot):
    tenant_id: str; society_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, society_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.multi_agent_bio_society_is_missing")
        return _mk(cls, tenant_id, "society_ref", society_ref, "biotechnology.bio_civilization.multi_agent_bio_society_is_missing", "CollectiveNetworkExpandedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollectiveBioDecisionRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.collective_bio_decision_intelligence_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "biotechnology.bio_civilization.collective_bio_decision_intelligence_is_missing", "CollectiveBioDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CivilizationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.civilization_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "biotechnology.bio_civilization.civilization_knowledge_graph_is_missing", "KnowledgeContributionRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioCivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.bio_civilization.digital_twin_integration_is_missing", "CognitiveEcosystemUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanCivilizationOversightRoot(AggregateRoot):
    tenant_id: str; oversight_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, oversight_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.human_civilization_oversight_is_missing")
        return _mk(cls, tenant_id, "oversight_ref", oversight_ref, "biotechnology.bio_civilization.human_civilization_oversight_is_missing", "CivilizationEthicsReviewRequiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class BioCivilizationSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.bio_civilization.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.bio_civilization.security_architecture_is_missing", "CivilizationGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
