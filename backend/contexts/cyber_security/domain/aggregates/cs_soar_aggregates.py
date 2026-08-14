"""P210-F Enterprise SOAR aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsSoarPlaybookVersionedRoot(AggregateRoot):
    tenant_id: str
    playbook_ref: str
    versioned: bool
    version: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        playbook_ref: str,
        versioned: bool = True,
        version: str = "1.0.0",
    ) -> CsSoarPlaybookVersionedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.tenant_required")
        if not versioned or not version.strip():
            raise ValueError("cyber_security.soar.playbooks_cannot_be_versioned")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            playbook_ref=playbook_ref.strip(),
            versioned=True,
            version=version.strip(),
            status="published",
        )
        root.pending_events.append("PlaybookVersionPublished")
        root.pending_events.append("UnversionedPlaybookRejected")
        root.history.append({"event": "PlaybookVersioned"})
        return root

    def is_unversioned(self) -> bool:
        return not self.versioned or not self.version


@dataclass(eq=False, kw_only=True)
class CsSoarAutomationAuditableRoot(AggregateRoot):
    tenant_id: str
    run_ref: str
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, run_ref: str, audited: bool = True
    ) -> CsSoarAutomationAuditableRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.audit_tenant_required")
        if not audited:
            raise ValueError("cyber_security.soar.automation_not_auditable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            audited=True,
            status="completed",
        )
        root.pending_events.append("AutomationCompleted")
        root.pending_events.append("UnauditedAutomationRejected")
        root.history.append({"event": "AutomationAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class CsSoarHumanApprovalRoot(AggregateRoot):
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
    ) -> CsSoarHumanApprovalRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.hitl_tenant_required")
        if not available or not via_workflow:
            raise ValueError("cyber_security.soar.human_approval_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            gate_ref=gate_ref.strip(),
            available=True,
            via_workflow=True,
            status="pending",
        )
        root.pending_events.append("ResponseApproved")
        root.history.append({"event": "HumanApprovalAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available or not self.via_workflow


@dataclass(eq=False, kw_only=True)
class CsSoarExplainableAiRoot(AggregateRoot):
    tenant_id: str
    advisory_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def advise(
        cls, *, tenant_id: str, advisory_ref: str, explainable: bool = True
    ) -> CsSoarExplainableAiRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.ai_tenant_required")
        if not explainable:
            raise ValueError(
                "cyber_security.soar.ai_recommendations_not_explainable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            advisory_ref=advisory_ref.strip(),
            explainable=True,
            status="advised",
        )
        root.pending_events.append("UnexplainableAiRejected")
        root.history.append({"event": "ExplainableAiAdvisory"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class CsSoarRollbackRoot(AggregateRoot):
    tenant_id: str
    plan_ref: str
    rollback_available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        plan_ref: str,
        rollback_available: bool = True,
    ) -> CsSoarRollbackRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.rollback_tenant_required")
        if not rollback_available:
            raise ValueError("cyber_security.soar.rollback_capability_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            rollback_available=True,
            status="ready",
        )
        root.pending_events.append("RollbackCompleted")
        root.history.append({"event": "RollbackEnabled"})
        return root

    def is_absent(self) -> bool:
        return not self.rollback_available


@dataclass(eq=False, kw_only=True)
class CsSoarLooseConnectorsRoot(AggregateRoot):
    tenant_id: str
    connector_ref: str
    tightly_coupled: bool
    via_integration: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        connector_ref: str,
        tightly_coupled: bool = False,
        via_integration: bool = True,
    ) -> CsSoarLooseConnectorsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.conn_tenant_required")
        if tightly_coupled or not via_integration:
            raise ValueError("cyber_security.soar.connectors_tightly_coupled")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            connector_ref=connector_ref.strip(),
            tightly_coupled=False,
            via_integration=True,
            status="bound",
        )
        root.pending_events.append("TightCouplingRejected")
        root.history.append({"event": "LooseConnectorBound"})
        return root

    def is_tightly_coupled(self) -> bool:
        return self.tightly_coupled or not self.via_integration


@dataclass(eq=False, kw_only=True)
class CsSoarEvidencePreservedRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    preserved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def preserve(
        cls, *, tenant_id: str, evidence_ref: str, preserved: bool = True
    ) -> CsSoarEvidencePreservedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.evidence_tenant_required")
        if not preserved:
            raise ValueError(
                "cyber_security.soar.incident_evidence_cannot_be_preserved"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            preserved=True,
            status="preserved",
        )
        root.pending_events.append("EvidencePreserved")
        root.history.append({"event": "EvidencePreserved"})
        return root

    def is_unpreservable(self) -> bool:
        return not self.preserved


@dataclass(eq=False, kw_only=True)
class CsSoarPlaybookExecutionRoot(AggregateRoot):
    tenant_id: str
    execution_ref: str
    playbook_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, execution_ref: str, playbook_ref: str
    ) -> CsSoarPlaybookExecutionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soar.exec_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            execution_ref=execution_ref.strip(),
            playbook_ref=playbook_ref.strip(),
            status="running",
        )
        root.pending_events.append("PlaybookExecuted")
        root.pending_events.append("AutomationStarted")
        root.history.append({"event": "PlaybookExecutionStarted"})
        return root
