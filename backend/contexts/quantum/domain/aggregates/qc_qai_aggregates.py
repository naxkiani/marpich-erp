"""P215-F aggregates — quantum AI/QML invariants."""
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
class QuantumAIPlatformRoot(AggregateRoot):
    tenant_id: str; qai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, qai_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_ai_platform_is_missing")
        return _mk(cls, tenant_id, "qai_ref", qai_ref, "quantum.qai.quantum_ai_platform_is_missing", "QuantumAIModelCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumMLPlatformRoot(AggregateRoot):
    tenant_id: str; ml_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ml_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_machine_learning_platform_is_missing")
        return _mk(cls, tenant_id, "ml_ref", ml_ref, "quantum.qai.quantum_machine_learning_platform_is_missing", "QuantumTrainingCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ModelLifecycleRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_model_lifecycle_is_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "quantum.qai.quantum_model_lifecycle_is_missing", "QuantumModelOptimizedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class NeuralIntelligenceRoot(AggregateRoot):
    tenant_id: str; neural_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, neural_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_neural_intelligence_is_missing")
        return _mk(cls, tenant_id, "neural_ref", neural_ref, "quantum.qai.quantum_neural_intelligence_is_missing", "QuantumIntelligenceExpandedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class FeatureIntelligenceRoot(AggregateRoot):
    tenant_id: str; feature_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, feature_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_feature_intelligence_is_missing")
        return _mk(cls, tenant_id, "feature_ref", feature_ref, "quantum.qai.quantum_feature_intelligence_is_missing", "QuantumFeatureSetPreparedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AIAgentFoundationRoot(AggregateRoot):
    tenant_id: str; agent_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.quantum_ai_agent_foundation_is_missing")
        return _mk(cls, tenant_id, "agent_ref", agent_ref, "quantum.qai.quantum_ai_agent_foundation_is_missing", "QuantumIntelligenceImprovedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QaiTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.qai.digital_twin_integration_is_missing", "QuantumIntelligenceImprovedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QaiKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.qai.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.qai.knowledge_graph_integration_is_missing", "QuantumAIModelCreatedEvent")
    def is_missing(self)->bool: return not self.present
