"""P213-L aggregates — quality-gate invariants."""
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
class BiGraphProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.graph.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.graph.decision_knowledge_graph_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("DecisionNodeCreatedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiDecisionOntologyRoot(AggregateRoot):
    tenant_id: str
    ontology_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, ontology_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.graph.ont_tenant_required")
        if not present:
            raise ValueError(
                "analytics.graph.enterprise_decision_ontology_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ontology_ref=ontology_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("OntologyPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDecisionMemoryRoot(AggregateRoot):
    tenant_id: str
    memory_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.graph.mem_tenant_required")
        if not present:
            raise ValueError(
                "analytics.graph.enterprise_decision_memory_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            memory_ref=memory_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DecisionOutcomeRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiDecisionLineageRoot(AggregateRoot):
    tenant_id: str
    lineage_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, lineage_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.graph.lin_tenant_required")
        if not present:
            raise ValueError(
                "analytics.graph.decision_lineage_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            lineage_ref=lineage_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DecisionLinkedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiGraphAnalyticsRoot(AggregateRoot):
    tenant_id: str
    analytics_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, analytics_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.graph.ga_tenant_required")
        if not present:
            raise ValueError("analytics.graph.graph_analytics_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            analytics_ref=analytics_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("GraphUpdatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiAiReasoningRoot(AggregateRoot):
    tenant_id: str
    reasoning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, reasoning_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.graph.ai_tenant_required")
        if not present:
            raise ValueError("analytics.graph.ai_reasoning_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            reasoning_ref=reasoning_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("DecisionReasoningCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
