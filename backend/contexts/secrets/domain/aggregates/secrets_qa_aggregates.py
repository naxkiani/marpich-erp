"""P209-O Testing, Governance, Security Validation & DoD aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsQaSecurityTestingRoot(AggregateRoot):
    """Security testing must be complete."""

    tenant_id: str
    plan_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_plan(
        cls,
        *,
        tenant_id: str,
        plan_ref: str,
        complete: bool = True,
    ) -> SecretsQaSecurityTestingRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.sec_tenant_required")
        if not complete:
            raise ValueError("secrets.qa.security_testing_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("SecurityTestingComplete")
        root.pending_events.append("TestCompleted")
        root.history.append({"event": "SecurityTestingComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsQaComplianceEvidenceRoot(AggregateRoot):
    """Compliance evidence must be available."""

    tenant_id: str
    evidence_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        available: bool = True,
    ) -> SecretsQaComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.ev_tenant_required")
        if not available:
            raise ValueError("secrets.qa.compliance_evidence_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            available=True,
            status="available",
        )
        root.pending_events.append("ComplianceEvidenceAvailable")
        root.pending_events.append("ComplianceValidated")
        root.history.append({"event": "ComplianceEvidenceAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class SecretsQaCryptoControlsRoot(AggregateRoot):
    """Cryptographic controls must be validated."""

    tenant_id: str
    control_ref: str
    validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        control_ref: str,
        validated: bool = True,
    ) -> SecretsQaCryptoControlsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.ctrl_tenant_required")
        if not validated:
            raise ValueError("secrets.qa.cryptographic_controls_not_validated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            validated=True,
            status="validated",
        )
        root.pending_events.append("CryptoControlsValidated")
        root.history.append({"event": "CryptoControlsValidated"})
        return root

    def is_unvalidated(self) -> bool:
        return not self.validated


@dataclass(eq=False, kw_only=True)
class SecretsQaProductionReadinessRoot(AggregateRoot):
    """Production readiness must be defined."""

    tenant_id: str
    checklist_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        checklist_ref: str,
        defined: bool = True,
    ) -> SecretsQaProductionReadinessRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.ready_tenant_required")
        if not defined:
            raise ValueError("secrets.qa.production_readiness_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            checklist_ref=checklist_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ProductionReadinessDefined")
        root.history.append({"event": "ProductionReadinessDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class SecretsQaGovernanceOwnershipRoot(AggregateRoot):
    """Governance ownership must not be missing."""

    tenant_id: str
    body_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls,
        *,
        tenant_id: str,
        body_ref: str,
        present: bool = True,
    ) -> SecretsQaGovernanceOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.gov_tenant_required")
        if not present:
            raise ValueError("secrets.qa.governance_ownership_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            body_ref=body_ref.strip(),
            present=True,
            status="assigned",
        )
        root.pending_events.append("GovernanceOwnershipPresent")
        root.history.append({"event": "GovernanceOwnershipPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsQaAuditTrailsRoot(AggregateRoot):
    """Audit trails must be complete."""

    tenant_id: str
    trail_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_trail(
        cls,
        *,
        tenant_id: str,
        trail_ref: str,
        complete: bool = True,
    ) -> SecretsQaAuditTrailsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.audit_tenant_required")
        if not complete:
            raise ValueError("secrets.qa.audit_trails_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trail_ref=trail_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("AuditTrailsComplete")
        root.history.append({"event": "AuditTrailsComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsQaDeployGateRoot(AggregateRoot):
    """Security failures must be able to block deployment."""

    tenant_id: str
    gate_ref: str
    can_block: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        gate_ref: str,
        can_block: bool = True,
    ) -> SecretsQaDeployGateRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.gate_tenant_required")
        if not can_block:
            raise ValueError(
                "secrets.qa.security_failures_cannot_block_deployment"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            can_block=True,
            status="enforced",
        )
        root.pending_events.append("DeployGateEnforced")
        root.pending_events.append("DeploymentRejected")
        root.history.append({"event": "DeployGateEnforced"})
        return root

    def cannot_block(self) -> bool:
        return not self.can_block


@dataclass(eq=False, kw_only=True)
class SecretsQaDefinitionOfDoneRoot(AggregateRoot):
    """Enterprise Definition of Done for cryptographic trust fabric."""

    tenant_id: str
    series_ref: str
    met: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def meet(
        cls,
        *,
        tenant_id: str,
        series_ref: str = "P209",
        met: bool = True,
    ) -> SecretsQaDefinitionOfDoneRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.qa.dod_tenant_required")
        if not met:
            raise ValueError("secrets.qa.production_readiness_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            series_ref=series_ref.strip(),
            met=True,
            status="met",
        )
        root.pending_events.append("DefinitionOfDoneMet")
        root.pending_events.append("ReleaseApproved")
        root.history.append({"event": "DefinitionOfDoneMet"})
        return root

    def is_unmet(self) -> bool:
        return not self.met
