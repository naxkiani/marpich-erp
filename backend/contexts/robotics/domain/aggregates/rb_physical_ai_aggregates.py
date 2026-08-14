"""P216-E aggregates — Physical AI / perception / cognitive robotics invariants."""
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
class PhysicalAIEngineRoot(AggregateRoot):
    tenant_id: str; engine_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, engine_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.physical_ai_engine_is_missing")
        return _mk(cls, tenant_id, "engine_ref", engine_ref, "robotics.physical_ai.physical_ai_engine_is_missing", "DecisionApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PerceptionPlatformRoot(AggregateRoot):
    tenant_id: str; perception_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, perception_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.robot_perception_platform_is_missing")
        return _mk(cls, tenant_id, "perception_ref", perception_ref, "robotics.physical_ai.robot_perception_platform_is_missing", "PerceptionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CognitiveRoboticsRoot(AggregateRoot):
    tenant_id: str; cognitive_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cognitive_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.cognitive_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "cognitive_ref", cognitive_ref, "robotics.physical_ai.cognitive_robotics_platform_is_missing", "DecisionApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousDecisionRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.autonomous_decision_platform_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "robotics.physical_ai.autonomous_decision_platform_is_missing", "ActionExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class WorldModelRoot(AggregateRoot):
    tenant_id: str; world_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, world_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.world_model_architecture_is_missing")
        return _mk(cls, tenant_id, "world_ref", world_ref, "robotics.physical_ai.world_model_architecture_is_missing", "EnvironmentMappedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RobotMemoryRoot(AggregateRoot):
    tenant_id: str; memory_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.robot_memory_architecture_is_missing")
        return _mk(cls, tenant_id, "memory_ref", memory_ref, "robotics.physical_ai.robot_memory_architecture_is_missing", "LearningCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LearningPlatformRoot(AggregateRoot):
    tenant_id: str; learning_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.learning_platform_is_missing")
        return _mk(cls, tenant_id, "learning_ref", learning_ref, "robotics.physical_ai.learning_platform_is_missing", "BehaviourAdaptedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ResponsibleAIRoot(AggregateRoot):
    tenant_id: str; responsible_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, responsible_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.safety_and_responsible_ai_is_missing")
        return _mk(cls, tenant_id, "responsible_ref", responsible_ref, "robotics.physical_ai.safety_and_responsible_ai_is_missing", "SafetyOverrideActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class KnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.physical_ai.knowledge_graph_integration_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.physical_ai.knowledge_graph_integration_is_missing", "LearningCompletedEvent")
    def is_missing(self)->bool: return not self.present
