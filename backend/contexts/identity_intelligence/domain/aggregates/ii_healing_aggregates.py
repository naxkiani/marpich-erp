"""P207-I Self-Healing Identity Fabric aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

REMEDIATION_LEVELS = frozenset({1, 2, 3})
FAILURE_KINDS = frozenset(
    {
        "missing_attributes",
        "incorrect_attributes",
        "duplicate_records",
        "failed_sync",
        "replication_delay",
        "provisioning_failure",
        "incorrect_permissions",
        "broken_entitlements",
        "policy_violations",
        "certification_issues",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityHealthProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    subject_ref: str
    health_score: float
    fully_manual: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def check(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        subject_ref: str,
        health_score: float = 0.8,
        fully_manual: bool = False,
    ) -> IdentityHealthProfileRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.tenant_required")
        if fully_manual:
            raise ValueError("ii.healing.recovery_fully_manual")
        if not (0 <= health_score <= 1):
            raise ValueError("ii.healing.health_score_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            subject_ref=subject_ref.strip(),
            health_score=health_score,
            fully_manual=False,
            status="checked",
        )
        root.history.append({"event": "HealthChecked"})
        return root

    def is_fully_manual(self) -> bool:
        return self.fully_manual

    def restore(self) -> None:
        self.status = "restored"
        self.pending_events.append("HealthRestored")
        self.history.append({"event": "HealthRestored"})


@dataclass(eq=False, kw_only=True)
class IdentityFailureIncidentRoot(AggregateRoot):
    tenant_id: str
    incident_ref: str
    subject_ref: str
    failure_kind: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls,
        *,
        tenant_id: str,
        incident_ref: str,
        subject_ref: str,
        failure_kind: str,
    ) -> IdentityFailureIncidentRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.incident_tenant_required")
        kind = failure_kind.strip().lower()
        if kind not in FAILURE_KINDS:
            raise ValueError("ii.healing.failure_kind_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            incident_ref=incident_ref.strip(),
            subject_ref=subject_ref.strip(),
            failure_kind=kind,
            status="detected",
        )
        root.pending_events.append("IdentityIssueDetected")
        root.history.append({"event": "IdentityIssueDetected"})
        return root


@dataclass(eq=False, kw_only=True)
class RootCauseAnalysisCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    incident_ref: str
    root_cause: str
    rca_present: bool
    via_ai: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        incident_ref: str,
        root_cause: str = "",
        rca_present: bool = True,
        via_ai: bool = True,
    ) -> RootCauseAnalysisCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.rca_tenant_required")
        if not rca_present or not root_cause.strip():
            raise ValueError("ii.healing.root_cause_analysis_missing")
        if not via_ai:
            raise ValueError("ii.healing.embeds_llm_sdk")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            incident_ref=incident_ref.strip(),
            root_cause=root_cause.strip(),
            rca_present=True,
            via_ai=True,
            status="identified",
        )
        root.pending_events.append("RootCauseIdentified")
        root.history.append({"event": "RootCauseIdentified"})
        return root

    def is_rca_missing(self) -> bool:
        return not self.rca_present or not self.root_cause.strip()


@dataclass(eq=False, kw_only=True)
class RemediationRunRoot(AggregateRoot):
    tenant_id: str
    run_ref: str
    incident_ref: str
    level: int
    governed: bool
    twin_simulated: bool
    auditable: bool
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
        incident_ref: str,
        level: int = 1,
        governed: bool = True,
        twin_simulated: bool = True,
        auditable: bool = True,
        hitl_approved: bool = True,
    ) -> RemediationRunRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.rem_tenant_required")
        if level not in REMEDIATION_LEVELS:
            raise ValueError("ii.healing.level_invalid")
        if not governed:
            raise ValueError("ii.healing.remediation_no_governance")
        if not twin_simulated:
            raise ValueError("ii.healing.digital_twin_simulation_absent")
        if not auditable:
            raise ValueError("ii.healing.actions_not_auditable")
        if level >= 2 and not hitl_approved:
            raise ValueError("ii.healing.skips_hitl_level_2_plus")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            incident_ref=incident_ref.strip(),
            level=level,
            governed=True,
            twin_simulated=True,
            auditable=True,
            hitl_approved=hitl_approved if level >= 2 else True,
            status="started",
        )
        root.pending_events.append("RecoveryStarted")
        if level >= 2:
            root.pending_events.append("RemediationApproved")
        root.history.append({"event": "RecoveryStarted"})
        return root

    def complete(self) -> None:
        self.status = "completed"
        self.pending_events.append("RecoveryCompleted")
        self.history.append({"event": "RecoveryCompleted"})

    def is_ungoverned(self) -> bool:
        return not self.governed

    def is_twin_sim_absent(self) -> bool:
        return not self.twin_simulated

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class RecoveryValidationRoot(AggregateRoot):
    tenant_id: str
    validation_ref: str
    run_ref: str
    security_validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        validation_ref: str,
        run_ref: str,
        security_validated: bool = True,
    ) -> RecoveryValidationRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.val_tenant_required")
        if not security_validated:
            raise ValueError("ii.healing.security_validation_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            validation_ref=validation_ref.strip(),
            run_ref=run_ref.strip(),
            security_validated=True,
            status="validated",
        )
        root.history.append({"event": "RecoveryValidated"})
        return root

    def is_security_undefined(self) -> bool:
        return not self.security_validated


@dataclass(eq=False, kw_only=True)
class HealingLearningRecordRoot(AggregateRoot):
    tenant_id: str
    record_ref: str
    incident_ref: str
    outcome: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        record_ref: str,
        incident_ref: str,
        outcome: str = "success",
    ) -> HealingLearningRecordRoot:
        if not tenant_id.strip() or not incident_ref.strip():
            raise ValueError("ii.healing.learning_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            record_ref=record_ref.strip(),
            incident_ref=incident_ref.strip(),
            outcome=outcome.strip(),
            status="recorded",
        )
        root.pending_events.append("LearningUpdated")
        root.history.append({"event": "LearningUpdated"})
        return root


@dataclass(eq=False, kw_only=True)
class HealingSecurityPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    security_validation_defined: bool
    actions_auditable: bool
    remediation_governed: bool
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
        security_validation_defined: bool = True,
        actions_auditable: bool = True,
        remediation_governed: bool = True,
    ) -> HealingSecurityPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.healing.sec_tenant_required")
        if not security_validation_defined:
            raise ValueError("ii.healing.security_validation_undefined")
        if not actions_auditable:
            raise ValueError("ii.healing.actions_not_auditable")
        if not remediation_governed:
            raise ValueError("ii.healing.remediation_no_governance")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            security_validation_defined=True,
            actions_auditable=True,
            remediation_governed=True,
            status="active",
        )
        root.history.append({"event": "HealingSecurityDefined"})
        return root
