"""P218-D aggregates — space infrastructure invariants."""
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
class SpaceInfrastructureRoot(AggregateRoot):
    tenant_id: str; infra_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, infra_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.space_infrastructure_architecture_is_missing")
        return _mk(cls, tenant_id, "infra_ref", infra_ref, "space.infrastructure.space_infrastructure_architecture_is_missing", "MissionInfrastructureReadyEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GroundSegmentRoot(AggregateRoot):
    tenant_id: str; ground_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ground_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.ground_segment_platform_is_missing")
        return _mk(cls, tenant_id, "ground_ref", ground_ref, "space.infrastructure.ground_segment_platform_is_missing", "GroundStationActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionControlRoot(AggregateRoot):
    tenant_id: str; moc_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, moc_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.mission_control_platform_is_missing")
        return _mk(cls, tenant_id, "moc_ref", moc_ref, "space.infrastructure.mission_control_platform_is_missing", "MissionControlInitializedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceCloudRoot(AggregateRoot):
    tenant_id: str; cloud_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cloud_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.space_cloud_platform_is_missing")
        return _mk(cls, tenant_id, "cloud_ref", cloud_ref, "space.infrastructure.space_cloud_platform_is_missing", "CloudClusterScaledEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceNetworkRoot(AggregateRoot):
    tenant_id: str; network_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.space_network_architecture_is_missing")
        return _mk(cls, tenant_id, "network_ref", network_ref, "space.infrastructure.space_network_architecture_is_missing", "NetworkPathUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SpaceDataInfraRoot(AggregateRoot):
    tenant_id: str; data_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, data_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.space_data_platform_is_missing")
        return _mk(cls, tenant_id, "data_ref", data_ref, "space.infrastructure.space_data_platform_is_missing", "TelemetryReceivedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class InfraDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.infrastructure_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.infrastructure.infrastructure_digital_twin_is_missing", "MissionInfrastructureReadyEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class InfraSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.infrastructure_security_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.infrastructure.infrastructure_security_is_missing", "InfrastructureFailureDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ObservabilityRoot(AggregateRoot):
    tenant_id: str; observability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, observability_ref: str, present: bool = True):
        if not present: raise ValueError("space.infrastructure.observability_architecture_is_missing")
        return _mk(cls, tenant_id, "observability_ref", observability_ref, "space.infrastructure.observability_architecture_is_missing", "InfrastructureRecoveredEvent")
    def is_missing(self)->bool: return not self.present
