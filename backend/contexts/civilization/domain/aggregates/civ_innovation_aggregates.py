"""P219-L aggregates — civilization innovation intelligence core invariants."""
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
class CivilizationInnovationIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; innovation_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, innovation_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.civilization_innovation_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "innovation_ref", innovation_ref,
            "civilization.innovation.civilization_innovation_intelligence_platform_is_missing",
            "InnovationCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalInnovationNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.global_innovation_network_is_missing")
        return _mk(
            cls, tenant_id, "network_ref", network_ref,
            "civilization.innovation.global_innovation_network_is_missing",
            "CollaborationCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TechnologyEvolutionPlatformRoot(AggregateRoot):
    tenant_id: str; technology_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, technology_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.technology_evolution_platform_is_missing")
        return _mk(
            cls, tenant_id, "technology_ref", technology_ref,
            "civilization.innovation.technology_evolution_platform_is_missing",
            "TechnologyForecastUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResearchIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; research_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.research_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "research_ref", research_ref,
            "civilization.innovation.research_intelligence_platform_is_missing",
            "ResearchInitiatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InnovationPortfolioIntelligenceRoot(AggregateRoot):
    tenant_id: str; portfolio_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, portfolio_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.innovation_portfolio_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "portfolio_ref", portfolio_ref,
            "civilization.innovation.innovation_portfolio_intelligence_is_missing",
            "InnovationValidatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InnovationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.innovation_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.innovation.innovation_digital_twin_is_missing",
            "DisruptionDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationInnovationIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.meos_civilization_innovation_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.innovation.meos_civilization_innovation_intelligence_core_is_missing",
            "InnovationScaledEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InnovationKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.innovation_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.innovation.innovation_knowledge_graph_is_missing",
            "KnowledgeSharedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InnovationEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.innovation.innovation_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.innovation.innovation_event_architecture_is_missing",
            "BreakthroughDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
