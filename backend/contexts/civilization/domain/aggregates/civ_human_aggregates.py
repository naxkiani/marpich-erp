"""P219-J aggregates — human civilization intelligence core invariants."""
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
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class HumanIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; human_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, human_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "human_ref", human_ref,
            "civilization.human.human_intelligence_platform_is_missing",
            "HumanCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanDigitalTwinPlatformRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_digital_twin_platform_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.human.human_digital_twin_platform_is_missing",
            "TwinSynchronizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanDevelopmentIntelligenceRoot(AggregateRoot):
    tenant_id: str; development_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, development_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_development_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "development_ref", development_ref,
            "civilization.human.human_development_intelligence_is_missing",
            "RecommendationGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WorkforceIntelligenceRoot(AggregateRoot):
    tenant_id: str; workforce_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, workforce_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.workforce_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "workforce_ref", workforce_ref,
            "civilization.human.workforce_intelligence_is_missing",
            "PredictionGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanCapabilityIntelligenceRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_capability_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "capability_ref", capability_ref,
            "civilization.human.human_capability_intelligence_is_missing",
            "CapabilityImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.human.human_knowledge_graph_is_missing",
            "AchievementRecordedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosHumanCivilizationIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.meos_human_civilization_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.human.meos_human_civilization_intelligence_core_is_missing",
            "HumanUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanWellbeingIntelligenceRoot(AggregateRoot):
    tenant_id: str; wellbeing_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, wellbeing_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_wellbeing_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "wellbeing_ref", wellbeing_ref,
            "civilization.human.human_wellbeing_intelligence_is_missing",
            "LearningCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.human.human_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.human.human_event_architecture_is_missing",
            "SimulationExecutedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
