"""P211-K Intelligence graph aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsKnownOriginRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    known: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, asset_ref: str, known: bool = True
    ) -> DsKnownOriginRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.tenant_required")
        if not known:
            raise ValueError(
                "data_security.intelligence.data_origin_is_unknown"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            known=True,
            status="known",
        )
        root.pending_events.append("DataAssetRegistered")
        root.pending_events.append("UnknownOriginRejected")
        root.history.append({"event": "OriginKnown"})
        return root

    def is_unknown(self) -> bool:
        return not self.known


@dataclass(eq=False, kw_only=True)
class DsVisibleMovementRoot(AggregateRoot):
    tenant_id: str
    lineage_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def track(
        cls, *, tenant_id: str, lineage_ref: str, visible: bool = True
    ) -> DsVisibleMovementRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.mov_tenant_required")
        if not visible:
            raise ValueError(
                "data_security.intelligence.data_movement_is_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lineage_ref=lineage_ref.strip(),
            visible=True,
            status="visible",
        )
        root.pending_events.append("LineageCreated")
        root.pending_events.append("InvisibleMovementRejected")
        root.history.append({"event": "MovementVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsCompleteMetadataRoot(AggregateRoot):
    tenant_id: str
    metadata_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls, *, tenant_id: str, metadata_ref: str, complete: bool = True
    ) -> DsCompleteMetadataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.meta_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.intelligence.metadata_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            metadata_ref=metadata_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("MetadataCollected")
        root.pending_events.append("IncompleteMetadataRejected")
        root.history.append({"event": "MetadataComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsQueryableRelationshipsRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    queryable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def update(
        cls, *, tenant_id: str, graph_ref: str, queryable: bool = True
    ) -> DsQueryableRelationshipsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.rel_tenant_required")
        if not queryable:
            raise ValueError(
                "data_security.intelligence.relationships_cannot_be_queried"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            graph_ref=graph_ref.strip(),
            queryable=True,
            status="queryable",
        )
        root.pending_events.append("RelationshipUpdated")
        root.pending_events.append("KnowledgeGraphUpdated")
        root.pending_events.append("UnqueryableRelationshipsRejected")
        root.history.append({"event": "RelationshipsQueryable"})
        return root

    def is_unqueryable(self) -> bool:
        return not self.queryable


@dataclass(eq=False, kw_only=True)
class DsImpactAnalysisRoot(AggregateRoot):
    tenant_id: str
    analysis_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls, *, tenant_id: str, analysis_ref: str, available: bool = True
    ) -> DsImpactAnalysisRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.imp_tenant_required")
        if not available:
            raise ValueError(
                "data_security.intelligence.impact_analysis_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            analysis_ref=analysis_ref.strip(),
            available=True,
            status="available",
        )
        root.pending_events.append("ImpactDetected")
        root.pending_events.append("UnavailableImpactAnalysisRejected")
        root.history.append({"event": "ImpactAnalysisAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsAiReasoningRoot(AggregateRoot):
    tenant_id: str
    reasoning_ref: str
    capable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def reason(
        cls, *, tenant_id: str, reasoning_ref: str, capable: bool = True
    ) -> DsAiReasoningRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.ai_tenant_required")
        if not capable:
            raise ValueError(
                "data_security.intelligence.ai_cannot_reason_over_data_context"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            reasoning_ref=reasoning_ref.strip(),
            capable=True,
            status="capable",
        )
        root.pending_events.append("KnowledgeGraphUpdated")
        root.pending_events.append("UnableAiReasoningRejected")
        root.history.append({"event": "AiReasoningCapable"})
        return root

    def is_unable(self) -> bool:
        return not self.capable


@dataclass(eq=False, kw_only=True)
class DsLineageBrokenRoot(AggregateRoot):
    tenant_id: str
    break_ref: str
    detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, break_ref: str, detected: bool = True
    ) -> DsLineageBrokenRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.brk_tenant_required")
        if not detected:
            raise ValueError("data_security.intelligence.lineage_break_not_detected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            break_ref=break_ref.strip(),
            detected=True,
            status="detected",
        )
        root.pending_events.append("LineageBroken")
        root.history.append({"event": "LineageBroken"})
        return root


@dataclass(eq=False, kw_only=True)
class DsSchemaChangedRoot(AggregateRoot):
    tenant_id: str
    schema_ref: str
    changed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls, *, tenant_id: str, schema_ref: str, changed: bool = True
    ) -> DsSchemaChangedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.intelligence.sch_tenant_required")
        if not changed:
            raise ValueError("data_security.intelligence.schema_not_changed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            schema_ref=schema_ref.strip(),
            changed=True,
            status="changed",
        )
        root.pending_events.append("SchemaChanged")
        root.history.append({"event": "SchemaChanged"})
        return root
