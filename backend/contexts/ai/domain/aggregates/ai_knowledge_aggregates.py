"""P214-G aggregates — quality-gate invariants."""
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
class KnowledgePlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.tenant_required")
        if not present:
            raise ValueError(
                "ai.knowledge.enterprise_ai_knowledge_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("KnowledgeAssetCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class RagPlatformRoot(AggregateRoot):
    tenant_id: str
    pipeline_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, pipeline_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.rag_tenant_required")
        if not present:
            raise ValueError("ai.knowledge.rag_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pipeline_ref=pipeline_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RAGResponseGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class VectorIntelligenceRoot(AggregateRoot):
    tenant_id: str
    vector_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, vector_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.vector_tenant_required")
        if not present:
            raise ValueError(
                "ai.knowledge.vector_intelligence_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            vector_ref=vector_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("EmbeddingGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.graph_tenant_required")
        if not present:
            raise ValueError(
                "ai.knowledge.knowledge_graph_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("KnowledgeIndexedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiMemoryRoot(AggregateRoot):
    tenant_id: str
    memory_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.memory_tenant_required")
        if not present:
            raise ValueError("ai.knowledge.ai_memory_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            memory_ref=memory_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ContextCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ContextEngineRoot(AggregateRoot):
    tenant_id: str
    context_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, context_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.knowledge.context_tenant_required")
        if not present:
            raise ValueError("ai.knowledge.context_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            context_ref=context_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("KnowledgeRetrievedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
