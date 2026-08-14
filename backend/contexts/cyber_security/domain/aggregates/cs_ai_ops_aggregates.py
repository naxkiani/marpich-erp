"""P210-J AI Ops aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsAiOpsExplainableDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def decide(
        cls, *, tenant_id: str, decision_ref: str, explainable: bool = True
    ) -> CsAiOpsExplainableDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.tenant_required")
        if not explainable:
            raise ValueError("cyber_security.ai_ops.ai_decisions_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            explainable=True,
            status="decided",
        )
        root.pending_events.append("RecommendationGenerated")
        root.pending_events.append("UnexplainableDecisionRejected")
        root.history.append({"event": "ExplainableDecision"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class CsAiOpsHumanOversightRoot(AggregateRoot):
    tenant_id: str
    gate_ref: str
    oversight_present: bool
    via_workflow: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def require(
        cls,
        *,
        tenant_id: str,
        gate_ref: str,
        oversight_present: bool = True,
        via_workflow: bool = True,
    ) -> CsAiOpsHumanOversightRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.hitl_tenant_required")
        if not oversight_present or not via_workflow:
            raise ValueError("cyber_security.ai_ops.human_oversight_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            oversight_present=True,
            via_workflow=True,
            status="pending",
        )
        root.pending_events.append("AbsentOversightRejected")
        root.history.append({"event": "HumanOversightRequired"})
        return root

    def is_absent(self) -> bool:
        return not self.oversight_present or not self.via_workflow


@dataclass(eq=False, kw_only=True)
class CsAiOpsAgentCollaborationRoot(AggregateRoot):
    tenant_id: str
    collaboration_ref: str
    supported: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collaborate(
        cls, *, tenant_id: str, collaboration_ref: str, supported: bool = True
    ) -> CsAiOpsAgentCollaborationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.collab_tenant_required")
        if not supported:
            raise ValueError(
                "cyber_security.ai_ops.agent_collaboration_unsupported"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            collaboration_ref=collaboration_ref.strip(),
            supported=True,
            status="collaborating",
        )
        root.pending_events.append("AgentCollaborated")
        root.pending_events.append("UnsupportedCollaborationRejected")
        root.history.append({"event": "AgentCollaboration"})
        return root

    def is_unsupported(self) -> bool:
        return not self.supported


@dataclass(eq=False, kw_only=True)
class CsAiOpsKnowledgeGraphConnectedRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    connected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, graph_ref: str, connected: bool = True
    ) -> CsAiOpsKnowledgeGraphConnectedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.kg_tenant_required")
        if not connected:
            raise ValueError(
                "cyber_security.ai_ops.knowledge_graph_disconnected"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            graph_ref=graph_ref.strip(),
            connected=True,
            status="connected",
        )
        root.pending_events.append("DisconnectedKgRejected")
        root.history.append({"event": "KnowledgeGraphConnected"})
        return root

    def is_disconnected(self) -> bool:
        return not self.connected


@dataclass(eq=False, kw_only=True)
class CsAiOpsAuditedAutonomyRoot(AggregateRoot):
    tenant_id: str
    action_ref: str
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, action_ref: str, audited: bool = True
    ) -> CsAiOpsAuditedAutonomyRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.auto_tenant_required")
        if not audited:
            raise ValueError(
                "cyber_security.ai_ops.autonomous_actions_unaudited"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            action_ref=action_ref.strip(),
            audited=True,
            status="executed",
        )
        root.pending_events.append("ResponseExecuted")
        root.pending_events.append("UnauditedAutonomyRejected")
        root.history.append({"event": "AuditedAutonomy"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class CsAiOpsGovernanceCompleteRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assert_complete(
        cls, *, tenant_id: str, governance_ref: str, complete: bool = True
    ) -> CsAiOpsGovernanceCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.gov_tenant_required")
        if not complete:
            raise ValueError("cyber_security.ai_ops.ai_governance_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            governance_ref=governance_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("IncompleteGovernanceRejected")
        root.history.append({"event": "AiGovernanceComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class CsAiOpsModelLifecycleRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    managed: bool
    version: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def manage(
        cls,
        *,
        tenant_id: str,
        model_ref: str,
        managed: bool = True,
        version: str = "1.0.0",
    ) -> CsAiOpsModelLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.model_tenant_required")
        if not managed or not version.strip():
            raise ValueError(
                "cyber_security.ai_ops.model_lifecycle_management_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            managed=True,
            version=version.strip(),
            status="managed",
        )
        root.pending_events.append("ModelRetrained")
        root.pending_events.append("MissingLifecycleRejected")
        root.history.append({"event": "ModelLifecycleManaged"})
        return root

    def is_missing(self) -> bool:
        return not self.managed or not self.version


@dataclass(eq=False, kw_only=True)
class CsAiOpsInvestigationCompletedRoot(AggregateRoot):
    tenant_id: str
    investigation_ref: str
    agent_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls, *, tenant_id: str, investigation_ref: str, agent_ref: str
    ) -> CsAiOpsInvestigationCompletedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.ai_ops.inv_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            investigation_ref=investigation_ref.strip(),
            agent_ref=agent_ref.strip(),
            status="completed",
        )
        root.pending_events.append("InvestigationCompleted")
        root.pending_events.append("ThreatAnalysed")
        root.history.append({"event": "InvestigationCompleted"})
        return root
