"""P218-I aggregates — space navigation invariants."""
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
class NavigationPlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.space_navigation_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "space.navigation.space_navigation_platform_is_missing", "NavigationInitializedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GnssIntelligenceRoot(AggregateRoot):
    tenant_id: str; gnss_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, gnss_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.gnss_intelligence_is_missing")
        return _mk(cls, tenant_id, "gnss_ref", gnss_ref, "space.navigation.gnss_intelligence_is_missing", "NavigationUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousNavigationRoot(AggregateRoot):
    tenant_id: str; autonav_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, autonav_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.autonomous_navigation_is_missing")
        return _mk(cls, tenant_id, "autonav_ref", autonav_ref, "space.navigation.autonomous_navigation_is_missing", "TrajectoryGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class TrajectoryOptimizationRoot(AggregateRoot):
    tenant_id: str; trajectory_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trajectory_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.trajectory_optimization_is_missing")
        return _mk(cls, tenant_id, "trajectory_ref", trajectory_ref, "space.navigation.trajectory_optimization_is_missing", "TrajectoryOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GncRoot(AggregateRoot):
    tenant_id: str; gnc_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, gnc_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.guidance_and_control_is_missing")
        return _mk(cls, tenant_id, "gnc_ref", gnc_ref, "space.navigation.guidance_and_control_is_missing", "ControlCommandIssuedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class NavigationAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.navigation_ai_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "space.navigation.navigation_ai_is_missing", "TrajectoryOptimizedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class NavigationDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.navigation_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.navigation.navigation_digital_twin_is_missing", "NavigationUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class NavigationObservabilityRoot(AggregateRoot):
    tenant_id: str; obs_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, obs_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.observability_is_missing")
        return _mk(cls, tenant_id, "obs_ref", obs_ref, "space.navigation.observability_is_missing", "LandingCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class NavigationSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("space.navigation.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "space.navigation.security_architecture_is_missing", "ControlCommandIssuedEvent")
    def is_missing(self)->bool: return not self.present
