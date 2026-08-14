"""P218-F aggregates — satellite intelligence invariants."""
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
class SatellitePlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.satellite_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.satellite.satellite_intelligence_platform_is_missing", "SatelliteRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ConstellationRoot(AggregateRoot):
    tenant_id: str; constellation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, constellation_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.constellation_management_is_missing")
        return _mk(cls, tenant_id, "constellation_ref", constellation_ref, "space.satellite.constellation_management_is_missing", "OrbitAdjustedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrbitalAssetRoot(AggregateRoot):
    tenant_id: str; asset_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, asset_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.orbital_asset_operations_is_missing")
        return _mk(cls, tenant_id, "asset_ref", asset_ref, "space.satellite.orbital_asset_operations_is_missing", "SatelliteActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteLifecycleRoot(AggregateRoot):
    tenant_id: str; lifecycle_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.satellite_lifecycle_is_missing")
        return _mk(cls, tenant_id, "lifecycle_ref", lifecycle_ref, "space.satellite.satellite_lifecycle_is_missing", "SatelliteRetiredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PayloadIntelligenceRoot(AggregateRoot):
    tenant_id: str; payload_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, payload_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.payload_intelligence_is_missing")
        return _mk(cls, tenant_id, "payload_ref", payload_ref, "space.satellite.payload_intelligence_is_missing", "PayloadAssignedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.satellite_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.satellite.satellite_ai_is_missing", "AnomalyDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.satellite_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.satellite.satellite_digital_twin_is_missing", "TelemetryReceivedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.ddd_model_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.satellite.ddd_model_is_missing", "MissionScheduledEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SatelliteSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.satellite.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.satellite.security_architecture_is_missing", "SatelliteActivatedEvent")
    def is_missing(self)->bool: return not self.present
