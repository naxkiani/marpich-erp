"""P213-M aggregates — quality-gate invariants."""
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
class BiAiProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.ai.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.ai.ai_native_decision_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("DecisionRequestedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiAutonomousDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, decision_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.ai.ad_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ai.autonomous_decision_intelligence_is_missing"
            )
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
class BiAgentPlatformRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agent_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ai.agent_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ai.enterprise_ai_agent_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            agent_ref=agent_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentCollaboratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiExecutiveCopilotRoot(AggregateRoot):
    tenant_id: str
    copilot_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, copilot_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.ai.copilot_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ai.executive_ai_copilot_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            copilot_ref=copilot_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RecommendationGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiAiGovernanceRoot(AggregateRoot):
    tenant_id: str
    gov_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, gov_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ai.gov_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ai.ai_governance_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gov_ref=gov_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PolicyValidationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiMultiAgentCollaborationRoot(AggregateRoot):
    tenant_id: str
    collab_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, collab_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.ai.mac_tenant_required")
        if not present:
            raise ValueError(
                "analytics.ai.multi_agent_collaboration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            collab_ref=collab_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AgentCollaboratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
