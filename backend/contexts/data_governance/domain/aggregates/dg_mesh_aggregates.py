"""P212-F Data Mesh aggregates — quality-gate invariants."""
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
class DgMeshArchitectureRoot(AggregateRoot):
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
    ) -> "DgMeshArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.mesh.data_mesh_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("DataDomainCreatedEvent")
        root.history.append({"event": "DgMeshArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgProductPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, platform_ref: str, complete: bool = True
    ) -> "DgProductPlatformRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_1_required")
        if not complete:
            raise ValueError("data_governance.mesh.data_product_platform_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("DataProductCreatedEvent")
        root.history.append({"event": "DgProductPlatformRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgMeshDddModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, model_ref: str, present: bool = True
    ) -> "DgMeshDddModelRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_2_required")
        if not present:
            raise ValueError("data_governance.mesh.ddd_domain_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductRegisteredEvent")
        root.history.append({"event": "DgMeshDddModelRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshDomainModelRoot(AggregateRoot):
    tenant_id: str
    domain_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, domain_ref: str, present: bool = True
    ) -> "DgMeshDomainModelRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_3_required")
        if not present:
            raise ValueError("data_governance.mesh.data_domain_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            domain_ref=domain_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataDomainCreatedEvent")
        root.history.append({"event": "DgMeshDomainModelRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshLifecycleRoot(AggregateRoot):
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
    ) -> "DgMeshLifecycleRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_4_required")
        if not present:
            raise ValueError("data_governance.mesh.data_product_lifecycle_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lifecycle_ref=lifecycle_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductPublishedEvent")
        root.history.append({"event": "DgMeshLifecycleRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshContractRoot(AggregateRoot):
    tenant_id: str
    contract_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, contract_ref: str, present: bool = True
    ) -> "DgMeshContractRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_5_required")
        if not present:
            raise ValueError("data_governance.mesh.data_contract_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            contract_ref=contract_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataContractApprovedEvent")
        root.history.append({"event": "DgMeshContractRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshQualityIntegrationRoot(AggregateRoot):
    tenant_id: str
    quality_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, quality_ref: str, present: bool = True
    ) -> "DgMeshQualityIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_6_required")
        if not present:
            raise ValueError("data_governance.mesh.data_quality_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            quality_ref=quality_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductCertifiedEvent")
        root.history.append({"event": "DgMeshQualityIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshKnowledgeGraphRoot(AggregateRoot):
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
    ) -> "DgMeshKnowledgeGraphRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_7_required")
        if not present:
            raise ValueError("data_governance.mesh.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductUpdatedEvent")
        root.history.append({"event": "DgMeshKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshDigitalTwinRoot(AggregateRoot):
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
    ) -> "DgMeshDigitalTwinRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_8_required")
        if not present:
            raise ValueError("data_governance.mesh.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductConsumedEvent")
        root.history.append({"event": "DgMeshDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshAiIntelligenceRoot(AggregateRoot):
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
    ) -> "DgMeshAiIntelligenceRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_9_required")
        if not present:
            raise ValueError("data_governance.mesh.ai_native_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductDeprecatedEvent")
        root.history.append({"event": "DgMeshAiIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshCqrsRoot(AggregateRoot):
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
    ) -> "DgMeshCqrsRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_10_required")
        if not present:
            raise ValueError("data_governance.mesh.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductApprovedEvent")
        root.history.append({"event": "DgMeshCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshEventSourcingRoot(AggregateRoot):
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
    ) -> "DgMeshEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_11_required")
        if not present:
            raise ValueError("data_governance.mesh.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductRetiredEvent")
        root.history.append({"event": "DgMeshEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshMicroservicesRoot(AggregateRoot):
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
    ) -> "DgMeshMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_12_required")
        if not present:
            raise ValueError("data_governance.mesh.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductPublishedEvent")
        root.history.append({"event": "DgMeshMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMeshScalabilityRoot(AggregateRoot):
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
    ) -> "DgMeshScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.mesh.tenant_13_required")
        if not present:
            raise ValueError("data_governance.mesh.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataProductConsumedEvent")
        root.history.append({"event": "DgMeshScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
