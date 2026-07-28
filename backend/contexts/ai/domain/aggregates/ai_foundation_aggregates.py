"""P214-A aggregates — quality-gate invariants."""
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
class AiFoundationProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "ai.foundation.tenant_required")
        if not complete:
            raise ValueError(
                "ai.foundation.enterprise_ai_platform_foundation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("AIModelRegisteredEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class AiMlPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.foundation.ml_tenant_required")
        if not present:
            raise ValueError(
                "ai.foundation.machine_learning_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AITrainingStartedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiGenerativePlatformRoot(AggregateRoot):
    tenant_id: str
    gen_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, gen_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.foundation.gen_tenant_required")
        if not present:
            raise ValueError(
                "ai.foundation.generative_ai_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gen_ref=gen_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIModelDeployedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiVectorIntelligenceRoot(AggregateRoot):
    tenant_id: str
    vector_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, vector_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.foundation.vector_tenant_required")
        if not present:
            raise ValueError("ai.foundation.vector_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            vector_ref=vector_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIInferenceExecutedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiGovernanceFoundationRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, governance_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.foundation.gov_tenant_required")
        if not present:
            raise ValueError(
                "ai.foundation.ai_governance_foundation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            governance_ref=governance_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIGovernanceValidatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiAgentFoundationRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.foundation.agent_tenant_required")
        if not present:
            raise ValueError("ai.foundation.ai_agent_foundation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            agent_ref=agent_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIInferenceExecutedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
