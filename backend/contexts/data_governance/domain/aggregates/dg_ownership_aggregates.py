"""P212-D Ownership/stewardship aggregates — quality-gate invariants."""
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
class DgOwnershipArchitectureRoot(AggregateRoot):
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
    ) -> DgOwnershipArchitectureRoot:
        tid = _tid(tenant_id, "data_governance.ownership.tenant_required")
        if not complete:
            raise ValueError(
                "data_governance.ownership.data_ownership_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("OwnerAssignedEvent")
        root.pending_events.append("IncompleteOwnershipArchitectureRejected")
        root.history.append({"event": "OwnershipArchitecturePublished"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgStewardshipArchitectureRoot(AggregateRoot):
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
    ) -> DgStewardshipArchitectureRoot:
        tid = _tid(tenant_id, "data_governance.ownership.stew_tenant_required")
        if not complete:
            raise ValueError(
                "data_governance.ownership.data_stewardship_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("StewardRegisteredEvent")
        root.history.append({"event": "StewardshipArchitecturePublished"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgAccountabilityFrameworkRoot(AggregateRoot):
    tenant_id: str
    framework_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, framework_ref: str, present: bool = True
    ) -> DgAccountabilityFrameworkRoot:
        tid = _tid(tenant_id, "data_governance.ownership.acc_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.accountability_framework_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            framework_ref=framework_ref.strip(),
            present=True,
            status="established",
        )
        root.pending_events.append("AccountabilityChangedEvent")
        root.history.append({"event": "AccountabilityFrameworkEstablished"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipDddModelRoot(AggregateRoot):
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
    ) -> DgOwnershipDddModelRoot:
        tid = _tid(tenant_id, "data_governance.ownership.ddd_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.ddd_domain_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="defined",
        )
        root.pending_events.append("DataOwnerAssignedEvent")
        root.history.append({"event": "DddModelDefined"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipCqrsRoot(AggregateRoot):
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
    ) -> DgOwnershipCqrsRoot:
        tid = _tid(tenant_id, "data_governance.ownership.cqrs_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.cqrs_design_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("OwnershipTransferredEvent")
        root.history.append({"event": "CqrsAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipEventSourcingRoot(AggregateRoot):
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
    ) -> DgOwnershipEventSourcingRoot:
        tid = _tid(tenant_id, "data_governance.ownership.es_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.event_sourcing_design_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DataOwnerChangedEvent")
        root.history.append({"event": "EventSourcingEnabled"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipDataMeshRoot(AggregateRoot):
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
    ) -> DgOwnershipDataMeshRoot:
        tid = _tid(tenant_id, "data_governance.ownership.mesh_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.data_mesh_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("DataStewardAssignedEvent")
        root.history.append({"event": "DataMeshAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipKnowledgeGraphRoot(AggregateRoot):
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
    ) -> DgOwnershipKnowledgeGraphRoot:
        tid = _tid(tenant_id, "data_governance.ownership.kg_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.knowledge_graph_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="integrated",
        )
        root.pending_events.append("StewardActivityCompletedEvent")
        root.history.append({"event": "KnowledgeGraphIntegrated"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipDigitalTwinRoot(AggregateRoot):
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
    ) -> DgOwnershipDigitalTwinRoot:
        tid = _tid(tenant_id, "data_governance.ownership.twin_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.digital_twin_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="integrated",
        )
        root.pending_events.append("OwnershipRiskDetectedEvent")
        root.history.append({"event": "DigitalTwinIntegrated"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipAiIntelligenceRoot(AggregateRoot):
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
    ) -> DgOwnershipAiIntelligenceRoot:
        tid = _tid(tenant_id, "data_governance.ownership.ai_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.ai_ownership_intelligence_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OwnershipViolationDetectedEvent")
        root.history.append({"event": "AiIntelligenceEnabled"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipZeroTrustRoot(AggregateRoot):
    tenant_id: str
    zt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, zt_ref: str, present: bool = True
    ) -> DgOwnershipZeroTrustRoot:
        tid = _tid(tenant_id, "data_governance.ownership.zt_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.zero_trust_security_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("DataIssueResolvedEvent")
        root.history.append({"event": "ZeroTrustAligned"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgOwnershipScalabilityRoot(AggregateRoot):
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
    ) -> DgOwnershipScalabilityRoot:
        tid = _tid(tenant_id, "data_governance.ownership.scale_tenant_required")
        if not present:
            raise ValueError(
                "data_governance.ownership.enterprise_scalability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="confirmed",
        )
        root.pending_events.append("OwnershipExpiredEvent")
        root.history.append({"event": "ScalabilityConfirmed"})
        return root

    def is_missing(self) -> bool:
        return not self.present
