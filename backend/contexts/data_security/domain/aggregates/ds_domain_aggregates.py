"""P211-C Data Security domain architecture aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsDomainsLooselyCoupledRoot(AggregateRoot):
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
    ) -> DsDomainsLooselyCoupledRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.tenant_required")
        if not loosely_coupled:
            raise ValueError(
                "data_security.domain.domains_are_tightly_coupled"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
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
class DsOwnershipClearRoot(AggregateRoot):
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
    ) -> DsOwnershipClearRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.own_tenant_required")
        if not clear:
            raise ValueError(
                "data_security.domain.data_ownership_is_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ownership_ref=ownership_ref.strip(),
            clear=True,
            status="bound",
        )
        root.pending_events.append("AggregateOwnershipBound")
        root.pending_events.append("UnclearOwnershipRejected")
        root.history.append({"event": "OwnershipCleared"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class DsPrivacyIntegratedRoot(AggregateRoot):
    tenant_id: str
    integration_ref: str
    integrated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, integration_ref: str, integrated: bool = True
    ) -> DsPrivacyIntegratedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.priv_tenant_required")
        if not integrated:
            raise ValueError(
                "data_security.domain.privacy_is_separated_from_security"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            integration_ref=integration_ref.strip(),
            integrated=True,
            status="integrated",
        )
        root.pending_events.append("PrivacySecurityIntegrated")
        root.pending_events.append("SeparatedPrivacyRejected")
        root.history.append({"event": "PrivacyIntegrated"})
        return root

    def is_separated(self) -> bool:
        return not self.integrated


@dataclass(eq=False, kw_only=True)
class DsEventsPresentRoot(AggregateRoot):
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
    ) -> DsEventsPresentRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.evt_tenant_required")
        if not present:
            raise ValueError("data_security.domain.events_are_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
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
class DsAggregatesDefinedRoot(AggregateRoot):
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
    ) -> DsAggregatesDefinedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.agg_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.domain.aggregates_are_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
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
class DsIntegrationBoundariesClearRoot(AggregateRoot):
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
    ) -> DsIntegrationBoundariesClearRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.int_tenant_required")
        if not clear:
            raise ValueError(
                "data_security.domain.integration_boundaries_are_unclear"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
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
class DsDomainMapRoot(AggregateRoot):
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
    ) -> DsDomainMapRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.map_tenant_required")
        if not published:
            raise ValueError("data_security.domain.domain_map_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("DomainMapPublished")
        root.history.append({"event": "DomainMapPublished"})
        return root


@dataclass(eq=False, kw_only=True)
class DsContextMapRoot(AggregateRoot):
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
    ) -> DsContextMapRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.domain.ctx_tenant_required")
        if not registered:
            raise ValueError("data_security.domain.context_not_registered")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            context_ref=context_ref.strip(),
            registered=True,
            status="registered",
        )
        root.pending_events.append("SubdomainRegistered")
        root.history.append({"event": "ContextRegistered"})
        return root
