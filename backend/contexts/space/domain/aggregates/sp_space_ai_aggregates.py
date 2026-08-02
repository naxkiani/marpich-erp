"""P218-E aggregates — space AI invariants."""
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
class SpaceAiPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.space_ai_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.space_ai.space_ai_platform_is_missing", "ModelRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FoundationModelsRoot(AggregateRoot):
    tenant_id: str; models_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, models_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.foundation_models_are_missing")
        return _mk(cls, tenant_id, "models_ref", models_ref, "space.space_ai.foundation_models_are_missing", "ModelRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceAiEngineRoot(AggregateRoot):
    tenant_id: str; engine_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, engine_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.space_ai_engine_is_missing")
        return _mk(cls, tenant_id, "engine_ref", engine_ref, "space.space_ai.space_ai_engine_is_missing", "InferenceCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionIntelligenceRoot(AggregateRoot):
    tenant_id: str; intel_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, intel_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.mission_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "intel_ref", intel_ref, "space.space_ai.mission_intelligence_platform_is_missing", "PredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousDecisionRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.autonomous_decision_platform_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "space.space_ai.autonomous_decision_platform_is_missing", "DecisionApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.multi_agent_architecture_is_missing")
        return _mk(cls, tenant_id, "agents_ref", agents_ref, "space.space_ai.multi_agent_architecture_is_missing", "AgentActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.space_ai.knowledge_graph_integration_is_missing", "InferenceCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResponsibleSpaceAiRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.ai_governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.space_ai.ai_governance_is_missing", "DecisionApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceAiSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.space_ai.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.space_ai.security_architecture_is_missing", "InferenceRequestedEvent")
    def is_missing(self)->bool: return not self.present
