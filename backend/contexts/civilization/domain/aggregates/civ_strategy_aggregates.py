"""P219-B aggregates — civilization strategic architecture invariants."""
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
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class CivilizationStrategyRoot(AggregateRoot):
    tenant_id: str; strategy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, strategy_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.civilization_strategic_architecture_is_missing")
        return _mk(cls, tenant_id, "strategy_ref", strategy_ref, "civilization.strategy.civilization_strategic_architecture_is_missing", "ArchitecturePublishedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CapabilityModelRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.enterprise_capability_model_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "civilization.strategy.enterprise_capability_model_is_missing", "CapabilityCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class OperatingModelRoot(AggregateRoot):
    tenant_id: str; operating_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, operating_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.civilization_operating_model_is_missing")
        return _mk(cls, tenant_id, "operating_ref", operating_ref, "civilization.strategy.civilization_operating_model_is_missing", "OperatingModelChangedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ServiceFrameworkRoot(AggregateRoot):
    tenant_id: str; service_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, service_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.civilization_service_framework_is_missing")
        return _mk(cls, tenant_id, "service_ref", service_ref, "civilization.strategy.civilization_service_framework_is_missing", "ServiceActivatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceFrameworkRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.governance_framework_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "civilization.strategy.governance_framework_is_missing", "GovernanceModelUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class OperatingFrameworkRoot(AggregateRoot):
    tenant_id: str; framework_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, framework_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.operating_framework_is_missing")
        return _mk(cls, tenant_id, "framework_ref", framework_ref, "civilization.strategy.operating_framework_is_missing", "OperatingModelChangedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class DigitalTwinOperatingModelRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.digital_twin_operating_model_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "civilization.strategy.digital_twin_operating_model_is_missing", "DigitalTwinOperatingModelSyncedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class TransformationRoot(AggregateRoot):
    tenant_id: str; transformation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, transformation_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.evolution_model_is_missing")
        return _mk(cls, tenant_id, "transformation_ref", transformation_ref, "civilization.strategy.evolution_model_is_missing", "CivilizationTransformationStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IntegrationArchitectureRoot(AggregateRoot):
    tenant_id: str; integration_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, integration_ref: str, present: bool = True):
        if not present: raise ValueError("civilization.strategy.meos_integration_architecture_is_missing")
        return _mk(cls, tenant_id, "integration_ref", integration_ref, "civilization.strategy.meos_integration_architecture_is_missing", "StrategyUpdatedEvent")
    def is_missing(self) -> bool: return not self.present
