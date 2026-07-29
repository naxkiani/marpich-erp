"""P214-F aggregates — quality-gate invariants."""
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
class AgentPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.tenant_required")
        if not present:
            raise ValueError("ai.agents.enterprise_ai_agent_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentIdentityRoot(AggregateRoot):
    tenant_id: str
    identity_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, identity_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.identity_tenant_required")
        if not present:
            raise ValueError("ai.agents.agent_identity_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            identity_ref=identity_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentActivatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentMemoryRoot(AggregateRoot):
    tenant_id: str
    memory_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.memory_tenant_required")
        if not present:
            raise ValueError("ai.agents.agent_memory_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            memory_ref=memory_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentLearningEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentReasoningRoot(AggregateRoot):
    tenant_id: str
    reasoning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.reasoning_tenant_required")
        if not present:
            raise ValueError("ai.agents.agent_reasoning_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            reasoning_ref=reasoning_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PlanGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AgentToolRoot(AggregateRoot):
    tenant_id: str
    tool_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, tool_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.tool_tenant_required")
        if not present:
            raise ValueError("ai.agents.agent_tool_ecosystem_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            tool_ref=tool_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ToolInvokedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MultiAgentRoot(AggregateRoot):
    tenant_id: str
    collab_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collab_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agents.collab_tenant_required")
        if not present:
            raise ValueError("ai.agents.multi_agent_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            collab_ref=collab_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("GoalAssignedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
