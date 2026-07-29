"""P214-Q aggregates — quality-gate invariants."""
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
class WorkforcePlatformRoot(AggregateRoot):
    tenant_id: str
    workforce_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, workforce_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.ai_digital_workforce_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            workforce_ref=workforce_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EmployeeActivatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EcosystemRoot(AggregateRoot):
    tenant_id: str
    ecosystem_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ecosystem_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.ecosystem_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.multi_agent_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ecosystem_ref=ecosystem_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class OrganizationRoot(AggregateRoot):
    tenant_id: str
    organization_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, organization_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.organization_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.ai_organization_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            organization_ref=organization_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EmployeeActivatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WorkflowRoot(AggregateRoot):
    tenant_id: str
    workflow_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, workflow_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.workflow_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.autonomous_workflow_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            workflow_ref=workflow_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TaskAssignedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LearningRoot(AggregateRoot):
    tenant_id: str
    learning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.learning_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.self_learning_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            learning_ref=learning_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("LearningCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.decision_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.autonomous_decision_framework_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            decision_ref=decision_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DecisionExecutedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MemoryRoot(AggregateRoot):
    tenant_id: str
    memory_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.memory_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.ai_memory_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            memory_ref=memory_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("LearningCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionRoot(AggregateRoot):
    tenant_id: str
    evolution_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.evolution_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.ai_evolution_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            evolution_ref=evolution_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("CapabilityImprovedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class WorkforceDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiworkforce.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiworkforce.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AutonomyChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
