"""P219-U aggregates — autonomous civilization operations invariants."""
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
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class AutonomousCivilizationOperationsPlatformRoot(AggregateRoot):
    tenant_id: str; ops_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ops_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.autonomous_civilization_operations_platform_is_missing")
        return _mk(
            cls, tenant_id, "ops_ref", ops_ref,
            "civilization.auto_ops.autonomous_civilization_operations_platform_is_missing",
            "MissionCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MissionOrchestrationPlatformRoot(AggregateRoot):
    tenant_id: str; mission_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, mission_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.mission_orchestration_platform_is_missing")
        return _mk(
            cls, tenant_id, "mission_ref", mission_ref,
            "civilization.auto_ops.mission_orchestration_platform_is_missing",
            "MissionAssignedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OperationsIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; intel_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, intel_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.operations_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "intel_ref", intel_ref,
            "civilization.auto_ops.operations_intelligence_platform_is_missing",
            "PerformanceMeasuredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WorkflowAutomationPlatformRoot(AggregateRoot):
    tenant_id: str; workflow_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, workflow_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.workflow_automation_platform_is_missing")
        return _mk(
            cls, tenant_id, "workflow_ref", workflow_ref,
            "civilization.auto_ops.workflow_automation_platform_is_missing",
            "WorkflowStartedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResourceOptimizationPlatformRoot(AggregateRoot):
    tenant_id: str; resource_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, resource_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.resource_optimization_platform_is_missing")
        return _mk(
            cls, tenant_id, "resource_ref", resource_ref,
            "civilization.auto_ops.resource_optimization_platform_is_missing",
            "ResourceAllocatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OperationsDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.operations_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.auto_ops.operations_digital_twin_is_missing",
            "MissionExecutedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosAutonomousCivilizationOperationsCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.meos_autonomous_civilization_operations_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.auto_ops.meos_autonomous_civilization_operations_core_is_missing",
            "MissionCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OperationsKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.operations_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.auto_ops.operations_knowledge_graph_is_missing",
            "WorkflowOptimizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OperationsEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.auto_ops.operations_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.auto_ops.operations_event_architecture_is_missing",
            "AlertGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present

