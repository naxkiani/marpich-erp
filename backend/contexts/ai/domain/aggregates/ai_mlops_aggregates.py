"""P214-D aggregates — quality-gate invariants."""
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
class MlopsPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mlops.tenant_required")
        if not present:
            raise ValueError("ai.mlops.enterprise_mlops_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ExperimentCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MlLifecycleRoot(AggregateRoot):
    tenant_id: str
    lifecycle_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, lifecycle_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.mlops.lifecycle_tenant_required")
        if not present:
            raise ValueError("ai.mlops.ml_lifecycle_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lifecycle_ref=lifecycle_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrainingStartedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FeatureStoreRoot(AggregateRoot):
    tenant_id: str
    store_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, store_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mlops.feature_tenant_required")
        if not present:
            raise ValueError("ai.mlops.feature_store_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            store_ref=store_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrainingStartedEvent")
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
    def enable(
        cls, *, tenant_id: str, registry_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.mlops.registry_tenant_required")
        if not present:
            raise ValueError("ai.mlops.model_registry_is_missing")
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
class ModelMonitoringRoot(AggregateRoot):
    tenant_id: str
    monitoring_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, monitoring_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.mlops.monitoring_tenant_required")
        if not present:
            raise ValueError("ai.mlops.monitoring_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            monitoring_ref=monitoring_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelDriftDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ContinuousTrainingRoot(AggregateRoot):
    tenant_id: str
    retrain_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, retrain_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.mlops.retrain_tenant_required")
        if not present:
            raise ValueError("ai.mlops.continuous_training_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            retrain_ref=retrain_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RetrainingStartedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
