"""P219-W aggregates — collective intelligence & global coordination invariants."""
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
class CollectiveIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; collective_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collective_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.collective_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "collective_ref", collective_ref,
            "civilization.collective.collective_intelligence_platform_is_missing",
            "CommunityCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalCoordinationPlatformRoot(AggregateRoot):
    tenant_id: str; coord_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, coord_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.global_coordination_platform_is_missing")
        return _mk(
            cls, tenant_id, "coord_ref", coord_ref,
            "civilization.collective.global_coordination_platform_is_missing",
            "CoordinationStartedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeCollaborationPlatformRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.knowledge_collaboration_platform_is_missing")
        return _mk(
            cls, tenant_id, "knowledge_ref", knowledge_ref,
            "civilization.collective.knowledge_collaboration_platform_is_missing",
            "KnowledgeSharedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ConsensusDecisionSupportPlatformRoot(AggregateRoot):
    tenant_id: str; consensus_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, consensus_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.consensus_decision_support_platform_is_missing")
        return _mk(
            cls, tenant_id, "consensus_ref", consensus_ref,
            "civilization.collective.consensus_decision_support_platform_is_missing",
            "RecommendationGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CoordinationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.coordination_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.collective.coordination_digital_twin_is_missing",
            "CoordinationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCollectiveIntelligenceGlobalCoordinationCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.meos_collective_intelligence_global_coordination_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.collective.meos_collective_intelligence_global_coordination_core_is_missing",
            "DecisionSupportedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.collective_intelligence_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.collective.collective_intelligence_knowledge_graph_is_missing",
            "KnowledgeGraphUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.collective_intelligence_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.collective.collective_intelligence_event_architecture_is_missing",
            "InsightCapturedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveLearningPlatformRoot(AggregateRoot):
    tenant_id: str; learning_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.collective.collective_learning_platform_is_missing")
        return _mk(
            cls, tenant_id, "learning_ref", learning_ref,
            "civilization.collective.collective_learning_platform_is_missing",
            "LearningCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present

