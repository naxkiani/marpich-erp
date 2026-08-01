"""P216-B aggregates — robotics strategic architecture invariants."""
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
class StrategicArchitectureRoot(AggregateRoot):
    tenant_id: str; architecture_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, architecture_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.robotics_strategic_architecture_is_missing")
        return _mk(cls, tenant_id, "architecture_ref", architecture_ref, "robotics.strategy.robotics_strategic_architecture_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class CapabilityModelRoot(AggregateRoot):
    tenant_id: str; capability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.capability_model_is_missing")
        return _mk(cls, tenant_id, "capability_ref", capability_ref, "robotics.strategy.capability_model_is_missing", "FleetIntelligenceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OperatingFrameworkRoot(AggregateRoot):
    tenant_id: str; framework_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, framework_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.operating_framework_is_missing")
        return _mk(cls, tenant_id, "framework_ref", framework_ref, "robotics.strategy.operating_framework_is_missing", "MissionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ServiceModelRoot(AggregateRoot):
    tenant_id: str; service_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, service_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.service_model_is_missing")
        return _mk(cls, tenant_id, "service_ref", service_ref, "robotics.strategy.service_model_is_missing", "RobotActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OrganizationalModelRoot(AggregateRoot):
    tenant_id: str; org_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, org_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.organizational_model_is_missing")
        return _mk(cls, tenant_id, "org_ref", org_ref, "robotics.strategy.organizational_model_is_missing", "RobotRegisteredEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GovernanceModelRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.governance_model_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "robotics.strategy.governance_model_is_missing", "SafetyAlertGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SecurityModelRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.security_model_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.strategy.security_model_is_missing", "SafetyAlertGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DataArchitectureRoot(AggregateRoot):
    tenant_id: str; data_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, data_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.data_architecture_is_missing")
        return _mk(cls, tenant_id, "data_ref", data_ref, "robotics.strategy.data_architecture_is_missing", "FleetIntelligenceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MaturityModelRoot(AggregateRoot):
    tenant_id: str; maturity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, maturity_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.strategy.maturity_model_is_missing")
        return _mk(cls, tenant_id, "maturity_ref", maturity_ref, "robotics.strategy.maturity_model_is_missing", "MachineOptimizationCompletedEvent")
    def is_missing(self)->bool: return not self.present
