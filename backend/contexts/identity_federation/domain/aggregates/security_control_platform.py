"""Security control, risk, threat, compliance posture aggregates (P200-B9)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecurityControl(AggregateRoot):
    tenant_id: str
    control_ref: str
    name: str
    security_level: int = 1
    classification: str = "internal"
    baseline: dict = field(default_factory=dict)
    rules: list[dict] = field(default_factory=list)
    enabled: bool = True
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        control_ref: str,
        name: str,
        security_level: int = 1,
        classification: str = "internal",
        baseline: dict | None = None,
        rules: list[dict] | None = None,
    ) -> SecurityControl:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            control_ref=control_ref,
            name=name or control_ref,
            security_level=max(0, min(3, int(security_level))),
            classification=classification or "internal",
            baseline=baseline or {},
            rules=list(rules or []),
            enabled=True,
            version=1,
        )

    def activate_policy(self, *, policy: dict) -> None:
        if not policy.get("policy_key"):
            raise ValueError("security.policy_key_required")
        # Never embed hardcoded business limits — policy_key + conditions only
        self.rules.append({**policy, "activated_at": datetime.now(UTC).isoformat()})
        self.version += 1

    def to_dict(self) -> dict:
        return {
            "control_ref": self.control_ref,
            "name": self.name,
            "security_level": self.security_level,
            "classification": self.classification,
            "baseline": self.baseline,
            "rules": self.rules,
            "enabled": self.enabled,
            "version": self.version,
        }


@dataclass(eq=False, kw_only=True)
class RiskAssessment(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    subject_type: str
    subject_id: str
    risk_score: int = 0
    risk_level: str = "low"
    signals: dict = field(default_factory=dict)
    factors: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "assessment_ref": self.assessment_ref,
            "subject_type": self.subject_type,
            "subject_id": self.subject_id,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "signals": self.signals,
            "factors": self.factors,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ThreatEvent(AggregateRoot):
    tenant_id: str
    threat_ref: str
    threat_type: str
    severity: str = "medium"
    status: str = "open"  # open|mitigated|false_positive
    indicators: dict = field(default_factory=dict)
    mitigation: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mitigate(self, *, action: str, notes: str = "") -> None:
        self.status = "mitigated"
        self.mitigation = {
            "action": action,
            "notes": notes,
            "at": datetime.now(UTC).isoformat(),
        }

    def to_dict(self) -> dict:
        return {
            "threat_ref": self.threat_ref,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "status": self.status,
            "indicators": self.indicators,
            "mitigation": self.mitigation,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CompliancePostureSnapshot(AggregateRoot):
    tenant_id: str
    assessment_ref: str
    frameworks: list[str] = field(default_factory=list)
    controls_passed: int = 0
    controls_failed: int = 0
    violations: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    status: str = "in_progress"  # in_progress|passed|failed
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        return {
            "assessment_ref": self.assessment_ref,
            "frameworks": self.frameworks,
            "controls_passed": self.controls_passed,
            "controls_failed": self.controls_failed,
            "violations": self.violations,
            "evidence_refs": self.evidence_refs,
            "status": self.status,
            "platform_owner": "compliance",
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SecurityException(AggregateRoot):
    tenant_id: str
    exception_ref: str
    reason: str
    scope: list[str] = field(default_factory=list)
    status: str = "approved"
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(days=7))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def revoke(self, *, reason: str = "") -> None:
        self.status = "revoked"
        self.scope = []

    def to_dict(self) -> dict:
        return {
            "exception_ref": self.exception_ref,
            "reason": self.reason,
            "scope": self.scope,
            "status": self.status,
            "expires_at": self.expires_at.isoformat(),
        }
