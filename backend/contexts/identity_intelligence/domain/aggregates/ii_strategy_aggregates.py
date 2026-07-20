"""P207-A Identity Intelligence strategy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

AGENT_KINDS = frozenset(
    {
        "identity_analyst",
        "governance",
        "security",
        "operations",
        "compliance",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityIntelligenceProfileRoot(AggregateRoot):
    """Intelligence profile — never chatbot-only."""

    tenant_id: str
    profile_ref: str
    chatbot_only: bool
    predictive_risk: bool
    behavioral_analytics: bool
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        chatbot_only: bool = False,
        predictive_risk: bool = True,
        behavioral_analytics: bool = True,
        explainable: bool = True,
    ) -> IdentityIntelligenceProfileRoot:
        if not tenant_id.strip():
            raise ValueError("ii.tenant_required")
        if chatbot_only:
            raise ValueError("ii.ai_only_chatbot")
        if not predictive_risk or not behavioral_analytics:
            raise ValueError("ii.intelligence_incomplete")
        if not explainable:
            raise ValueError("ii.decisions_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            chatbot_only=False,
            predictive_risk=True,
            behavioral_analytics=True,
            explainable=True,
            status="active",
        )
        root.pending_events.append("InsightGenerated")
        root.history.append({"event": "IntelligenceProfileDefined"})
        return root

    def is_chatbot_only(self) -> bool:
        return self.chatbot_only


@dataclass(eq=False, kw_only=True)
class AutonomousOperationRunRoot(AggregateRoot):
    """Autonomous run — governance + HITL required for high impact."""

    tenant_id: str
    run_ref: str
    governed: bool
    human_control: bool
    high_impact: bool
    hitl_approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        run_ref: str,
        governed: bool = True,
        human_control: bool = True,
        high_impact: bool = False,
        hitl_approved: bool = True,
    ) -> AutonomousOperationRunRoot:
        if not tenant_id.strip():
            raise ValueError("ii.ops_tenant_required")
        if not governed:
            raise ValueError("ii.automation_without_governance")
        if not human_control:
            raise ValueError("ii.human_control_removed")
        if high_impact and not hitl_approved:
            raise ValueError("ii.hitl_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            governed=True,
            human_control=True,
            high_impact=high_impact,
            hitl_approved=hitl_approved if high_impact else True,
            status="running",
        )
        root.pending_events.append("ActionRecommended")
        root.history.append({"event": "AutonomousRunStarted"})
        return root

    def execute_remediation(self) -> None:
        self.status = "executed"
        self.pending_events.append("RemediationExecuted")
        self.history.append({"event": "RemediationExecuted"})


@dataclass(eq=False, kw_only=True)
class IdentityAiAgentContractRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    kind: str
    explainable: bool
    via_ai_platform: bool
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
        explainable: bool = True,
        via_ai_platform: bool = True,
    ) -> IdentityAiAgentContractRoot:
        if not tenant_id.strip():
            raise ValueError("ii.agent_tenant_required")
        k = kind.strip().lower()
        if k not in AGENT_KINDS:
            raise ValueError("ii.agent_kind_invalid")
        if not explainable:
            raise ValueError("ii.decisions_not_explainable")
        if not via_ai_platform:
            raise ValueError("ii.embeds_llm_sdk")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            kind=k,
            explainable=True,
            via_ai_platform=True,
            status="registered",
        )
        root.history.append({"event": "AgentContractRegistered"})
        return root


@dataclass(eq=False, kw_only=True)
class DigitalTwinOrchestrationRoot(AggregateRoot):
    """Orchestrates twin via peer SoR — never owns twin storage."""

    tenant_id: str
    orchestration_ref: str
    twin_ref: str
    twin_present: bool
    owns_twin_sor: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        orchestration_ref: str,
        twin_ref: str,
        twin_present: bool = True,
        owns_twin_sor: bool = False,
    ) -> DigitalTwinOrchestrationRoot:
        if not tenant_id.strip() or not twin_ref.strip():
            raise ValueError("ii.twin_required")
        if not twin_present:
            raise ValueError("ii.digital_twin_absent")
        if owns_twin_sor:
            raise ValueError("ii.duplicates_twin_sor")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            orchestration_ref=orchestration_ref.strip(),
            twin_ref=twin_ref.strip(),
            twin_present=True,
            owns_twin_sor=False,
            status="bound",
        )
        root.history.append({"event": "TwinOrchestrationBound"})
        return root

    def is_absent(self) -> bool:
        return not self.twin_present


@dataclass(eq=False, kw_only=True)
class IdentityRiskPredictionRoot(AggregateRoot):
    tenant_id: str
    prediction_ref: str
    subject_ref: str
    score: float
    explanation: str
    measurable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def predict(
        cls,
        *,
        tenant_id: str,
        prediction_ref: str,
        subject_ref: str,
        score: float,
        explanation: str,
        measurable: bool = True,
    ) -> IdentityRiskPredictionRoot:
        if not tenant_id.strip() or not subject_ref.strip():
            raise ValueError("ii.risk_required")
        if not measurable:
            raise ValueError("ii.risk_prediction_not_measurable")
        if not explanation.strip():
            raise ValueError("ii.decisions_not_explainable")
        if score < 0 or score > 1:
            raise ValueError("ii.risk_score_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            prediction_ref=prediction_ref.strip(),
            subject_ref=subject_ref.strip(),
            score=score,
            explanation=explanation.strip(),
            measurable=True,
            status="predicted",
        )
        root.pending_events.append("RiskPredicted")
        root.history.append({"event": "RiskPredicted", "score": score})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class KnowledgeGraphIntegrationRoot(AggregateRoot):
    tenant_id: str
    integration_ref: str
    graph_integrated: bool
    owns_graph_sor: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def connect(
        cls,
        *,
        tenant_id: str,
        integration_ref: str,
        graph_integrated: bool = True,
        owns_graph_sor: bool = False,
    ) -> KnowledgeGraphIntegrationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph_tenant_required")
        if not graph_integrated:
            raise ValueError("ii.identity_graph_integration_missing")
        if owns_graph_sor:
            raise ValueError("ii.duplicates_directory_graph_sor")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            integration_ref=integration_ref.strip(),
            graph_integrated=True,
            owns_graph_sor=False,
            status="connected",
        )
        root.history.append({"event": "GraphIntegrationConnected"})
        return root

    def is_missing(self) -> bool:
        return not self.graph_integrated
