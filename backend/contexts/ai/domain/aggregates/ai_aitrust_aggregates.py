"""P214-P aggregates — quality-gate invariants."""
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
class AitrustPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.tenant_required")
        if not present:
            raise ValueError(
                "ai.aitrust.enterprise_ai_governance_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AIPolicyCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ComplianceRoot(AggregateRoot):
    tenant_id: str
    compliance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, compliance_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.comp_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.ai_compliance_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            compliance_ref=compliance_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ComplianceValidatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AuditRoot(AggregateRoot):
    tenant_id: str
    audit_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, audit_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.audit_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.ai_audit_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            audit_ref=audit_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AuditCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustRoot(AggregateRoot):
    tenant_id: str
    trust_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.trust_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.ai_trust_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            trust_ref=trust_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrustScoreCalculatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class RiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.risk_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.ai_risk_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            risk_ref=risk_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RiskDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, policy_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.policy_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.ai_policy_management_is_missing")
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
class CertificationRoot(AggregateRoot):
    tenant_id: str
    certification_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, certification_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.cert_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.certification_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            certification_ref=certification_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("CertificationApprovedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrustDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aitrust.twin_tenant_required")
        if not present:
            raise ValueError("ai.aitrust.governance_digital_twin_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrustScoreCalculatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
