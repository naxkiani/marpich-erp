"""P212-E Data Quality Intelligence aggregates — quality-gate invariants."""
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
class DgQualityArchitectureRoot(AggregateRoot):
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
    ) -> "DgQualityArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.quality.data_quality_intelligence_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("QualityCheckExecutedEvent")
        root.history.append({"event": "DgQualityArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DgQualityDddModelRoot(AggregateRoot):
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
    ) -> "DgQualityDddModelRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_1_required")
        if not present:
            raise ValueError("data_governance.quality.ddd_domain_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DataQualityAssessmentCompletedEvent")
        root.history.append({"event": "DgQualityDddModelRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityRuleArchitectureRoot(AggregateRoot):
    tenant_id: str
    rule_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, rule_ref: str, present: bool = True
    ) -> "DgQualityRuleArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_2_required")
        if not present:
            raise ValueError("data_governance.quality.quality_rule_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            rule_ref=rule_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityRuleCreatedEvent")
        root.history.append({"event": "DgQualityRuleArchitectureRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityMeasurementRoot(AggregateRoot):
    tenant_id: str
    measure_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, measure_ref: str, present: bool = True
    ) -> "DgQualityMeasurementRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_3_required")
        if not present:
            raise ValueError("data_governance.quality.quality_measurement_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            measure_ref=measure_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityScoreCalculatedEvent")
        root.history.append({"event": "DgQualityMeasurementRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityAiIntelligenceRoot(AggregateRoot):
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
    ) -> "DgQualityAiIntelligenceRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_4_required")
        if not present:
            raise ValueError("data_governance.quality.ai_quality_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityViolationDetectedEvent")
        root.history.append({"event": "DgQualityAiIntelligenceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityDataMeshRoot(AggregateRoot):
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
    ) -> "DgQualityDataMeshRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_5_required")
        if not present:
            raise ValueError("data_governance.quality.data_mesh_alignment_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityScoreUpdatedEvent")
        root.history.append({"event": "DgQualityDataMeshRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityKnowledgeGraphRoot(AggregateRoot):
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
    ) -> "DgQualityKnowledgeGraphRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_6_required")
        if not present:
            raise ValueError("data_governance.quality.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityRuleChangedEvent")
        root.history.append({"event": "DgQualityKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityDigitalTwinRoot(AggregateRoot):
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
    ) -> "DgQualityDigitalTwinRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_7_required")
        if not present:
            raise ValueError("data_governance.quality.digital_twin_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityImprovementRecordedEvent")
        root.history.append({"event": "DgQualityDigitalTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityCqrsRoot(AggregateRoot):
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
    ) -> "DgQualityCqrsRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_8_required")
        if not present:
            raise ValueError("data_governance.quality.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityIssueResolvedEvent")
        root.history.append({"event": "DgQualityCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityEventSourcingRoot(AggregateRoot):
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
    ) -> "DgQualityEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_9_required")
        if not present:
            raise ValueError("data_governance.quality.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityCheckExecutedEvent")
        root.history.append({"event": "DgQualityEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityMicroservicesRoot(AggregateRoot):
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
    ) -> "DgQualityMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_10_required")
        if not present:
            raise ValueError("data_governance.quality.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityScoreCalculatedEvent")
        root.history.append({"event": "DgQualityMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQualityScalabilityRoot(AggregateRoot):
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
    ) -> "DgQualityScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.quality.tenant_11_required")
        if not present:
            raise ValueError("data_governance.quality.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("QualityImprovementRecordedEvent")
        root.history.append({"event": "DgQualityScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
