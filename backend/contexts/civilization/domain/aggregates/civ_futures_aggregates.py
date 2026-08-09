"""P219-S aggregates — civilization futures intelligence core invariants."""
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
class CivilizationFuturesIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; futures_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, futures_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.civilization_futures_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "futures_ref", futures_ref,
            "civilization.futures.civilization_futures_intelligence_platform_is_missing",
            "TrendDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicForesightEngineRoot(AggregateRoot):
    tenant_id: str; foresight_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, foresight_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.strategic_foresight_engine_is_missing")
        return _mk(
            cls, tenant_id, "foresight_ref", foresight_ref,
            "civilization.futures.strategic_foresight_engine_is_missing",
            "ForecastGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HorizonScanningPlatformRoot(AggregateRoot):
    tenant_id: str; horizon_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, horizon_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.horizon_scanning_platform_is_missing")
        return _mk(
            cls, tenant_id, "horizon_ref", horizon_ref,
            "civilization.futures.horizon_scanning_platform_is_missing",
            "SignalClassifiedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ScenarioIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; scenario_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, scenario_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.scenario_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "scenario_ref", scenario_ref,
            "civilization.futures.scenario_intelligence_platform_is_missing",
            "ScenarioGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicResilienceFrameworkRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.strategic_resilience_framework_is_missing")
        return _mk(
            cls, tenant_id, "resilience_ref", resilience_ref,
            "civilization.futures.strategic_resilience_framework_is_missing",
            "ResilienceImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FutureDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.future_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.futures.future_digital_twin_is_missing",
            "PolicySimulatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationFuturesIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.meos_civilization_futures_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.futures.meos_civilization_futures_intelligence_core_is_missing",
            "FutureAlertGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FuturesKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.futures_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.futures.futures_knowledge_graph_is_missing",
            "SignalClassifiedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FuturesEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.futures.futures_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.futures.futures_event_architecture_is_missing",
            "StrategyUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
