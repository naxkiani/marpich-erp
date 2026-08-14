"""P219-R aggregates — civilization evolution intelligence core invariants."""
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
class CivilizationEvolutionIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.civilization_evolution_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "evolution_ref", evolution_ref,
            "civilization.evolution.civilization_evolution_intelligence_platform_is_missing",
            "EvolutionMeasuredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AdaptiveCivilizationEvolutionPlatformRoot(AggregateRoot):
    tenant_id: str; adaptive_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, adaptive_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.adaptive_civilization_evolution_platform_is_missing")
        return _mk(
            cls, tenant_id, "adaptive_ref", adaptive_ref,
            "civilization.evolution.adaptive_civilization_evolution_platform_is_missing",
            "AdaptationTriggeredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LongTermStrategyPlatformRoot(AggregateRoot):
    tenant_id: str; strategy_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, strategy_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.long_term_strategy_platform_is_missing")
        return _mk(
            cls, tenant_id, "strategy_ref", strategy_ref,
            "civilization.evolution.long_term_strategy_platform_is_missing",
            "RoadmapPublishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FutureScenarioEngineRoot(AggregateRoot):
    tenant_id: str; scenario_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, scenario_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.future_scenario_engine_is_missing")
        return _mk(
            cls, tenant_id, "scenario_ref", scenario_ref,
            "civilization.evolution.future_scenario_engine_is_missing",
            "ScenarioGeneratedEvent",
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
            raise ValueError("civilization.evolution.evolution_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.evolution.evolution_digital_twin_is_missing",
            "SimulationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionOptimizationFrameworkRoot(AggregateRoot):
    tenant_id: str; optimization_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, optimization_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.evolution_optimization_framework_is_missing")
        return _mk(
            cls, tenant_id, "optimization_ref", optimization_ref,
            "civilization.evolution.evolution_optimization_framework_is_missing",
            "OptimizationFinishedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationEvolutionIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.meos_civilization_evolution_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.evolution.meos_civilization_evolution_intelligence_core_is_missing",
            "TransformationInitiatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.evolution_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.evolution.evolution_knowledge_graph_is_missing",
            "TrendDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.evolution.evolution_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.evolution.evolution_event_architecture_is_missing",
            "KnowledgeIntegratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
