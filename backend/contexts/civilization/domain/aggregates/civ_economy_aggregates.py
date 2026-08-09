"""P219-H aggregates — civilization economy platform invariants."""
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
class CivilizationEconomyIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; economy_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, economy_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.civilization_economy_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "economy_ref", economy_ref,
            "civilization.economy.civilization_economy_intelligence_platform_is_missing",
            "EconomicModelCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalEconomicIntelligenceRoot(AggregateRoot):
    tenant_id: str; global_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, global_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.global_economic_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "global_ref", global_ref,
            "civilization.economy.global_economic_intelligence_is_missing",
            "EconomicStateChangedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EconomicDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.economic_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.economy.economic_digital_twin_is_missing",
            "MarketShiftDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FutureEconomyIntelligenceRoot(AggregateRoot):
    tenant_id: str; future_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, future_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.future_economy_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "future_ref", future_ref,
            "civilization.economy.future_economy_intelligence_is_missing",
            "FutureEconomyScenarioGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousEconomicAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.autonomous_economic_agents_is_missing")
        return _mk(
            cls, tenant_id, "agents_ref", agents_ref,
            "civilization.economy.autonomous_economic_agents_is_missing",
            "InvestmentOpportunityCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EconomicSimulationCapabilityRoot(AggregateRoot):
    tenant_id: str; sim_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, sim_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.economic_simulation_capability_is_missing")
        return _mk(
            cls, tenant_id, "sim_ref", sim_ref,
            "civilization.economy.economic_simulation_capability_is_missing",
            "InnovationAcceleratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationEconomyPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.meos_civilization_economy_platform_is_missing")
        return _mk(
            cls, tenant_id, "platform_ref", platform_ref,
            "civilization.economy.meos_civilization_economy_platform_is_missing",
            "EconomicRiskDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EconomicKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.economic_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.economy.economic_knowledge_graph_is_missing",
            "EconomicPatternDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EconomicEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.economy.economic_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.economy.economic_event_architecture_is_missing",
            "EconomicForecastGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
