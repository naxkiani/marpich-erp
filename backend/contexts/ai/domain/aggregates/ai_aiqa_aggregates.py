"""P214-O aggregates — quality-gate invariants."""
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
class AiqaPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.tenant_required")
        if not present:
            raise ValueError("ai.aiqa.enterprise_ai_testing_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TestCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvaluationRoot(AggregateRoot):
    tenant_id: str
    evaluation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, evaluation_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.eval_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.ai_evaluation_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            evaluation_ref=evaluation_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EvaluationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ValidationRoot(AggregateRoot):
    tenant_id: str
    validation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, validation_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.val_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.ai_validation_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            validation_ref=validation_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EvaluationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SafetyTestingRoot(AggregateRoot):
    tenant_id: str
    safety_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.safety_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.ai_safety_testing_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            safety_ref=safety_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("SafetyViolationDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class RegressionRoot(AggregateRoot):
    tenant_id: str
    regression_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, regression_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.reg_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.ai_regression_testing_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            regression_ref=regression_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RegressionDetectedEvent")
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
        tid = _tid(tenant_id, "ai.aiqa.cert_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.ai_certification_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            certification_ref=certification_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("CertificationGrantedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class QualityIntelligenceRoot(AggregateRoot):
    tenant_id: str
    quality_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, quality_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.qi_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.quality_intelligence_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            quality_ref=quality_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("QualityScoreChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class QualityDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiqa.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiqa.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("QualityScoreChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
