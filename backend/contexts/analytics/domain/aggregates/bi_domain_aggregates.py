"""P213-C BI domain architecture aggregates — quality-gate invariants."""
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
class BiDomainsLooselyCoupledRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    loosely_coupled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, map_ref: str, loosely_coupled: bool = True
    ) -> BiDomainsLooselyCoupledRoot:
        tid = _tid(tenant_id, "analytics.domain.tenant_required")
        if not loosely_coupled:
            raise ValueError("analytics.domain.domains_are_tightly_coupled")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            map_ref=map_ref.strip(),
            loosely_coupled=True,
            status="enforced",
        )
        root.pending_events.append("DomainMapPublished")
        root.pending_events.append("TightCouplingRejected")
        root.history.append({"event": "LooseCouplingEnforced"})
        return root

    def is_tightly_coupled(self) -> bool:
        return not self.loosely_coupled


@dataclass(eq=False, kw_only=True)
class BiOwnershipClearRoot(AggregateRoot):
    tenant_id: str
    ownership_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, ownership_ref: str, clear: bool = True
    ) -> BiOwnershipClearRoot:
        tid = _tid(tenant_id, "analytics.domain.own_tenant_required")
        if not clear:
            raise ValueError("analytics.domain.bi_ownership_is_unclear")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ownership_ref=ownership_ref.strip(),
            clear=True,
            status="bound",
        )
        root.pending_events.append("BIOwnershipBound")
        root.pending_events.append("UnclearOwnershipRejected")
        root.history.append({"event": "OwnershipCleared"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class BiAggregatesDefinedRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, catalog_ref: str, defined: bool = True
    ) -> BiAggregatesDefinedRoot:
        tid = _tid(tenant_id, "analytics.domain.agg_tenant_required")
        if not defined:
            raise ValueError("analytics.domain.aggregates_are_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            catalog_ref=catalog_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("SubdomainRegistered")
        root.pending_events.append("UndefinedAggregatesRejected")
        root.history.append({"event": "AggregatesDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class BiEventsPresentRoot(AggregateRoot):
    tenant_id: str
    catalogue_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, catalogue_ref: str, present: bool = True
    ) -> BiEventsPresentRoot:
        tid = _tid(tenant_id, "analytics.domain.evt_tenant_required")
        if not present:
            raise ValueError("analytics.domain.events_are_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            catalogue_ref=catalogue_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("EventCataloguePublished")
        root.pending_events.append("MissingEventsRejected")
        root.history.append({"event": "EventsPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiIntegrationBoundariesClearRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, boundary_ref: str, clear: bool = True
    ) -> BiIntegrationBoundariesClearRoot:
        tid = _tid(tenant_id, "analytics.domain.int_tenant_required")
        if not clear:
            raise ValueError(
                "analytics.domain.integration_boundaries_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            boundary_ref=boundary_ref.strip(),
            clear=True,
            status="declared",
        )
        root.pending_events.append("IntegrationBoundaryDeclared")
        root.pending_events.append("UnclearBoundariesRejected")
        root.history.append({"event": "BoundariesCleared"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class BiCqrsAlignedRoot(AggregateRoot):
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
    ) -> BiCqrsAlignedRoot:
        tid = _tid(tenant_id, "analytics.domain.cqrs_tenant_required")
        if not present:
            raise ValueError("analytics.domain.cqrs_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("CqrsAligned")
        root.history.append({"event": "CqrsAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiMicroserviceBoundariesClearRoot(AggregateRoot):
    tenant_id: str
    boundary_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, boundary_ref: str, clear: bool = True
    ) -> BiMicroserviceBoundariesClearRoot:
        tid = _tid(tenant_id, "analytics.domain.ms_tenant_required")
        if not clear:
            raise ValueError(
                "analytics.domain.microservice_boundaries_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            boundary_ref=boundary_ref.strip(),
            clear=True,
            status="declared",
        )
        root.pending_events.append("MicroserviceBoundariesDeclared")
        root.history.append({"event": "MicroserviceBoundariesCleared"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


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
    def align(
        cls, *, tenant_id: str, mesh_ref: str, present: bool = True
    ) -> BiDataMeshAlignedRoot:
        tid = _tid(tenant_id, "analytics.domain.mesh_tenant_required")
        if not present:
            raise ValueError("analytics.domain.data_mesh_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("DataMeshAligned")
        root.history.append({"event": "DataMeshAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiKnowledgeGraphAlignedRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, graph_ref: str, present: bool = True
    ) -> BiKnowledgeGraphAlignedRoot:
        tid = _tid(tenant_id, "analytics.domain.kg_tenant_required")
        if not present:
            raise ValueError(
                "analytics.domain.knowledge_graph_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("KnowledgeGraphAligned")
        root.history.append({"event": "KnowledgeGraphAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDigitalTwinAlignedRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, twin_ref: str, present: bool = True
    ) -> BiDigitalTwinAlignedRoot:
        tid = _tid(tenant_id, "analytics.domain.twin_tenant_required")
        if not present:
            raise ValueError(
                "analytics.domain.digital_twin_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("DigitalTwinAligned")
        root.history.append({"event": "DigitalTwinAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiGovernanceAlignedRoot(AggregateRoot):
    tenant_id: str
    gov_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, gov_ref: str, present: bool = True
    ) -> BiGovernanceAlignedRoot:
        tid = _tid(tenant_id, "analytics.domain.gov_tenant_required")
        if not present:
            raise ValueError(
                "analytics.domain.enterprise_governance_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gov_ref=gov_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("GovernanceAligned")
        root.history.append({"event": "GovernanceAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDomainMapRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, map_ref: str, published: bool = True
    ) -> BiDomainMapRoot:
        tid = _tid(tenant_id, "analytics.domain.map_tenant_required")
        if not published:
            raise ValueError("analytics.domain.domain_map_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            map_ref=map_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("DomainMapPublished")
        root.history.append({"event": "DomainMapPublished"})
        return root


@dataclass(eq=False, kw_only=True)
class BiContextMapRoot(AggregateRoot):
    tenant_id: str
    context_ref: str
    registered: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, context_ref: str, registered: bool = True
    ) -> BiContextMapRoot:
        tid = _tid(tenant_id, "analytics.domain.ctx_tenant_required")
        if not registered:
            raise ValueError("analytics.domain.context_not_registered")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            context_ref=context_ref.strip(),
            registered=True,
            status="registered",
        )
        root.pending_events.append("SubdomainRegistered")
        root.history.append({"event": "ContextRegistered"})
        return root
