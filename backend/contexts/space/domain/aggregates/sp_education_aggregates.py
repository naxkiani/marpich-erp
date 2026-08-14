"""P218-S aggregates — education intelligence invariants."""
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
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class EducationPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.space_education_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.education.space_education_platform_is_missing", "LearnerRegisteredEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeEconomyRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.space_knowledge_economy_is_missing")
        return _mk(cls, tenant_id, "knowledge_ref", knowledge_ref, "space.education.space_knowledge_economy_is_missing", "KnowledgePublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class TrainingSystemsRoot(AggregateRoot):
    tenant_id: str; training_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, training_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.training_systems_is_missing")
        return _mk(cls, tenant_id, "training_ref", training_ref, "space.education.training_systems_is_missing", "TrainingStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class WorkforceIntelligenceRoot(AggregateRoot):
    tenant_id: str; workforce_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, workforce_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.workforce_intelligence_is_missing")
        return _mk(cls, tenant_id, "workforce_ref", workforce_ref, "space.education.workforce_intelligence_is_missing", "TalentMatchedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class LearningAiRoot(AggregateRoot):
    tenant_id: str; learning_ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, learning_ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.learning_ai_is_missing")
        return _mk(cls, tenant_id, "learning_ai_ref", learning_ai_ref, "space.education.learning_ai_is_missing", "TrainingOptimizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SimulationPlatformRoot(AggregateRoot):
    tenant_id: str; simulation_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, simulation_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.simulation_platform_is_missing")
        return _mk(cls, tenant_id, "simulation_ref", simulation_ref, "space.education.simulation_platform_is_missing", "SimulationCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EducationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.education.knowledge_graph_is_missing", "ResearchSharedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EducationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.education_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.education.education_digital_twin_is_missing", "CareerPathUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EducationGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.education.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.education.governance_is_missing", "CertificationCompletedEvent")
    def is_missing(self) -> bool: return not self.present
