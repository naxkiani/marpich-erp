"""P211-D Discovery / inventory aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsDiscoverableAssetsRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    discoverable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, asset_ref: str, discoverable: bool = True
    ) -> DsDiscoverableAssetsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.tenant_required")
        if not discoverable:
            raise ValueError(
                "data_security.discovery.data_assets_cannot_be_discovered"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            discoverable=True,
            status="discovered",
        )
        root.pending_events.append("DataAssetDiscovered")
        root.pending_events.append("UndiscoverableAssetRejected")
        root.history.append({"event": "AssetDiscovered"})
        return root

    def is_undiscoverable(self) -> bool:
        return not self.discoverable


@dataclass(eq=False, kw_only=True)
class DsCompleteInventoryRoot(AggregateRoot):
    tenant_id: str
    inventory_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def update(
        cls, *, tenant_id: str, inventory_ref: str, complete: bool = True
    ) -> DsCompleteInventoryRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.inv_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.discovery.inventory_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            inventory_ref=inventory_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("InventoryUpdated")
        root.pending_events.append("IncompleteInventoryRejected")
        root.history.append({"event": "InventoryComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsAvailableMetadataRoot(AggregateRoot):
    tenant_id: str
    metadata_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls, *, tenant_id: str, metadata_ref: str, available: bool = True
    ) -> DsAvailableMetadataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.meta_tenant_required")
        if not available:
            raise ValueError(
                "data_security.discovery.metadata_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            metadata_ref=metadata_ref.strip(),
            available=True,
            status="collected",
        )
        root.pending_events.append("MetadataCollected")
        root.pending_events.append("UnavailableMetadataRejected")
        root.history.append({"event": "MetadataAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsDeterminableOwnershipRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    determinable: bool
    owner_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def determine(
        cls,
        *,
        tenant_id: str,
        asset_ref: str,
        owner_ref: str = "owner",
        determinable: bool = True,
    ) -> DsDeterminableOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.own_tenant_required")
        if not determinable:
            raise ValueError(
                "data_security.discovery.ownership_cannot_be_determined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            owner_ref=owner_ref.strip(),
            determinable=True,
            status="determined",
        )
        root.pending_events.append("InventoryUpdated")
        root.pending_events.append("UndeterminableOwnershipRejected")
        root.history.append({"event": "OwnershipDetermined"})
        return root

    def is_undeterminable(self) -> bool:
        return not self.determinable


@dataclass(eq=False, kw_only=True)
class DsVisibleShadowDataRoot(AggregateRoot):
    tenant_id: str
    shadow_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, shadow_ref: str, visible: bool = True
    ) -> DsVisibleShadowDataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.shadow_tenant_required")
        if not visible:
            raise ValueError(
                "data_security.discovery.shadow_data_remains_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            shadow_ref=shadow_ref.strip(),
            visible=True,
            status="detected",
        )
        root.pending_events.append("ShadowDataDetected")
        root.pending_events.append("InvisibleShadowRejected")
        root.history.append({"event": "ShadowVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsAiDiscoveryRoot(AggregateRoot):
    tenant_id: str
    capability_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, capability_ref: str, present: bool = True
    ) -> DsAiDiscoveryRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.ai_tenant_required")
        if not present:
            raise ValueError(
                "data_security.discovery.ai_discovery_capability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            capability_ref=capability_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("SensitivePatternDetected")
        root.pending_events.append("MissingAiDiscoveryRejected")
        root.history.append({"event": "AiDiscoveryEnabled"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsAnalyzableRelationshipsRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    analyzable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls, *, tenant_id: str, graph_ref: str, analyzable: bool = True
    ) -> DsAnalyzableRelationshipsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.rel_tenant_required")
        if not analyzable:
            raise ValueError(
                "data_security.discovery.data_relationships_cannot_be_analyzed"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            graph_ref=graph_ref.strip(),
            analyzable=True,
            status="analyzable",
        )
        root.pending_events.append("DiscoveryCompleted")
        root.pending_events.append("UnanalyzableRelationshipsRejected")
        root.history.append({"event": "RelationshipsAnalyzable"})
        return root

    def is_unanalyzable(self) -> bool:
        return not self.analyzable


@dataclass(eq=False, kw_only=True)
class DsDiscoveryJobRoot(AggregateRoot):
    tenant_id: str
    job_ref: str
    started: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls, *, tenant_id: str, job_ref: str, started: bool = True
    ) -> DsDiscoveryJobRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.discovery.job_tenant_required")
        if not started:
            raise ValueError("data_security.discovery.job_not_started")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            job_ref=job_ref.strip(),
            started=True,
            status="running",
        )
        root.pending_events.append("DiscoveryStarted")
        root.pending_events.append("DataSourceRegistered")
        root.history.append({"event": "JobStarted"})
        return root
