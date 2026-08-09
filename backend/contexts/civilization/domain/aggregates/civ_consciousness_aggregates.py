"""P219-Q aggregates — civilization consciousness intelligence core invariants."""
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
class CivilizationConsciousnessIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; consciousness_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, consciousness_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.civilization_consciousness_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "consciousness_ref", consciousness_ref,
            "civilization.consciousness.civilization_consciousness_intelligence_platform_is_missing",
            "AwarenessExpandedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveConsciousnessNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.collective_consciousness_network_is_missing")
        return _mk(
            cls, tenant_id, "network_ref", network_ref,
            "civilization.consciousness.collective_consciousness_network_is_missing",
            "ContextUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WisdomIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; wisdom_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, wisdom_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.wisdom_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "wisdom_ref", wisdom_ref,
            "civilization.consciousness.wisdom_intelligence_platform_is_missing",
            "WisdomCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationAwarenessPlatformRoot(AggregateRoot):
    tenant_id: str; awareness_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, awareness_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.civilization_awareness_platform_is_missing")
        return _mk(
            cls, tenant_id, "awareness_ref", awareness_ref,
            "civilization.consciousness.civilization_awareness_platform_is_missing",
            "CivilizationStateUpdatedEvent",
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
            raise ValueError("civilization.consciousness.collective_learning_platform_is_missing")
        return _mk(
            cls, tenant_id, "learning_ref", learning_ref,
            "civilization.consciousness.collective_learning_platform_is_missing",
            "KnowledgeIntegratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.civilization_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.consciousness.civilization_digital_twin_is_missing",
            "EvolutionCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationConsciousnessIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.meos_civilization_consciousness_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.consciousness.meos_civilization_consciousness_intelligence_core_is_missing",
            "ReflectionCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.civilization_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.consciousness.civilization_knowledge_graph_is_missing",
            "InsightGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ConsciousnessEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.consciousness.consciousness_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.consciousness.consciousness_event_architecture_is_missing",
            "RecommendationIssuedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
