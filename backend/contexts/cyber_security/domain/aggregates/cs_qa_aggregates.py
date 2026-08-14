"""P210-O QA / Validation aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsQaAutomatedTestingRoot(AggregateRoot):
    tenant_id: str
    plan_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_plan(
        cls, *, tenant_id: str, plan_ref: str, automated: bool = True
    ) -> CsQaAutomatedTestingRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.tenant_required")
        if not automated:
            raise ValueError(
                "cyber_security.qa.security_testing_is_manual_only"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            automated=True,
            status="planned",
        )
        root.pending_events.append("TestStarted")
        root.pending_events.append("ManualOnlyTestingRejected")
        root.history.append({"event": "AutomatedTestPlanCreated"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class CsQaAdversarialValidationRoot(AggregateRoot):
    tenant_id: str
    exercise_ref: str
    adversarial: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def launch(
        cls, *, tenant_id: str, exercise_ref: str, adversarial: bool = True
    ) -> CsQaAdversarialValidationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.adv_tenant_required")
        if not adversarial:
            raise ValueError(
                "cyber_security.qa.no_adversarial_validation_exists"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            exercise_ref=exercise_ref.strip(),
            adversarial=True,
            status="running",
        )
        root.pending_events.append("TestStarted")
        root.pending_events.append("MissingAdversarialValidationRejected")
        root.history.append({"event": "RedTeamExerciseLaunched"})
        return root

    def is_absent(self) -> bool:
        return not self.adversarial


@dataclass(eq=False, kw_only=True)
class CsQaAiSystemsTestedRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    tested: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def test(
        cls, *, tenant_id: str, model_ref: str, tested: bool = True
    ) -> CsQaAiSystemsTestedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.ai_tenant_required")
        if not tested:
            raise ValueError(
                "cyber_security.qa.ai_systems_are_not_tested"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            model_ref=model_ref.strip(),
            tested=True,
            status="tested",
        )
        root.pending_events.append("TestCompleted")
        root.pending_events.append("UntestedAiRejected")
        root.history.append({"event": "AiSecurityTested"})
        return root

    def is_untested(self) -> bool:
        return not self.tested


@dataclass(eq=False, kw_only=True)
class CsQaComplianceVerificationRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    verifiable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls, *, tenant_id: str, evidence_ref: str, verifiable: bool = True
    ) -> CsQaComplianceVerificationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.comp_tenant_required")
        if not verifiable:
            raise ValueError(
                "cyber_security.qa.compliance_cannot_be_verified"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            verifiable=True,
            status="verified",
        )
        root.pending_events.append("ComplianceEvidenceGenerated")
        root.pending_events.append("UnverifiableComplianceRejected")
        root.history.append({"event": "ComplianceVerified"})
        return root

    def is_unverifiable(self) -> bool:
        return not self.verifiable


@dataclass(eq=False, kw_only=True)
class CsQaProductionReadinessRoot(AggregateRoot):
    tenant_id: str
    gate_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, gate_ref: str, defined: bool = True
    ) -> CsQaProductionReadinessRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.pr_tenant_required")
        if not defined:
            raise ValueError(
                "cyber_security.qa.production_readiness_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ReleaseApproved")
        root.pending_events.append("UndefinedReadinessRejected")
        root.history.append({"event": "ProductionReadinessDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class CsQaMeasurableControlsRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def measure(
        cls,
        *,
        tenant_id: str,
        control_ref: str,
        measurable: bool = True,
        score: float = 1.0,
    ) -> CsQaMeasurableControlsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.ctrl_tenant_required")
        if not measurable:
            raise ValueError(
                "cyber_security.qa.security_controls_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            measurable=True,
            score=float(score),
            status="measured",
        )
        root.pending_events.append("ControlValidated")
        root.pending_events.append("UnmeasurableControlRejected")
        root.history.append({"event": "ControlMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class CsQaAuditableEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls, *, tenant_id: str, evidence_ref: str, auditable: bool = True
    ) -> CsQaAuditableEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.ev_tenant_required")
        if not auditable:
            raise ValueError(
                "cyber_security.qa.test_evidence_cannot_be_audited"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            auditable=True,
            status="collected",
        )
        root.pending_events.append("TestCompleted")
        root.pending_events.append("UnauditableEvidenceRejected")
        root.history.append({"event": "EvidenceAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class CsQaReleaseApprovalRoot(AggregateRoot):
    tenant_id: str
    release_ref: str
    approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls, *, tenant_id: str, release_ref: str, approved: bool = True
    ) -> CsQaReleaseApprovalRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.qa.rel_tenant_required")
        if not approved:
            raise ValueError("cyber_security.qa.release_not_approved")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            release_ref=release_ref.strip(),
            approved=True,
            status="approved",
        )
        root.pending_events.append("ReleaseApproved")
        root.pending_events.append("UnapprovedReleaseRejected")
        root.history.append({"event": "ReleaseGatePassed"})
        return root
