"""P214-S aggregates — quality-gate invariants."""
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
class ResearchPlatformRoot(AggregateRoot):
    tenant_id: str
    research_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, research_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.tenant_required")
        if not present:
            raise ValueError("ai.airesearch.enterprise_ai_research_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, research_ref=research_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ResearchStartedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class InnovationLabRoot(AggregateRoot):
    tenant_id: str
    innovation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, innovation_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.innovation_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.ai_innovation_lab_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, innovation_ref=innovation_ref.strip(), present=True, status="enabled")
        root.pending_events.append("InnovationValidatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ExperimentRoot(AggregateRoot):
    tenant_id: str
    experiment_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, experiment_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.experiment_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.experimentation_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, experiment_ref=experiment_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ExperimentExecutedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class PrototypeRoot(AggregateRoot):
    tenant_id: str
    prototype_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, prototype_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.prototype_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.prototype_factory_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, prototype_ref=prototype_ref.strip(), present=True, status="enabled")
        root.pending_events.append("PrototypeCreatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class TechnologyObservatoryRoot(AggregateRoot):
    tenant_id: str
    tech_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, tech_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.tech_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.future_intelligence_observatory_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, tech_ref=tech_ref.strip(), present=True, status="enabled")
        root.pending_events.append("BreakthroughDiscoveredEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgePlatformRoot(AggregateRoot):
    tenant_id: str
    knowledge_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.knowledge_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.scientific_knowledge_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, knowledge_ref=knowledge_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ResearchPublicationIndexedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BreakthroughRoot(AggregateRoot):
    tenant_id: str
    breakthrough_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, breakthrough_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.breakthrough_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.breakthrough_management_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, breakthrough_ref=breakthrough_ref.strip(), present=True, status="enabled")
        root.pending_events.append("BreakthroughDiscoveredEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class RoadmapRoot(AggregateRoot):
    tenant_id: str
    roadmap_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, roadmap_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.roadmap_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.ai_evolution_roadmap_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, roadmap_ref=roadmap_ref.strip(), present=True, status="enabled")
        root.pending_events.append("RoadmapUpdatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ResearchDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.airesearch.twin_tenant_required")
        if not present:
            raise ValueError("ai.airesearch.digital_twin_integration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("RoadmapUpdatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present
