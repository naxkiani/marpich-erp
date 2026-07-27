"""P212-J Knowledge Graph aggregates — quality-gate invariants."""
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
class DgGraphArchitectureRoot(AggregateRoot):
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
    ) -> "DgGraphArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.graph.enterprise_knowledge_graph_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeGraphUpdatedEvent")
        root.history.append({"event": "DgGraphArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class DgGraphDddModelRoot(AggregateRoot):
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
    ) -> "DgGraphDddModelRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_1_required")
        if not present:
            raise ValueError("data_governance.graph.ddd_domain_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeEntityCreatedEvent")
        root.history.append({"event": "DgGraphDddModelRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphOntologyRoot(AggregateRoot):
    tenant_id: str
    ontology_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, ontology_ref: str, present: bool = True
    ) -> "DgGraphOntologyRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_2_required")
        if not present:
            raise ValueError("data_governance.graph.ontology_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ontology_ref=ontology_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("OntologyCreatedEvent")
        root.history.append({"event": "DgGraphOntologyRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphSemanticFabricRoot(AggregateRoot):
    tenant_id: str
    fabric_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, fabric_ref: str, present: bool = True
    ) -> "DgGraphSemanticFabricRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_3_required")
        if not present:
            raise ValueError("data_governance.graph.semantic_data_fabric_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            fabric_ref=fabric_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeGraphUpdatedEvent")
        root.history.append({"event": "DgGraphSemanticFabricRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphIntelligenceRoot(AggregateRoot):
    tenant_id: str
    intel_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, intel_ref: str, present: bool = True
    ) -> "DgGraphIntelligenceRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_4_required")
        if not present:
            raise ValueError("data_governance.graph.graph_intelligence_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            intel_ref=intel_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("InferenceGeneratedEvent")
        root.history.append({"event": "DgGraphIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphAiReasoningRoot(AggregateRoot):
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
    ) -> "DgGraphAiReasoningRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_5_required")
        if not present:
            raise ValueError("data_governance.graph.ai_reasoning_layer_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("InferenceGeneratedEvent")
        root.history.append({"event": "DgGraphAiReasoningRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphMeshIntegrationRoot(AggregateRoot):
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
    ) -> "DgGraphMeshIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_6_required")
        if not present:
            raise ValueError("data_governance.graph.data_mesh_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RelationshipCreatedEvent")
        root.history.append({"event": "DgGraphMeshIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphMetadataIntegrationRoot(AggregateRoot):
    tenant_id: str
    metadata_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, metadata_ref: str, present: bool = True
    ) -> "DgGraphMetadataIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_7_required")
        if not present:
            raise ValueError("data_governance.graph.metadata_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            metadata_ref=metadata_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeEntityCreatedEvent")
        root.history.append({"event": "DgGraphMetadataIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphMarketplaceIntegrationRoot(AggregateRoot):
    tenant_id: str
    marketplace_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, marketplace_ref: str, present: bool = True
    ) -> "DgGraphMarketplaceIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_8_required")
        if not present:
            raise ValueError("data_governance.graph.data_marketplace_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            marketplace_ref=marketplace_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RelationshipCreatedEvent")
        root.history.append({"event": "DgGraphMarketplaceIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphPolicyIntegrationRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, policy_ref: str, present: bool = True
    ) -> "DgGraphPolicyIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_9_required")
        if not present:
            raise ValueError("data_governance.graph.policy_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            policy_ref=policy_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SemanticRuleAppliedEvent")
        root.history.append({"event": "DgGraphPolicyIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphDigitalTwinRoot(AggregateRoot):
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
    ) -> "DgGraphDigitalTwinRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_10_required")
        if not present:
            raise ValueError("data_governance.graph.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeGraphUpdatedEvent")
        root.history.append({"event": "DgGraphDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphCqrsRoot(AggregateRoot):
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
    ) -> "DgGraphCqrsRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_11_required")
        if not present:
            raise ValueError("data_governance.graph.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeEntityCreatedEvent")
        root.history.append({"event": "DgGraphCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphEventSourcingRoot(AggregateRoot):
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
    ) -> "DgGraphEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_12_required")
        if not present:
            raise ValueError("data_governance.graph.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("KnowledgeGraphUpdatedEvent")
        root.history.append({"event": "DgGraphEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphMicroservicesRoot(AggregateRoot):
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
    ) -> "DgGraphMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_13_required")
        if not present:
            raise ValueError("data_governance.graph.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("OntologyCreatedEvent")
        root.history.append({"event": "DgGraphMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphZeroTrustRoot(AggregateRoot):
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
    ) -> "DgGraphZeroTrustRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_14_required")
        if not present:
            raise ValueError("data_governance.graph.zero_trust_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SemanticRuleAppliedEvent")
        root.history.append({"event": "DgGraphZeroTrustRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgGraphScalabilityRoot(AggregateRoot):
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
    ) -> "DgGraphScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.graph.tenant_15_required")
        if not present:
            raise ValueError("data_governance.graph.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("InferenceGeneratedEvent")
        root.history.append({"event": "DgGraphScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
