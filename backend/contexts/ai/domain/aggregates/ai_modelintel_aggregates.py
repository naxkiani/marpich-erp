"""P214-L aggregates — quality-gate invariants."""
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
class ModelintelPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.tenant_required")
        if not present:
            raise ValueError("ai.modelintel.enterprise_ai_model_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelRegistryRoot(AggregateRoot):
    tenant_id: str
    registry_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, registry_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.registry_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_registry_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            registry_ref=registry_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelLifecycleRoot(AggregateRoot):
    tenant_id: str
    lifecycle_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.lifecycle_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_lifecycle_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lifecycle_ref=lifecycle_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrainingCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelEvaluationRoot(AggregateRoot):
    tenant_id: str
    evaluation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, evaluation_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.eval_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_evaluation_intelligence_is_missing")
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
class ModelMonitoringRoot(AggregateRoot):
    tenant_id: str
    monitoring_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, monitoring_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.mon_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_monitoring_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            monitoring_ref=monitoring_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelPerformanceChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelDriftRoot(AggregateRoot):
    tenant_id: str
    drift_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, drift_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.drift_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.drift_detection_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            drift_ref=drift_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DriftDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.risk_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_risk_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            risk_ref=risk_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EvaluationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ModelDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.modelintel.twin_tenant_required")
        if not present:
            raise ValueError("ai.modelintel.model_digital_twin_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OptimizationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
