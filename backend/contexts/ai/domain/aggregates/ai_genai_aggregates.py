"""P214-E aggregates — quality-gate invariants."""
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
class GenaiPlatformRoot(AggregateRoot):
    tenant_id: str
    platform_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.genai.tenant_required")
        if not present:
            raise ValueError("ai.genai.enterprise_generative_ai_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            platform_ref=platform_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("LLMRegisteredEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class FoundationModelRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.genai.model_tenant_required")
        if not present:
            raise ValueError("ai.genai.foundation_model_management_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ModelDeployedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PromptPlatformRoot(AggregateRoot):
    tenant_id: str
    prompt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, prompt_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.genai.prompt_tenant_required")
        if not present:
            raise ValueError("ai.genai.prompt_intelligence_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            prompt_ref=prompt_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PromptCreatedEvent")
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
        tid = _tid(tenant_id, "ai.genai.rag_tenant_required")
        if not present:
            raise ValueError("ai.genai.rag_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pipeline_ref=pipeline_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RAGPipelineCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AssistantPlatformRoot(AggregateRoot):
    tenant_id: str
    assistant_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, assistant_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "ai.genai.assistant_tenant_required")
        if not present:
            raise ValueError("ai.genai.ai_assistant_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            assistant_ref=assistant_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("GenerationRequestedEvent")
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
        tid = _tid(tenant_id, "ai.genai.vector_tenant_required")
        if not present:
            raise ValueError("ai.genai.vector_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            vector_ref=vector_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("GenerationCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
