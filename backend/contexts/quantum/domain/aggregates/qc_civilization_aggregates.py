"""P215-W aggregates — civilization / collective intelligence invariants."""
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
class QuantumCivilizationIntelligenceRoot(AggregateRoot):
    tenant_id: str; civilization_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.quantum_civilization_intelligence_layer_is_missing")
        return _mk(cls, tenant_id, "civilization_ref", civilization_ref, "quantum.civilization.quantum_civilization_intelligence_layer_is_missing", "CollectiveIntelligenceCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.collective_intelligence_network_is_missing")
        return _mk(cls, tenant_id, "network_ref", network_ref, "quantum.civilization.collective_intelligence_network_is_missing", "IntelligenceNodeConnectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GlobalCognitiveEcosystemRoot(AggregateRoot):
    tenant_id: str; ecosystem_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ecosystem_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.global_cognitive_ecosystem_is_missing")
        return _mk(cls, tenant_id, "ecosystem_ref", ecosystem_ref, "quantum.civilization.global_cognitive_ecosystem_is_missing", "CognitiveNetworkExpandedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeCivilizationRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.knowledge_civilization_platform_is_missing")
        return _mk(cls, tenant_id, "knowledge_ref", knowledge_ref, "quantum.civilization.knowledge_civilization_platform_is_missing", "KnowledgeSharedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MultiAgentIntelligenceSocietyRoot(AggregateRoot):
    tenant_id: str; society_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, society_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.multi_agent_intelligence_society_is_missing")
        return _mk(cls, tenant_id, "society_ref", society_ref, "quantum.civilization.multi_agent_intelligence_society_is_missing", "CognitiveNetworkExpandedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CollectiveDecisionIntelligenceRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.collective_decision_intelligence_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "quantum.civilization.collective_decision_intelligence_is_missing", "CollectiveDecisionCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FutureIntelligenceEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.future_intelligence_evolution_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.civilization.future_intelligence_evolution_is_missing", "CivilizationCapabilityEvolvedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CivilizationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.civilization.knowledge_graph_integration_is_missing", "KnowledgeSharedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.civilization.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.civilization.digital_twin_integration_is_missing", "FutureMilestoneReachedEvent")
    def is_missing(self)->bool: return not self.present
