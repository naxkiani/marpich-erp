"""P219-N aggregates — civilization sustainability intelligence core invariants."""
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
class CivilizationSustainabilityIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; sustainability_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, sustainability_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.civilization_sustainability_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "sustainability_ref", sustainability_ref,
            "civilization.sustainability.civilization_sustainability_intelligence_platform_is_missing",
            "PlanetaryHealthImprovedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ClimateIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; climate_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, climate_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.climate_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "climate_ref", climate_ref,
            "civilization.sustainability.climate_intelligence_platform_is_missing",
            "ClimateUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetarySustainabilityPlatformRoot(AggregateRoot):
    tenant_id: str; planetary_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, planetary_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.planetary_sustainability_platform_is_missing")
        return _mk(
            cls, tenant_id, "planetary_ref", planetary_ref,
            "civilization.sustainability.planetary_sustainability_platform_is_missing",
            "BiodiversityRecoveredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CircularCivilizationSystemsRoot(AggregateRoot):
    tenant_id: str; circular_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, circular_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.circular_civilization_systems_is_missing")
        return _mk(
            cls, tenant_id, "circular_ref", circular_ref,
            "civilization.sustainability.circular_civilization_systems_is_missing",
            "CircularLoopCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CarbonIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; carbon_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, carbon_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.carbon_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "carbon_ref", carbon_ref,
            "civilization.sustainability.carbon_intelligence_platform_is_missing",
            "CarbonMeasuredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnvironmentalDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.environmental_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.sustainability.environmental_digital_twin_is_missing",
            "ClimateScenarioChangedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationSustainabilityIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.meos_civilization_sustainability_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.sustainability.meos_civilization_sustainability_intelligence_core_is_missing",
            "WasteReducedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.sustainability_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.sustainability.sustainability_knowledge_graph_is_missing",
            "MaterialRecoveredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SustainabilityEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.sustainability.sustainability_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.sustainability.sustainability_event_architecture_is_missing",
            "EmissionDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
