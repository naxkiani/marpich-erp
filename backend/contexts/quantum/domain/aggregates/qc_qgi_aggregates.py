"""P215-V aggregates — QGI / cognitive enterprise / reasoning invariants."""
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
class QuantumGeneralIntelligenceRoot(AggregateRoot):
    tenant_id: str; qgi_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, qgi_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.quantum_general_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "qgi_ref", qgi_ref, "quantum.qgi.quantum_general_intelligence_platform_is_missing", "CognitiveReasoningStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CognitiveEnterpriseBrainRoot(AggregateRoot):
    tenant_id: str; brain_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, brain_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.cognitive_enterprise_brain_is_missing")
        return _mk(cls, tenant_id, "brain_ref", brain_ref, "quantum.qgi.cognitive_enterprise_brain_is_missing", "DecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AdvancedReasoningEngineRoot(AggregateRoot):
    tenant_id: str; reasoning_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.advanced_reasoning_engine_is_missing")
        return _mk(cls, tenant_id, "reasoning_ref", reasoning_ref, "quantum.qgi.advanced_reasoning_engine_is_missing", "ReasoningCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeUnderstandingRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.knowledge_understanding_layer_is_missing")
        return _mk(cls, tenant_id, "knowledge_ref", knowledge_ref, "quantum.qgi.knowledge_understanding_layer_is_missing", "KnowledgeIntegratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CognitiveAgentNetworkRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.cognitive_agent_network_is_missing")
        return _mk(cls, tenant_id, "agent_ref", agent_ref, "quantum.qgi.cognitive_agent_network_is_missing", "DecisionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EnterpriseMemoryRoot(AggregateRoot):
    tenant_id: str; memory_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.enterprise_memory_platform_is_missing")
        return _mk(cls, tenant_id, "memory_ref", memory_ref, "quantum.qgi.enterprise_memory_platform_is_missing", "KnowledgeIntegratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IntelligenceEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.intelligence_evolution_framework_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "quantum.qgi.intelligence_evolution_framework_is_missing", "CognitiveCapabilityExpandedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QgiKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.qgi.knowledge_graph_integration_is_missing", "KnowledgeIntegratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class QgiDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qgi.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.qgi.digital_twin_integration_is_missing", "LearningCompletedEvent")
    def is_missing(self)->bool: return not self.present
