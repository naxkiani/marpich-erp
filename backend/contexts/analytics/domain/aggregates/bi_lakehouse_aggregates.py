"""P213-F aggregates — quality-gate invariants."""
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
class BiLakehouseProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.lakehouse.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.lakehouse.lakehouse_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("LakehouseZoneRegistered")
        root.pending_events.append("LakehouseCreatedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiAiDataFoundationRoot(AggregateRoot):
    tenant_id: str
    foundation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, foundation_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.lakehouse.ai_tenant_required")
        if not present:
            raise ValueError(
                "analytics.lakehouse.ai_data_foundation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            foundation_ref=foundation_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("FeatureDatasetCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDataMeshAlignedRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(cls, *, tenant_id: str, mesh_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.lakehouse.mesh_tenant_required")
        if not present:
            raise ValueError(
                "analytics.lakehouse.data_mesh_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("DataProductPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiStorageArchitectureRoot(AggregateRoot):
    tenant_id: str
    storage_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, storage_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.lakehouse.storage_tenant_required")
        if not present:
            raise ValueError(
                "analytics.lakehouse.storage_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            storage_ref=storage_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("DatasetRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiProcessingArchitectureRoot(AggregateRoot):
    tenant_id: str
    processing_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, processing_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.lakehouse.proc_tenant_required")
        if not present:
            raise ValueError(
                "analytics.lakehouse.data_processing_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            processing_ref=processing_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PipelineCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
