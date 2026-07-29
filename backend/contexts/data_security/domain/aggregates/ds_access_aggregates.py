"""P211-H Access governance aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsVisiblePermissionsRoot(AggregateRoot):
    tenant_id: str
    permission_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls, *, tenant_id: str, permission_ref: str, visible: bool = True
    ) -> DsVisiblePermissionsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.tenant_required")
        if not visible:
            raise ValueError(
                "data_security.access.data_permissions_are_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            permission_ref=permission_ref.strip(),
            visible=True,
            status="visible",
        )
        root.pending_events.append("AccessGranted")
        root.pending_events.append("InvisiblePermissionsRejected")
        root.history.append({"event": "PermissionsVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsDefinedOwnershipRoot(AggregateRoot):
    tenant_id: str
    owner_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assign(
        cls, *, tenant_id: str, owner_ref: str, defined: bool = True
    ) -> DsDefinedOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.own_tenant_required")
        if not defined or not owner_ref.strip():
            raise ValueError("data_security.access.ownership_is_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            owner_ref=owner_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("AccessApproved")
        root.pending_events.append("UndefinedOwnershipRejected")
        root.history.append({"event": "OwnershipDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsAutomatedReviewRoot(AggregateRoot):
    tenant_id: str
    review_ref: str
    automated_path: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def review(
        cls,
        *,
        tenant_id: str,
        review_ref: str,
        automated_path: bool = True,
    ) -> DsAutomatedReviewRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.rev_tenant_required")
        if not automated_path:
            raise ValueError(
                "data_security.access.access_reviews_are_manual_only"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            review_ref=review_ref.strip(),
            automated_path=True,
            status="completed",
        )
        root.pending_events.append("AccessReviewCompleted")
        root.pending_events.append("ManualOnlyReviewRejected")
        root.history.append({"event": "ReviewAutomated"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated_path


@dataclass(eq=False, kw_only=True)
class DsRiskEvaluationRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def evaluate(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        present: bool = True,
        score: float = 0.4,
    ) -> DsRiskEvaluationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.risk_tenant_required")
        if not present:
            raise ValueError(
                "data_security.access.risk_evaluation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            present=True,
            score=score,
            status="evaluated",
        )
        root.pending_events.append("RiskDetected")
        root.pending_events.append("MissingRiskEvaluationRejected")
        root.history.append({"event": "RiskEvaluated"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsManagedAiAccessRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def govern(
        cls, *, tenant_id: str, agent_ref: str, managed: bool = True
    ) -> DsManagedAiAccessRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.ai_tenant_required")
        if not managed:
            raise ValueError("data_security.access.ai_access_is_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("AccessGranted")
        root.pending_events.append("UnmanagedAiAccessRejected")
        root.history.append({"event": "AiAccessManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class DsLeastPrivilegeRoot(AggregateRoot):
    tenant_id: str
    entitlement_ref: str
    enforceable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        entitlement_ref: str,
        enforceable: bool = True,
    ) -> DsLeastPrivilegeRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.lp_tenant_required")
        if not enforceable:
            raise ValueError(
                "data_security.access.least_privilege_cannot_be_enforced"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            entitlement_ref=entitlement_ref.strip(),
            enforceable=True,
            status="enforced",
        )
        root.pending_events.append("AccessRevoked")
        root.pending_events.append("UnenforceableLeastPrivilegeRejected")
        root.history.append({"event": "LeastPrivilegeEnforced"})
        return root

    def is_unenforceable(self) -> bool:
        return not self.enforceable


@dataclass(eq=False, kw_only=True)
class DsAuditableDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def decide(
        cls, *, tenant_id: str, decision_ref: str, auditable: bool = True
    ) -> DsAuditableDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.aud_tenant_required")
        if not auditable:
            raise ValueError(
                "data_security.access.authorization_decisions_are_not_auditable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            auditable=True,
            status="audited",
        )
        root.pending_events.append("AccessApproved")
        root.pending_events.append("AccessDenied")
        root.pending_events.append("UnauditableDecisionRejected")
        root.history.append({"event": "DecisionAuditable"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class DsAccessRequestRoot(AggregateRoot):
    tenant_id: str
    request_ref: str
    requested: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def request(
        cls, *, tenant_id: str, request_ref: str, requested: bool = True
    ) -> DsAccessRequestRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.access.req_tenant_required")
        if not requested:
            raise ValueError("data_security.access.request_not_created")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            request_ref=request_ref.strip(),
            requested=True,
            status="requested",
        )
        root.pending_events.append("AccessRequested")
        root.history.append({"event": "AccessRequested"})
        return root
