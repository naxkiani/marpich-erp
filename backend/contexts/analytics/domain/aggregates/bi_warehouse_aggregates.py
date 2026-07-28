"""P213-E aggregates — quality-gate invariants."""
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
class BiWarehouseProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.warehouse.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.warehouse.warehouse_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("WarehouseModelPublished")
        root.pending_events.append("WarehouseCreatedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiDimensionalModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.warehouse.model_tenant_required")
        if not present:
            raise ValueError(
                "analytics.warehouse.dimensional_modeling_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("ModelCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDataIntegrationRoot(AggregateRoot):
    tenant_id: str
    pipeline_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, pipeline_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.warehouse.ingest_tenant_required")
        if not present:
            raise ValueError(
                "analytics.warehouse.data_integration_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pipeline_ref=pipeline_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DataIngestionStartedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiSemanticLayerRoot(AggregateRoot):
    tenant_id: str
    layer_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, layer_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.warehouse.semantic_tenant_required")
        if not present:
            raise ValueError(
                "analytics.warehouse.semantic_layer_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            layer_ref=layer_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("AnalyticsReadyEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiHistoricalDataRoot(AggregateRoot):
    tenant_id: str
    history_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def snapshot(
        cls, *, tenant_id: str, history_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.warehouse.hist_tenant_required")
        if not present:
            raise ValueError(
                "analytics.warehouse.historical_data_management_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            history_ref=history_ref.strip(),
            present=True,
            status="snapshotted",
        )
        root.pending_events.append("SnapshotGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
