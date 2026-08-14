"""P219-F aggregates — planetary digital twin / earth intelligence twin invariants."""
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
class MeosEarthIntelligenceTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.meos_earth_intelligence_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.simulation.meos_earth_intelligence_twin_is_missing",
            "EarthTwinCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryDigitalTwinArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.planetary_digital_twin_architecture_is_missing")
        return _mk(
            cls, tenant_id, "architecture_ref", architecture_ref,
            "civilization.simulation.planetary_digital_twin_architecture_is_missing",
            "EarthStateUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EarthSimulationPlatformRoot(AggregateRoot):
    tenant_id: str; sim_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, sim_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.earth_simulation_platform_is_missing")
        return _mk(
            cls, tenant_id, "sim_ref", sim_ref,
            "civilization.simulation.earth_simulation_platform_is_missing",
            "SimulationStartedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationSimulationEngineRoot(AggregateRoot):
    tenant_id: str; civ_sim_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, civ_sim_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.civilization_simulation_engine_is_missing")
        return _mk(
            cls, tenant_id, "civ_sim_ref", civ_sim_ref,
            "civilization.simulation.civilization_simulation_engine_is_missing",
            "CivilizationScenarioGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FutureScenarioIntelligenceRoot(AggregateRoot):
    tenant_id: str; scenario_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, scenario_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.future_scenario_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "scenario_ref", scenario_ref,
            "civilization.simulation.future_scenario_intelligence_is_missing",
            "FutureImpactDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DigitalTwinDomainModelRoot(AggregateRoot):
    tenant_id: str; domain_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, domain_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.digital_twin_domain_model_is_missing")
        return _mk(
            cls, tenant_id, "domain_ref", domain_ref,
            "civilization.simulation.digital_twin_domain_model_is_missing",
            "TwinSynchronizationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EarthIntelligenceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.earth_intelligence_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.simulation.earth_intelligence_knowledge_graph_is_missing",
            "EnvironmentalPatternDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DigitalTwinAiEngineRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.digital_twin_ai_intelligence_engine_is_missing")
        return _mk(
            cls, tenant_id, "ai_ref", ai_ref,
            "civilization.simulation.digital_twin_ai_intelligence_engine_is_missing",
            "StrategicRecommendationCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SimulationEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.simulation.simulation_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.simulation.simulation_event_architecture_is_missing",
            "SimulationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
