"""P210-C Cyber Security domain architecture aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsNonOverlappingContextsRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    overlapping: bool
    context_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        map_ref: str,
        overlapping: bool = False,
        context_count: int = 10,
    ) -> CsNonOverlappingContextsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.tenant_required")
        if overlapping or context_count < 10:
            raise ValueError("cyber_security.domain.bounded_contexts_overlap")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            overlapping=False,
            context_count=context_count,
            status="registered",
        )
        root.pending_events.append("LogicalContextRegistered")
        root.pending_events.append("OverlappingContextRejected")
        root.history.append({"event": "NonOverlappingContextsRegistered"})
        return root

    def is_overlapping(self) -> bool:
        return self.overlapping


@dataclass(eq=False, kw_only=True)
class CsAggregateBoundaryRoot(AggregateRoot):
    tenant_id: str
    aggregate_ref: str
    consistency_ok: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        aggregate_ref: str,
        consistency_ok: bool = True,
    ) -> CsAggregateBoundaryRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.agg_tenant_required")
        if not consistency_ok:
            raise ValueError(
                "cyber_security.domain.aggregates_violate_consistency_boundaries"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            aggregate_ref=aggregate_ref.strip(),
            consistency_ok=True,
            status="defined",
        )
        root.pending_events.append("AggregateBoundaryDefined")
        root.history.append({"event": "AggregateBoundaryDefined"})
        return root

    def violates_consistency(self) -> bool:
        return not self.consistency_ok


@dataclass(eq=False, kw_only=True)
class CsOwnershipClearRoot(AggregateRoot):
    tenant_id: str
    ownership_ref: str
    clear: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, ownership_ref: str, clear: bool = True
    ) -> CsOwnershipClearRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.own_tenant_required")
        if not clear:
            raise ValueError("cyber_security.domain.domain_ownership_unclear")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ownership_ref=ownership_ref.strip(),
            clear=True,
            status="declared",
        )
        root.pending_events.append("ContextMapBound")
        root.history.append({"event": "OwnershipDeclaredClear"})
        return root

    def is_unclear(self) -> bool:
        return not self.clear


@dataclass(eq=False, kw_only=True)
class CsNoRuleLeakRoot(AggregateRoot):
    tenant_id: str
    contract_ref: str
    leaking: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, contract_ref: str, leaking: bool = False
    ) -> CsNoRuleLeakRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.leak_tenant_required")
        if leaking:
            raise ValueError(
                "cyber_security.domain.business_rules_leak_across_contexts"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            contract_ref=contract_ref.strip(),
            leaking=False,
            status="bound",
        )
        root.pending_events.append("RuleLeakRejected")
        root.history.append({"event": "NoRuleLeakBound"})
        return root

    def is_leaking(self) -> bool:
        return self.leaking


@dataclass(eq=False, kw_only=True)
class CsDomainDrivenEventsRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    domain_driven: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, catalog_ref: str, domain_driven: bool = True
    ) -> CsDomainDrivenEventsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.evt_tenant_required")
        if not domain_driven:
            raise ValueError("cyber_security.domain.events_not_domain_driven")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            catalog_ref=catalog_ref.strip(),
            domain_driven=True,
            status="published",
        )
        root.pending_events.append("DomainEventCatalogPublished")
        root.pending_events.append("NonDomainEventRejected")
        root.history.append({"event": "DomainDrivenEventsPublished"})
        return root

    def is_non_domain_driven(self) -> bool:
        return not self.domain_driven


@dataclass(eq=False, kw_only=True)
class CsKnowledgeGraphRequiredRoot(AggregateRoot):
    tenant_id: str
    link_ref: str
    integrated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, link_ref: str, integrated: bool = True
    ) -> CsKnowledgeGraphRequiredRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.kg_tenant_required")
        if not integrated:
            raise ValueError(
                "cyber_security.domain.knowledge_graph_integration_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            link_ref=link_ref.strip(),
            integrated=True,
            status="declared",
        )
        root.pending_events.append("KnowledgeGraphLinkDeclared")
        root.history.append({"event": "KnowledgeGraphIntegrated"})
        return root

    def is_missing(self) -> bool:
        return not self.integrated


@dataclass(eq=False, kw_only=True)
class CsAclPresentRoot(AggregateRoot):
    tenant_id: str
    acl_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, acl_ref: str, present: bool = True
    ) -> CsAclPresentRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.acl_tenant_required")
        if not present:
            raise ValueError(
                "cyber_security.domain.anti_corruption_layers_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            acl_ref=acl_ref.strip(),
            present=True,
            status="registered",
        )
        root.pending_events.append("AclContractRegistered")
        root.pending_events.append("MissingAclRejected")
        root.history.append({"event": "AclPresentRegistered"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsDigitalTwinLinkRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, twin_ref: str
    ) -> CsDigitalTwinLinkRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.domain.twin_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            twin_ref=twin_ref.strip(),
            status="declared",
        )
        root.pending_events.append("DigitalTwinLinkDeclared")
        root.history.append({"event": "DigitalTwinLinkDeclared"})
        return root
