"""P214-H aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class GovernancePlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.tenant_required")
        if not present:
            raise ValueError(
                "ai.governance.enterprise_ai_governance_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIGovernancePolicyCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.policy_tenant_required")
        if not present:
            raise ValueError("ai.governance.ai_policy_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            policy_ref=policy_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIPolicyCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.risk_tenant_required")
        if not present:
            raise ValueError(
                "ai.governance.ai_risk_management_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            risk_ref=risk_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIRiskAssessmentCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResponsibleAiRoot(AggregateRoot):
    tenant_id: str
    ethics_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.ethics_tenant_required")
        if not present:
            raise ValueError("ai.governance.responsible_ai_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ethics_ref=ethics_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIComplianceValidatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiTrustRoot(AggregateRoot):
    tenant_id: str
    trust_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.trust_tenant_required")
        if not present:
            raise ValueError("ai.governance.ai_trust_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            trust_ref=trust_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AITrustScoreChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GovernanceTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.governance.twin_tenant_required")
        if not present:
            raise ValueError("ai.governance.governance_digital_twin_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIAuditCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
