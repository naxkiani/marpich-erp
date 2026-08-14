"""P218-N aggregates — resource intelligence invariants."""
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
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class ResourceIntelPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.resource_intelligence_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.resources.resource_intelligence_is_missing", "ResourceDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class IsruPlatformRoot(AggregateRoot):
    tenant_id: str; isru_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, isru_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.isru_platform_is_missing")
        return _mk(cls, tenant_id, "isru_ref", isru_ref, "space.resources.isru_platform_is_missing", "ISRUFacilityActivatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AsteroidMiningRoot(AggregateRoot):
    tenant_id: str; asteroid_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, asteroid_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.asteroid_mining_intelligence_is_missing")
        return _mk(cls, tenant_id, "asteroid_ref", asteroid_ref, "space.resources.asteroid_mining_intelligence_is_missing", "MiningMissionCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class PlanetaryResourceRoot(AggregateRoot):
    tenant_id: str; planetary_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, planetary_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.planetary_resource_management_is_missing")
        return _mk(cls, tenant_id, "planetary_ref", planetary_ref, "space.resources.planetary_resource_management_is_missing", "ReserveUpdatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousExtractionRoot(AggregateRoot):
    tenant_id: str; autonomy_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonomy_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.autonomous_extraction_is_missing")
        return _mk(cls, tenant_id, "autonomy_ref", autonomy_ref, "space.resources.autonomous_extraction_is_missing", "ExtractionStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.resource_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.resources.resource_ai_is_missing", "ResourceValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.resources.digital_twin_is_missing", "ProcessingCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.resources.governance_is_missing", "ExtractionAuthorizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.resources.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.resources.security_architecture_is_missing", "ResourceDepletedEvent")
    def is_missing(self) -> bool: return not self.present
