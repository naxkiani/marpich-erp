"""P212-A Data Governance strategy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _require_tenant(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class DgCompleteGovernanceArchitectureRoot(AggregateRoot):
    tenant_id: str
    architecture_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, architecture_ref: str, complete: bool = True
    ) -> DgCompleteGovernanceArchitectureRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.tenant_required"
        )
        if not complete:
            raise ValueError(
                "data_governance.strategy."
                "enterprise_data_governance_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("DataPolicyApproved")
        root.pending_events.append("IncompleteGovernanceArchitectureRejected")
        root.history.append({"event": "GovernanceArchitectureComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgDddDomainModelRoot(AggregateRoot):
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
    ) -> DgDddDomainModelRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.ddd_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.ddd_domain_model_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="defined",
        )
        root.pending_events.append("DataOwnerAssigned")
        root.pending_events.append("MissingDddDomainModelRejected")
        root.history.append({"event": "DddDomainModelPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgCqrsArchitectureRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, cqrs_ref: str, present: bool = True
    ) -> DgCqrsArchitectureRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.cqrs_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.cqrs_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="defined",
        )
        root.pending_events.append("DataProductRegistered")
        root.pending_events.append("MissingCqrsArchitectureRejected")
        root.history.append({"event": "CqrsArchitecturePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgEventDrivenArchitectureRoot(AggregateRoot):
    tenant_id: str
    events_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, events_ref: str, present: bool = True
    ) -> DgEventDrivenArchitectureRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.events_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.event_driven_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            events_ref=events_ref.strip(),
            present=True,
            status="defined",
        )
        root.pending_events.append("MetadataUpdated")
        root.pending_events.append("MissingEventDrivenArchitectureRejected")
        root.history.append({"event": "EventDrivenArchitecturePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgMicroservicesArchitectureRoot(AggregateRoot):
    tenant_id: str
    services_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, services_ref: str, present: bool = True
    ) -> DgMicroservicesArchitectureRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.ms_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.microservices_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            services_ref=services_ref.strip(),
            present=True,
            status="defined",
        )
        root.pending_events.append("DataStewardCreated")
        root.pending_events.append("MissingMicroservicesArchitectureRejected")
        root.history.append({"event": "MicroservicesArchitecturePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDataMeshNativeRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    native: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, mesh_ref: str, native: bool = True
    ) -> DgDataMeshNativeRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.mesh_tenant_required"
        )
        if not native:
            raise ValueError(
                "data_governance.strategy."
                "data_mesh_native_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            native=True,
            status="native",
        )
        root.pending_events.append("DataProductRegistered")
        root.pending_events.append("MissingDataMeshNativeRejected")
        root.history.append({"event": "DataMeshNative"})
        return root

    def is_missing(self) -> bool:
        return not self.native


@dataclass(eq=False, kw_only=True)
class DgKnowledgeGraphIntegrationRoot(AggregateRoot):
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
    ) -> DgKnowledgeGraphIntegrationRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.kg_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.knowledge_graph_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="integrated",
        )
        root.pending_events.append("MetadataUpdated")
        root.pending_events.append("MissingKnowledgeGraphIntegrationRejected")
        root.history.append({"event": "KnowledgeGraphIntegrationPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgDigitalTwinIntegrationRoot(AggregateRoot):
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
    ) -> DgDigitalTwinIntegrationRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.twin_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.digital_twin_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="integrated",
        )
        root.pending_events.append("AIReadinessScoreCalculated")
        root.pending_events.append("MissingDigitalTwinIntegrationRejected")
        root.history.append({"event": "DigitalTwinIntegrationPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgAiNativeGovernanceRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> DgAiNativeGovernanceRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.ai_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.ai_native_governance_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="present",
        )
        root.pending_events.append("AIReadinessScoreCalculated")
        root.pending_events.append("MissingAiNativeGovernanceRejected")
        root.history.append({"event": "AiNativeGovernancePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgZeroTrustAlignmentRoot(AggregateRoot):
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
    ) -> DgZeroTrustAlignmentRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.zt_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.zero_trust_alignment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="aligned",
        )
        root.pending_events.append("GovernanceViolationDetected")
        root.pending_events.append("MissingZeroTrustAlignmentRejected")
        root.history.append({"event": "ZeroTrustAlignmentPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgPrivacyByDesignRoot(AggregateRoot):
    tenant_id: str
    privacy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def apply(
        cls, *, tenant_id: str, privacy_ref: str, present: bool = True
    ) -> DgPrivacyByDesignRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.privacy_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.privacy_by_design_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            privacy_ref=privacy_ref.strip(),
            present=True,
            status="applied",
        )
        root.pending_events.append("DataQualityRulePublished")
        root.pending_events.append("MissingPrivacyByDesignRejected")
        root.history.append({"event": "PrivacyByDesignPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgCloudNativeDeploymentRoot(AggregateRoot):
    tenant_id: str
    deploy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, deploy_ref: str, present: bool = True
    ) -> DgCloudNativeDeploymentRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.cloud_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.cloud_native_deployment_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            deploy_ref=deploy_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DataPolicyApproved")
        root.pending_events.append("MissingCloudNativeDeploymentRejected")
        root.history.append({"event": "CloudNativeDeploymentPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgEnterpriseScalabilityRoot(AggregateRoot):
    tenant_id: str
    scale_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, scale_ref: str, present: bool = True
    ) -> DgEnterpriseScalabilityRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.scale_tenant_required"
        )
        if not present:
            raise ValueError(
                "data_governance.strategy.enterprise_scalability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DataOwnerAssigned")
        root.pending_events.append("MissingEnterpriseScalabilityRejected")
        root.history.append({"event": "EnterpriseScalabilityPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgStrategyProfileRoot(AggregateRoot):
    tenant_id: str
    strategy_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, strategy_ref: str, published: bool = True
    ) -> DgStrategyProfileRoot:
        tid = _require_tenant(
            tenant_id, "data_governance.strategy.profile_tenant_required"
        )
        if not published:
            raise ValueError("data_governance.strategy.strategy_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            strategy_ref=strategy_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("DataGovernanceStrategyPublished")
        root.history.append({"event": "StrategyPublished"})
        return root
