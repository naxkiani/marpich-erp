"""P210-M AI Governance aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsGovAiInventoryRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    inventoried: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, model_ref: str, inventoried: bool = True
    ) -> CsGovAiInventoryRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.tenant_required")
        if not inventoried:
            raise ValueError(
                "cyber_security.gov.ai_models_cannot_be_inventoried"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            inventoried=True,
            status="registered",
        )
        root.pending_events.append("AIModelRegistered")
        root.pending_events.append("UninventoriedModelRejected")
        root.history.append({"event": "AiModelInventoried"})
        return root

    def is_uninventoried(self) -> bool:
        return not self.inventoried


@dataclass(eq=False, kw_only=True)
class CsGovAuditableDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def audit(
        cls, *, tenant_id: str, decision_ref: str, auditable: bool = True
    ) -> CsGovAuditableDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.audit_tenant_required")
        if not auditable:
            raise ValueError(
                "cyber_security.gov.ai_decisions_cannot_be_audited"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            auditable=True,
            status="audited",
        )
        root.pending_events.append("AuditCompleted")
        root.pending_events.append("UnauditableDecisionRejected")
        root.history.append({"event": "AiDecisionAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class CsGovMeasurableRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assess(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        measurable: bool = True,
        score: float = 0.5,
    ) -> CsGovMeasurableRiskRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.risk_tenant_required")
        if not measurable:
            raise ValueError(
                "cyber_security.gov.ai_risks_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            measurable=True,
            score=score,
            status="assessed",
        )
        root.pending_events.append("AIRiskDetected")
        root.pending_events.append("UnmeasurableRiskRejected")
        root.history.append({"event": "AiRiskMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class CsGovAgentGovernanceRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    governed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def govern(
        cls, *, tenant_id: str, agent_ref: str, governed: bool = True
    ) -> CsGovAgentGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.agent_tenant_required")
        if not governed:
            raise ValueError(
                "cyber_security.gov.ai_agents_operate_without_governance"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            governed=True,
            status="governed",
        )
        root.pending_events.append("AgentActionExecuted")
        root.pending_events.append("UngovernedAgentRejected")
        root.history.append({"event": "AgentGoverned"})
        return root

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class CsGovPolicyEnforcementRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    enforceable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, policy_ref: str, enforceable: bool = True
    ) -> CsGovPolicyEnforcementRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.policy_tenant_required")
        if not enforceable:
            raise ValueError(
                "cyber_security.gov.policies_cannot_be_enforced"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            enforceable=True,
            status="enforced",
        )
        root.pending_events.append("AIPolicyUpdated")
        root.pending_events.append("PolicyViolationDetected")
        root.pending_events.append("UnenforceablePolicyRejected")
        root.history.append({"event": "PolicyEnforced"})
        return root

    def is_unenforceable(self) -> bool:
        return not self.enforceable


@dataclass(eq=False, kw_only=True)
class CsGovComplianceEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    generatable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        generatable: bool = True,
    ) -> CsGovComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.evidence_tenant_required")
        if not generatable:
            raise ValueError(
                "cyber_security.gov.compliance_evidence_cannot_be_generated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            generatable=True,
            status="generated",
        )
        root.pending_events.append("ComplianceReportGenerated")
        root.pending_events.append("UngeneratableEvidenceRejected")
        root.history.append({"event": "ComplianceEvidenceGenerated"})
        return root

    def is_ungeneratable(self) -> bool:
        return not self.generatable


@dataclass(eq=False, kw_only=True)
class CsGovHumanOversightRoot(AggregateRoot):
    tenant_id: str
    gate_ref: str
    available: bool
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
        available: bool = True,
        via_workflow: bool = True,
    ) -> CsGovHumanOversightRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.hitl_tenant_required")
        if not available or not via_workflow:
            raise ValueError(
                "cyber_security.gov.human_oversight_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            available=True,
            via_workflow=True,
            status="pending",
        )
        root.pending_events.append("AbsentOversightRejected")
        root.history.append({"event": "HumanOversightRequired"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available or not self.via_workflow


@dataclass(eq=False, kw_only=True)
class CsGovModelRegisteredRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls, *, tenant_id: str, model_ref: str
    ) -> CsGovModelRegisteredRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.gov.approve_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            status="approved",
        )
        root.pending_events.append("AIModelApproved")
        root.history.append({"event": "AiModelApproved"})
        return root
