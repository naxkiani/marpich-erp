"""P219-G aggregates — planetary resource intelligence invariants."""
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
class PlanetaryResourceIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; resource_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, resource_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.planetary_resource_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "resource_ref", resource_ref,
            "civilization.resources.planetary_resource_intelligence_platform_is_missing",
            "ResourceRegisteredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EnergyIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; energy_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, energy_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.energy_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "energy_ref", energy_ref,
            "civilization.resources.energy_intelligence_platform_is_missing",
            "EnergyDemandPredictedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WaterIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; water_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, water_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.water_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "water_ref", water_ref,
            "civilization.resources.water_intelligence_platform_is_missing",
            "WaterRiskDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FoodIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; food_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, food_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.food_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "food_ref", food_ref,
            "civilization.resources.food_intelligence_platform_is_missing",
            "FoodRiskDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceOptimizationEngineRoot(AggregateRoot):
    tenant_id: str; opt_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, opt_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.resource_optimization_engine_is_missing")
        return _mk(
            cls, tenant_id, "opt_ref", opt_ref,
            "civilization.resources.resource_optimization_engine_is_missing",
            "ResourceOptimizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.resource_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.resources.resource_digital_twin_is_missing",
            "ResourceMonitoredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosPlanetaryResourceIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.meos_planetary_resource_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.resources.meos_planetary_resource_intelligence_core_is_missing",
            "ResourceAllocatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.resource_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.resources.resource_knowledge_graph_is_missing",
            "ResourceDiscoveredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.resources.resource_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.resources.resource_event_architecture_is_missing",
            "ResourceRiskDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
