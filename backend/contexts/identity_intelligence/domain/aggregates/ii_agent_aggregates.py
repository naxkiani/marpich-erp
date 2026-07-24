"""P207-E Identity AI Agent Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

AGENT_KINDS = frozenset(
    {
        "identity_analyst",
        "identity_governance",
        "identity_security",
        "identity_operations",
        "identity_compliance",
        "identity_architecture",
    }
)

AGENT_TOOLS = frozenset(
    {
        "identity_search_tool",
        "access_analysis_tool",
        "risk_analysis_tool",
        "policy_evaluation_tool",
        "workflow_execution_tool",
        "graph_query_tool",
        "audit_query_tool",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityAiAgentContractRoot(AggregateRoot):
    """Agent contract — permissions required, via AI platform."""

    tenant_id: str
    agent_ref: str
    kind: str
    permission_scope: tuple[str, ...]
    explainable: bool
    via_ai_platform: bool
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        agent_ref: str,
        kind: str,
        permission_scope: tuple[str, ...] | None = None,
        explainable: bool = True,
        via_ai_platform: bool = True,
        audited: bool = True,
    ) -> IdentityAiAgentContractRoot:
        if not tenant_id.strip():
            raise ValueError("ii.agent.tenant_required")
        k = kind.strip().lower()
        if k not in AGENT_KINDS:
            raise ValueError("ii.agent.kind_invalid")
        if permission_scope is None:
            perms = ("identity_intelligence.ai.infer",)
        else:
            perms = tuple(permission_scope)
        if not perms:
            raise ValueError("ii.agent.agents_without_permissions")
        if not explainable:
            raise ValueError("ii.agent.decisions_not_explainable")
        if not via_ai_platform:
            raise ValueError("ii.agent.embeds_llm_sdk")
        if not audited:
            raise ValueError("ii.agent.ai_actions_not_audited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            kind=k,
            permission_scope=tuple(perms),
            explainable=True,
            via_ai_platform=True,
            audited=True,
            status="active",
        )
        root.pending_events.append("AgentActivated")
        root.history.append({"event": "AgentActivated"})
        return root

    def is_permissionless(self) -> bool:
        return len(self.permission_scope) == 0


@dataclass(eq=False, kw_only=True)
class AgentTaskRoot(AggregateRoot):
    tenant_id: str
    task_ref: str
    agent_ref: str
    subject_ref: str
    explanation: str
    human_governance: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        task_ref: str,
        agent_ref: str,
        subject_ref: str,
        explanation: str = "pending",
        human_governance: bool = True,
    ) -> AgentTaskRoot:
        if not tenant_id.strip() or not agent_ref.strip():
            raise ValueError("ii.agent.task_required")
        if not human_governance:
            raise ValueError("ii.agent.human_governance_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            task_ref=task_ref.strip(),
            agent_ref=agent_ref.strip(),
            subject_ref=subject_ref.strip(),
            explanation=explanation.strip() or "pending",
            human_governance=True,
            status="created",
        )
        root.history.append({"event": "AgentTaskCreated"})
        return root

    def complete_analysis(self, *, explanation: str) -> None:
        if not explanation.strip():
            raise ValueError("ii.agent.decisions_not_explainable")
        self.explanation = explanation.strip()
        self.status = "analyzed"
        self.pending_events.append("AnalysisCompleted")
        self.history.append({"event": "AnalysisCompleted"})


@dataclass(eq=False, kw_only=True)
class AgentToolGrantRoot(AggregateRoot):
    tenant_id: str
    grant_ref: str
    agent_ref: str
    tools: tuple[str, ...]
    scoped: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def grant(
        cls,
        *,
        tenant_id: str,
        grant_ref: str,
        agent_ref: str,
        tools: tuple[str, ...] | None = None,
        scoped: bool = True,
    ) -> AgentToolGrantRoot:
        if not tenant_id.strip():
            raise ValueError("ii.agent.grant_tenant_required")
        if tools is None:
            t = ("identity_search_tool", "risk_analysis_tool")
        else:
            t = tuple(tools)
        if not scoped or not t:
            raise ValueError("ii.agent.tool_access_unscoped")
        if not set(t).issubset(AGENT_TOOLS):
            raise ValueError("ii.agent.tool_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            grant_ref=grant_ref.strip(),
            agent_ref=agent_ref.strip(),
            tools=tuple(t),
            scoped=True,
            status="granted",
        )
        root.pending_events.append("ToolAccessGranted")
        root.history.append({"event": "ToolAccessGranted"})
        return root

    def is_unscoped(self) -> bool:
        return not self.scoped or len(self.tools) == 0


@dataclass(eq=False, kw_only=True)
class AgentRecommendationRoot(AggregateRoot):
    tenant_id: str
    recommendation_ref: str
    agent_ref: str
    action: str
    explanation: str
    confidence: float
    high_impact: bool
    hitl_approved: bool
    knowledge_controlled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        recommendation_ref: str,
        agent_ref: str,
        action: str,
        explanation: str,
        confidence: float = 0.8,
        high_impact: bool = False,
        hitl_approved: bool = True,
        knowledge_controlled: bool = True,
    ) -> AgentRecommendationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.agent.rec_tenant_required")
        if not explanation.strip():
            raise ValueError("ii.agent.decisions_not_explainable")
        if not knowledge_controlled:
            raise ValueError("ii.agent.knowledge_sources_uncontrolled")
        if high_impact and not hitl_approved:
            raise ValueError("ii.agent.skips_hitl_high_impact")
        if confidence < 0 or confidence > 1:
            raise ValueError("ii.agent.confidence_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            recommendation_ref=recommendation_ref.strip(),
            agent_ref=agent_ref.strip(),
            action=action.strip(),
            explanation=explanation.strip(),
            confidence=confidence,
            high_impact=high_impact,
            hitl_approved=hitl_approved if high_impact else True,
            knowledge_controlled=True,
            status="created",
        )
        root.pending_events.append("RecommendationCreated")
        if high_impact:
            root.pending_events.append("ApprovalRequested")
        root.history.append({"event": "RecommendationCreated"})
        return root


@dataclass(eq=False, kw_only=True)
class AgentGovernancePolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    security_boundaries_defined: bool
    human_governance: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        security_boundaries_defined: bool = True,
        human_governance: bool = True,
    ) -> AgentGovernancePolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.agent.gov_tenant_required")
        if not security_boundaries_defined:
            raise ValueError("ii.agent.security_boundaries_undefined")
        if not human_governance:
            raise ValueError("ii.agent.human_governance_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            security_boundaries_defined=True,
            human_governance=True,
            status="active",
        )
        root.history.append({"event": "AgentGovernanceDefined"})
        return root

    def is_undefined_security(self) -> bool:
        return not self.security_boundaries_defined
