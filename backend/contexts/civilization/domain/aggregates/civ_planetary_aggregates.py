"""P219-D aggregates — planetary infrastructure intelligence invariants."""
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
class PlanetaryIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; planetary_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, planetary_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.planetary_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "planetary_ref", planetary_ref,
            "civilization.planetary.planetary_intelligence_platform_is_missing",
            "PlanetaryDecisionGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EarthDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.earth_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.planetary.earth_digital_twin_is_missing", "TwinCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SmartPlanetArchitectureRoot(AggregateRoot):
    tenant_id: str; smart_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, smart_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.smart_planet_architecture_is_missing")
        return _mk(
            cls, tenant_id, "smart_ref", smart_ref,
            "civilization.planetary.smart_planet_architecture_is_missing",
            "InfrastructureOptimizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalInfrastructureIntelligenceRoot(AggregateRoot):
    tenant_id: str; global_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, global_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.global_infrastructure_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "global_ref", global_ref,
            "civilization.planetary.global_infrastructure_intelligence_is_missing",
            "SystemDependencyDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousPlanetaryOpsRoot(AggregateRoot):
    tenant_id: str; ops_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ops_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.autonomous_planetary_operations_foundation_is_missing")
        return _mk(
            cls, tenant_id, "ops_ref", ops_ref,
            "civilization.planetary.autonomous_planetary_operations_foundation_is_missing",
            "MaintenanceScheduledEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosPlanetaryIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.meos_planetary_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.planetary.meos_planetary_intelligence_core_is_missing",
            "SimulationCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.planetary_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.planetary.planetary_knowledge_graph_is_missing",
            "InfrastructureImpactDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryAiEngineRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.planetary_ai_engine_contract_is_missing")
        return _mk(
            cls, tenant_id, "ai_ref", ai_ref,
            "civilization.planetary.planetary_ai_engine_contract_is_missing",
            "FutureScenarioGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.planetary.planetary_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.planetary.planetary_event_architecture_is_missing",
            "AssetFailureDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
