"""P214-K aggregates — quality-gate invariants."""
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
class AidataPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.tenant_required")
        if not present:
            raise ValueError("ai.aidata.enterprise_ai_data_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DatasetCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DatasetManagementRoot(AggregateRoot):
    tenant_id: str
    dataset_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, dataset_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.dataset_tenant_required")
        if not present:
            raise ValueError("ai.aidata.ai_dataset_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            dataset_ref=dataset_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DatasetApprovedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FeatureEngineeringRoot(AggregateRoot):
    tenant_id: str
    feature_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, feature_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.fe_tenant_required")
        if not present:
            raise ValueError("ai.aidata.feature_engineering_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            feature_ref=feature_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("FeatureCreatedEvent")
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
        tid = _tid(tenant_id, "ai.aidata.store_tenant_required")
        if not present:
            raise ValueError("ai.aidata.feature_store_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            store_ref=store_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("FeaturePublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TrainingDataRoot(AggregateRoot):
    tenant_id: str
    training_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, training_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.training_tenant_required")
        if not present:
            raise ValueError("ai.aidata.training_data_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            training_ref=training_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("TrainingDataPreparedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SyntheticDataRoot(AggregateRoot):
    tenant_id: str
    synthetic_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, synthetic_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.synthetic_tenant_required")
        if not present:
            raise ValueError("ai.aidata.synthetic_data_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            synthetic_ref=synthetic_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("SyntheticDataGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DataQualityRoot(AggregateRoot):
    tenant_id: str
    quality_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, quality_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.quality_tenant_required")
        if not present:
            raise ValueError("ai.aidata.data_quality_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            quality_ref=quality_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DataQualityChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DataLineageRoot(AggregateRoot):
    tenant_id: str
    lineage_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, lineage_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aidata.lineage_tenant_required")
        if not present:
            raise ValueError("ai.aidata.ai_data_lineage_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lineage_ref=lineage_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DatasetCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
