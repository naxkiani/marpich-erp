"""P219-I aggregates — knowledge civilization core invariants."""
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
class MeosKnowledgeCivilizationPlatformRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.meos_knowledge_civilization_platform_is_missing")
        return _mk(
            cls, tenant_id, "knowledge_ref", knowledge_ref,
            "civilization.knowledge.meos_knowledge_civilization_platform_is_missing",
            "KnowledgeCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class UniversalKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; ukg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ukg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.universal_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "ukg_ref", ukg_ref,
            "civilization.knowledge.universal_knowledge_graph_is_missing",
            "KnowledgeConnectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ScientificIntelligenceNetworkRoot(AggregateRoot):
    tenant_id: str; scientific_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, scientific_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.scientific_intelligence_network_is_missing")
        return _mk(
            cls, tenant_id, "scientific_ref", scientific_ref,
            "civilization.knowledge.scientific_intelligence_network_is_missing",
            "BreakthroughDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveIntelligenceArchitectureRoot(AggregateRoot):
    tenant_id: str; collective_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collective_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.collective_intelligence_architecture_is_missing")
        return _mk(
            cls, tenant_id, "collective_ref", collective_ref,
            "civilization.knowledge.collective_intelligence_architecture_is_missing",
            "CollectiveInsightGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeReasoningEngineRoot(AggregateRoot):
    tenant_id: str; reasoning_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.knowledge_reasoning_engine_is_missing")
        return _mk(
            cls, tenant_id, "reasoning_ref", reasoning_ref,
            "civilization.knowledge.knowledge_reasoning_engine_is_missing",
            "KnowledgeValidatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationLearningFoundationRoot(AggregateRoot):
    tenant_id: str; learning_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.civilization_learning_foundation_is_missing")
        return _mk(
            cls, tenant_id, "learning_ref", learning_ref,
            "civilization.knowledge.civilization_learning_foundation_is_missing",
            "LearningPathCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosKnowledgeCivilizationCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.meos_knowledge_civilization_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.knowledge.meos_knowledge_civilization_core_is_missing",
            "KnowledgeExpandedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.knowledge_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.knowledge.knowledge_digital_twin_is_missing",
            "DiscoveryGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.knowledge.knowledge_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.knowledge.knowledge_event_architecture_is_missing",
            "IntelligenceNetworkExpandedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
