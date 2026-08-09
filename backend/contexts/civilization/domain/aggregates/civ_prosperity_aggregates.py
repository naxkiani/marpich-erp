"""P219-O aggregates — civilization prosperity intelligence core invariants."""
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
class CivilizationProsperityIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; prosperity_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, prosperity_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.civilization_prosperity_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "prosperity_ref", prosperity_ref,
            "civilization.prosperity.civilization_prosperity_intelligence_platform_is_missing",
            "ProsperityImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalQualityOfLifeIntelligenceRoot(AggregateRoot):
    tenant_id: str; qol_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, qol_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.global_quality_of_life_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "qol_ref", qol_ref,
            "civilization.prosperity.global_quality_of_life_intelligence_is_missing",
            "QualityOfLifeUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanFlourishingPlatformRoot(AggregateRoot):
    tenant_id: str; flourishing_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, flourishing_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.human_flourishing_platform_is_missing")
        return _mk(
            cls, tenant_id, "flourishing_ref", flourishing_ref,
            "civilization.prosperity.human_flourishing_platform_is_missing",
            "FlourishingMilestoneReachedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OpportunityIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; opportunity_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, opportunity_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.opportunity_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "opportunity_ref", opportunity_ref,
            "civilization.prosperity.opportunity_intelligence_platform_is_missing",
            "OpportunityMatchedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ProsperityOptimizationEngineRoot(AggregateRoot):
    tenant_id: str; optimization_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, optimization_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.prosperity_optimization_engine_is_missing")
        return _mk(
            cls, tenant_id, "optimization_ref", optimization_ref,
            "civilization.prosperity.prosperity_optimization_engine_is_missing",
            "ProsperityMeasuredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ProsperityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.prosperity_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.prosperity.prosperity_digital_twin_is_missing",
            "CommunityDevelopedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationProsperityIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.meos_civilization_prosperity_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.prosperity.meos_civilization_prosperity_intelligence_core_is_missing",
            "CapabilityImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ProsperityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.prosperity_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.prosperity.prosperity_knowledge_graph_is_missing",
            "OpportunityDiscoveredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ProsperityEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.prosperity.prosperity_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.prosperity.prosperity_event_architecture_is_missing",
            "SocialProgramCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
