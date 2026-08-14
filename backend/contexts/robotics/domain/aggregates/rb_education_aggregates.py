"""P216-Q aggregates — education robotics / smart campus invariants."""
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
class EducationRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.education_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.education.education_robotics_platform_is_missing", "RobotTeachingSessionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiLearningRoot(AggregateRoot):
    tenant_id: str; learning_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.ai_learning_platform_is_missing")
        return _mk(cls, tenant_id, "learning_ref", learning_ref, "robotics.education.ai_learning_platform_is_missing", "LearningStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartCampusRoot(AggregateRoot):
    tenant_id: str; campus_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, campus_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.smart_campus_platform_is_missing")
        return _mk(cls, tenant_id, "campus_ref", campus_ref, "robotics.education.smart_campus_platform_is_missing", "CampusOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousEducationOperationsRoot(AggregateRoot):
    tenant_id: str; operations_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, operations_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.autonomous_education_operations_is_missing")
        return _mk(cls, tenant_id, "operations_ref", operations_ref, "robotics.education.autonomous_education_operations_is_missing", "CampusOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AcademicIntelligenceRoot(AggregateRoot):
    tenant_id: str; academic_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, academic_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.academic_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "academic_ref", academic_ref, "robotics.education.academic_intelligence_platform_is_missing", "LearningOutcomeChangedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EducationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.education_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.education.education_digital_twin_is_missing", "CampusOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LearningKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.learning_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.education.learning_knowledge_graph_is_missing", "StudentRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EducationSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.education.security_architecture_is_missing", "AssessmentCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartClassroomRoot(AggregateRoot):
    tenant_id: str; classroom_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, classroom_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.education.smart_campus_platform_is_missing")
        return _mk(cls, tenant_id, "classroom_ref", classroom_ref, "robotics.education.smart_campus_platform_is_missing", "LearningStartedEvent")
    def is_missing(self)->bool: return not self.present
