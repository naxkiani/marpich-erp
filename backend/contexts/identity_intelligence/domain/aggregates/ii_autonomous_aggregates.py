"""P207-D Autonomous Identity Operations aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

DECISION_OUTPUTS = frozenset(
    {"approve", "deny", "request_approval", "execute_remediation", "monitor"}
)


@dataclass(eq=False, kw_only=True)
class AutonomousOperationRunRoot(AggregateRoot):
    """Governed autonomous run — never ungoverned / never no human oversight."""

    tenant_id: str
    run_ref: str
    event_kind: str
    governed: bool
    human_oversight: bool
    policy_validated: bool
    auditable: bool
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
        event_kind: str = "identity_modification",
        governed: bool = True,
        human_oversight: bool = True,
        policy_validated: bool = True,
        auditable: bool = True,
    ) -> AutonomousOperationRunRoot:
        if not tenant_id.strip():
            raise ValueError("ii.auto.tenant_required")
        if not governed:
            raise ValueError("ii.auto.automation_without_governance")
        if not human_oversight:
            raise ValueError("ii.auto.human_oversight_absent")
        if not policy_validated:
            raise ValueError("ii.auto.skips_policy_validation")
        if not auditable:
            raise ValueError("ii.auto.actions_not_auditable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            event_kind=event_kind.strip(),
            governed=True,
            human_oversight=True,
            policy_validated=True,
            auditable=True,
            status="started",
        )
        root.pending_events.append("IdentityOperationStarted")
        root.history.append({"event": "IdentityOperationStarted"})
        return root

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class AutonomousDecisionCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    outcome: str
    explanation: str
    security_bypassed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        outcome: str = "request_approval",
        explanation: str,
        security_bypassed: bool = False,
    ) -> AutonomousDecisionCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.auto.decision_tenant_required")
        o = outcome.strip().lower()
        if o not in DECISION_OUTPUTS:
            raise ValueError("ii.auto.decision_outcome_invalid")
        if not explanation.strip():
            raise ValueError("ii.auto.decisions_not_explainable")
        if security_bypassed:
            raise ValueError("ii.auto.security_controls_bypassed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            outcome=o,
            explanation=explanation.strip(),
            security_bypassed=False,
            status="generated",
        )
        root.pending_events.append("DecisionGenerated")
        if o == "request_approval":
            root.pending_events.append("ApprovalRequested")
        root.history.append({"event": "DecisionGenerated", "outcome": o})
        return root

    def is_non_explainable(self) -> bool:
        return not self.explanation.strip()


@dataclass(eq=False, kw_only=True)
class SelfHealingRemediationRoot(AggregateRoot):
    tenant_id: str
    remediation_ref: str
    kind: str
    reversible: bool
    recovery_present: bool
    hitl_approved: bool
    high_impact: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        remediation_ref: str,
        kind: str = "attribute_repair",
        reversible: bool = True,
        recovery_present: bool = True,
        high_impact: bool = False,
        hitl_approved: bool = True,
    ) -> SelfHealingRemediationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.auto.heal_tenant_required")
        if not recovery_present:
            raise ValueError("ii.auto.recovery_mechanisms_missing")
        if not reversible:
            raise ValueError("ii.auto.irreversible_without_compensation")
        if high_impact and not hitl_approved:
            raise ValueError("ii.auto.hitl_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            remediation_ref=remediation_ref.strip(),
            kind=kind.strip(),
            reversible=True,
            recovery_present=True,
            hitl_approved=hitl_approved if high_impact else True,
            high_impact=high_impact,
            status="ready",
        )
        root.history.append({"event": "RemediationPrepared"})
        return root

    def execute(self) -> None:
        self.status = "completed"
        self.pending_events.append("RemediationCompleted")
        self.pending_events.append("ActionExecuted")
        self.history.append({"event": "RemediationCompleted"})

    def is_missing_recovery(self) -> bool:
        return not self.recovery_present


@dataclass(eq=False, kw_only=True)
class ActionApprovalGateRoot(AggregateRoot):
    """Approval gate — Workflow Engine, never local approval engine."""

    tenant_id: str
    gate_ref: str
    action_ref: str
    via_workflow: bool
    local_engine: bool
    approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def request(
        cls,
        *,
        tenant_id: str,
        gate_ref: str,
        action_ref: str,
        via_workflow: bool = True,
        local_engine: bool = False,
    ) -> ActionApprovalGateRoot:
        if not tenant_id.strip():
            raise ValueError("ii.auto.gate_tenant_required")
        if local_engine or not via_workflow:
            raise ValueError("ii.auto.local_approval_engine")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            action_ref=action_ref.strip(),
            via_workflow=True,
            local_engine=False,
            approved=False,
            status="pending",
        )
        root.pending_events.append("ApprovalRequested")
        root.history.append({"event": "ApprovalRequested"})
        return root

    def approve(self) -> None:
        self.approved = True
        self.status = "approved"
        self.history.append({"event": "ActionApproved"})


@dataclass(eq=False, kw_only=True)
class LearningFeedbackRecordRoot(AggregateRoot):
    tenant_id: str
    feedback_ref: str
    run_ref: str
    success: bool
    notes: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        feedback_ref: str,
        run_ref: str,
        success: bool = True,
        notes: str = "",
    ) -> LearningFeedbackRecordRoot:
        if not tenant_id.strip() or not run_ref.strip():
            raise ValueError("ii.auto.feedback_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            feedback_ref=feedback_ref.strip(),
            run_ref=run_ref.strip(),
            success=success,
            notes=notes.strip(),
            status="recorded",
        )
        root.pending_events.append("LearningUpdated")
        root.history.append({"event": "LearningUpdated", "success": success})
        return root
