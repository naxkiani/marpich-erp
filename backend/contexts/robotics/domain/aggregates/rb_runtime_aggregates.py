"""P216-D aggregates — robotics OS / runtime / fleet control invariants."""
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
class ErosOsRoot(AggregateRoot):
    tenant_id: str; os_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, os_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.robotics_os_architecture_is_missing")
        return _mk(cls, tenant_id, "os_ref", os_ref, "robotics.runtime.robotics_os_architecture_is_missing", "RobotRuntimeStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RobotRuntimeRoot(AggregateRoot):
    tenant_id: str; runtime_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, runtime_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.robot_runtime_platform_is_missing")
        return _mk(cls, tenant_id, "runtime_ref", runtime_ref, "robotics.runtime.robot_runtime_platform_is_missing", "RobotApplicationDeployedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class FleetControlPlaneRoot(AggregateRoot):
    tenant_id: str; fleet_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fleet_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.fleet_control_plane_is_missing")
        return _mk(cls, tenant_id, "fleet_ref", fleet_ref, "robotics.runtime.fleet_control_plane_is_missing", "FleetOptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousInfraRoot(AggregateRoot):
    tenant_id: str; infra_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, infra_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.autonomous_machine_infrastructure_is_missing")
        return _mk(cls, tenant_id, "infra_ref", infra_ref, "robotics.runtime.autonomous_machine_infrastructure_is_missing", "MachineRecoveredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EdgePlatformRoot(AggregateRoot):
    tenant_id: str; edge_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, edge_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.edge_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "edge_ref", edge_ref, "robotics.runtime.edge_robotics_platform_is_missing", "RobotRuntimeStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MissionRuntimeRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.mission_execution_engine_is_missing")
        return _mk(cls, tenant_id, "mission_ref", mission_ref, "robotics.runtime.mission_execution_engine_is_missing", "MissionExecutionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DeviceManagementRoot(AggregateRoot):
    tenant_id: str; device_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, device_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.device_management_is_missing")
        return _mk(cls, tenant_id, "device_ref", device_ref, "robotics.runtime.device_management_is_missing", "RobotApplicationDeployedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RuntimeSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.runtime.security_architecture_is_missing", "RuntimeSecurityViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SelfHealingRoot(AggregateRoot):
    tenant_id: str; recovery_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, recovery_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.runtime.self_healing_capability_is_missing")
        return _mk(cls, tenant_id, "recovery_ref", recovery_ref, "robotics.runtime.self_healing_capability_is_missing", "MachineRecoveredEvent")
    def is_missing(self)->bool: return not self.present
