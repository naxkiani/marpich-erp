"""P219-X aggregates — strategic evolution & adaptive transformation invariants."""
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
class StrategicEvolutionPlatformRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.strategic_evolution_platform_is_missing")
        return _mk(
            cls, tenant_id, "evolution_ref", evolution_ref,
            "civilization.strategic_evolution.strategic_evolution_platform_is_missing",
            "EvolutionProgramDefinedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AdaptiveTransformationPlatformRoot(AggregateRoot):
    tenant_id: str; transform_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, transform_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.adaptive_transformation_platform_is_missing")
        return _mk(
            cls, tenant_id, "transform_ref", transform_ref,
            "civilization.strategic_evolution.adaptive_transformation_platform_is_missing",
            "TransformationInitiativeDesignedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicPortfolioEvolutionPlatformRoot(AggregateRoot):
    tenant_id: str; portfolio_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, portfolio_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.strategic_portfolio_evolution_platform_is_missing")
        return _mk(
            cls, tenant_id, "portfolio_ref", portfolio_ref,
            "civilization.strategic_evolution.strategic_portfolio_evolution_platform_is_missing",
            "PortfolioAssessedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BusinessCapabilityEvolutionPlatformRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.business_capability_evolution_platform_is_missing")
        return _mk(
            cls, tenant_id, "capability_ref", capability_ref,
            "civilization.strategic_evolution.business_capability_evolution_platform_is_missing",
            "CapabilityEvolvedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnterpriseTransformationIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; intel_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, intel_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.strategic_evolution.enterprise_transformation_intelligence_platform_is_missing"
            )
        return _mk(
            cls, tenant_id, "intel_ref", intel_ref,
            "civilization.strategic_evolution.enterprise_transformation_intelligence_platform_is_missing",
            "TransformationRecommendationPublishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosStrategicEvolutionAdaptiveTransformationCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError(
                "civilization.strategic_evolution.meos_strategic_evolution_adaptive_transformation_core_is_missing"
            )
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.strategic_evolution.meos_strategic_evolution_adaptive_transformation_core_is_missing",
            "TransformationAuthorizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicEvolutionKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.strategic_evolution_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.strategic_evolution.strategic_evolution_knowledge_graph_is_missing",
            "StrategicEvolutionKnowledgeGraphUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicEvolutionEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.strategic_evolution_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.strategic_evolution.strategic_evolution_event_architecture_is_missing",
            "TransformationInsightCapturedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.strategic_evolution.evolution_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.strategic_evolution.evolution_digital_twin_is_missing",
            "TransformationImpactSimulatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
