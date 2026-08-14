"""P214-T aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class OperatingSystemRoot(AggregateRoot):
    tenant_id: str
    os_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, os_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.tenant_required")
        if not present:
            raise ValueError("ai.aios.enterprise_ai_operating_system_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, os_ref=os_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ControlPlaneCreatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ControlPlaneRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, control_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.control_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_control_plane_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, control_ref=control_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ControlPlaneCreatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OrchestrationRoot(AggregateRoot):
    tenant_id: str
    orchestration_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, orchestration_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.orchestration_tenant_required")
        if not present:
            raise ValueError("ai.aios.autonomous_orchestration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, orchestration_ref=orchestration_ref.strip(), present=True, status="enabled")
        root.pending_events.append("WorkflowExecutedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CommandCenterRoot(AggregateRoot):
    tenant_id: str
    command_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, command_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.command_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_command_center_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, command_ref=command_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AIStateChangedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CapabilityManagementRoot(AggregateRoot):
    tenant_id: str
    capability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, capability_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.capability_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_capability_management_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, capability_ref=capability_ref.strip(), present=True, status="enabled")
        root.pending_events.append("CapabilityRegisteredEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PolicyControlRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.policy_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_policy_control_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, policy_ref=policy_ref.strip(), present=True, status="enabled")
        root.pending_events.append("PolicyAppliedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionControlRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.decision_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_decision_governance_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, decision_ref=decision_ref.strip(), present=True, status="enabled")
        root.pending_events.append("DecisionCompletedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LifecycleRoot(AggregateRoot):
    tenant_id: str
    lifecycle_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.lifecycle_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_lifecycle_management_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, lifecycle_ref=lifecycle_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AIStateChangedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OSDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aios.twin_tenant_required")
        if not present:
            raise ValueError("ai.aios.ai_digital_twin_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("OptimizationTriggeredEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present
