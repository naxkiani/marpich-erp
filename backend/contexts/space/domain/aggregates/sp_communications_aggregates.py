"""P218-H aggregates — space communications invariants."""
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
class CommunicationsPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.space_communications_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.communications.space_communications_platform_is_missing", "GroundStationOnlineEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DeepSpaceNetworkRoot(AggregateRoot):
    tenant_id: str; dsn_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, dsn_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.deep_space_network_is_missing")
        return _mk(cls, tenant_id, "dsn_ref", dsn_ref, "space.communications.deep_space_network_is_missing", "DeepSpaceWindowOpenedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class InterSatelliteNetworkRoot(AggregateRoot):
    tenant_id: str; isn_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, isn_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.inter_satellite_networking_is_missing")
        return _mk(cls, tenant_id, "isn_ref", isn_ref, "space.communications.inter_satellite_networking_is_missing", "RouteOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LaserCommunicationsRoot(AggregateRoot):
    tenant_id: str; laser_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, laser_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.laser_communications_is_missing")
        return _mk(cls, tenant_id, "laser_ref", laser_ref, "space.communications.laser_communications_is_missing", "LaserLinkActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class NetworkAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.communication_ai_platform_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.communications.communication_ai_platform_is_missing", "NetworkCongestionDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CommunicationsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.communication_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.communications.communication_digital_twin_is_missing", "CommunicationEstablishedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionCommsRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.ddd_model_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "space.communications.ddd_model_is_missing", "MissionCommunicationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CommunicationsObservabilityRoot(AggregateRoot):
    tenant_id: str; obs_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, obs_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.observability_is_missing")
        return _mk(cls, tenant_id, "obs_ref", obs_ref, "space.communications.observability_is_missing", "CommunicationLostEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CommunicationsSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.communications.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.communications.security_architecture_is_missing", "BandwidthAllocatedEvent")
    def is_missing(self)->bool: return not self.present
