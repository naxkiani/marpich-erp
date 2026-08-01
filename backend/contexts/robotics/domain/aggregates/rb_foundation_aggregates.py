"""P216 aggregates — robotics / cyber-physical foundation invariants."""
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
class RobotSystemRoot(AggregateRoot):
    tenant_id: str; robot_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robot_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.enterprise_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robot_ref", robot_ref, "robotics.foundation.enterprise_robotics_platform_is_missing", "RobotCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousMachineRoot(AggregateRoot):
    tenant_id: str; machine_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, machine_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.autonomous_machine_platform_is_missing")
        return _mk(cls, tenant_id, "machine_ref", machine_ref, "robotics.foundation.autonomous_machine_platform_is_missing", "AutonomousActionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PhysicalAIRoot(AggregateRoot):
    tenant_id: str; pai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, pai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.physical_ai_engine_is_missing")
        return _mk(cls, tenant_id, "pai_ref", pai_ref, "robotics.foundation.physical_ai_engine_is_missing", "PhysicalAIModelUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class IndustrialIntelligenceRoot(AggregateRoot):
    tenant_id: str; industrial_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, industrial_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.industrial_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "industrial_ref", industrial_ref, "robotics.foundation.industrial_intelligence_platform_is_missing", "MachineCapabilityUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RobotFleetRoot(AggregateRoot):
    tenant_id: str; fleet_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, fleet_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.robot_fleet_intelligence_is_missing")
        return _mk(cls, tenant_id, "fleet_ref", fleet_ref, "robotics.foundation.robot_fleet_intelligence_is_missing", "FleetOptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanRobotCollaborationRoot(AggregateRoot):
    tenant_id: str; hri_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hri_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.human_robot_collaboration_is_missing")
        return _mk(cls, tenant_id, "hri_ref", hri_ref, "robotics.foundation.human_robot_collaboration_is_missing", "SafetyValidationCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class EdgeIntelligenceRoot(AggregateRoot):
    tenant_id: str; edge_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, edge_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.edge_intelligence_is_missing")
        return _mk(cls, tenant_id, "edge_ref", edge_ref, "robotics.foundation.edge_intelligence_is_missing", "AutonomousActionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoboticsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.foundation.digital_twin_integration_is_missing", "MissionStartedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SafetyIntelligenceRoot(AggregateRoot):
    tenant_id: str; safety_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.foundation.cyber_physical_security_is_missing")
        return _mk(cls, tenant_id, "safety_ref", safety_ref, "robotics.foundation.cyber_physical_security_is_missing", "SafetyViolationDetectedEvent")
    def is_missing(self)->bool: return not self.present
