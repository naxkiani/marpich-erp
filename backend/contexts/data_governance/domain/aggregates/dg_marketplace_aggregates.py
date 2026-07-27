"""P212-G Data Marketplace aggregates — quality-gate invariants."""
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
class DgMarketplaceArchitectureRoot(AggregateRoot):
    tenant_id: str
    architecture_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, architecture_ref: str, complete: bool = True
    ) -> "DgMarketplaceArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.marketplace.enterprise_data_marketplace_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("DataProductPublishedToMarketplaceEvent")
        root.history.append({"event": "DgMarketplaceArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class DgMarketplaceCatalogRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, catalog_ref: str, present: bool = True
    ) -> "DgMarketplaceCatalogRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_1_required")
        if not present:
            raise ValueError("data_governance.marketplace.data_catalog_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            catalog_ref=catalog_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CatalogEntryCreatedEvent")
        root.history.append({"event": "DgMarketplaceCatalogRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceDiscoveryRoot(AggregateRoot):
    tenant_id: str
    discovery_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, discovery_ref: str, present: bool = True
    ) -> "DgMarketplaceDiscoveryRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_2_required")
        if not present:
            raise ValueError("data_governance.marketplace.data_discovery_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            discovery_ref=discovery_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductDiscoveredEvent")
        root.history.append({"event": "DgMarketplaceDiscoveryRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceConsumptionRoot(AggregateRoot):
    tenant_id: str
    consumption_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, consumption_ref: str, present: bool = True
    ) -> "DgMarketplaceConsumptionRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_3_required")
        if not present:
            raise ValueError("data_governance.marketplace.data_product_consumption_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            consumption_ref=consumption_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductConsumedEvent")
        root.history.append({"event": "DgMarketplaceConsumptionRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceAccessGovernanceRoot(AggregateRoot):
    tenant_id: str
    access_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, access_ref: str, present: bool = True
    ) -> "DgMarketplaceAccessGovernanceRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_4_required")
        if not present:
            raise ValueError("data_governance.marketplace.data_access_governance_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            access_ref=access_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataAccessRequestedEvent")
        root.history.append({"event": "DgMarketplaceAccessGovernanceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceAiRecommendationRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> "DgMarketplaceAiRecommendationRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_5_required")
        if not present:
            raise ValueError("data_governance.marketplace.ai_recommendation_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductDiscoveredEvent")
        root.history.append({"event": "DgMarketplaceAiRecommendationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceMeshAlignmentRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, mesh_ref: str, present: bool = True
    ) -> "DgMarketplaceMeshAlignmentRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_6_required")
        if not present:
            raise ValueError("data_governance.marketplace.data_mesh_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductPublishedEvent")
        root.history.append({"event": "DgMarketplaceMeshAlignmentRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, graph_ref: str, present: bool = True
    ) -> "DgMarketplaceKnowledgeGraphRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_7_required")
        if not present:
            raise ValueError("data_governance.marketplace.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CatalogEntryCreatedEvent")
        root.history.append({"event": "DgMarketplaceKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, twin_ref: str, present: bool = True
    ) -> "DgMarketplaceDigitalTwinRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_8_required")
        if not present:
            raise ValueError("data_governance.marketplace.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataUsageRecordedEvent")
        root.history.append({"event": "DgMarketplaceDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceCqrsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, cqrs_ref: str, present: bool = True
    ) -> "DgMarketplaceCqrsRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_9_required")
        if not present:
            raise ValueError("data_governance.marketplace.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("AccessRequestedEvent")
        root.history.append({"event": "DgMarketplaceCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceEventSourcingRoot(AggregateRoot):
    tenant_id: str
    es_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, es_ref: str, present: bool = True
    ) -> "DgMarketplaceEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_10_required")
        if not present:
            raise ValueError("data_governance.marketplace.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SubscriptionCreatedEvent")
        root.history.append({"event": "DgMarketplaceEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceMicroservicesRoot(AggregateRoot):
    tenant_id: str
    ms_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, ms_ref: str, present: bool = True
    ) -> "DgMarketplaceMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_11_required")
        if not present:
            raise ValueError("data_governance.marketplace.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("AccessApprovedEvent")
        root.history.append({"event": "DgMarketplaceMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceZeroTrustRoot(AggregateRoot):
    tenant_id: str
    zt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, zt_ref: str, present: bool = True
    ) -> "DgMarketplaceZeroTrustRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_12_required")
        if not present:
            raise ValueError("data_governance.marketplace.zero_trust_security_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("AccessApprovedEvent")
        root.history.append({"event": "DgMarketplaceZeroTrustRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgMarketplaceScalabilityRoot(AggregateRoot):
    tenant_id: str
    scale_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, scale_ref: str, present: bool = True
    ) -> "DgMarketplaceScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.marketplace.tenant_13_required")
        if not present:
            raise ValueError("data_governance.marketplace.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataUsageRecordedEvent")
        root.history.append({"event": "DgMarketplaceScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
