"""P214-W aggregates — civilization-layer invariants."""
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
class CivilizationRoot(AggregateRoot):
    tenant_id: str
    civilization_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, civilization_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.tenant_required")
        if not present:
            raise ValueError("ai.aiciv.enterprise_ai_civilization_layer_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, civilization_ref=civilization_ref.strip(), present=True, status="enabled")
        root.pending_events.append("NetworkCreatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class NetworkRoot(AggregateRoot):
    tenant_id: str
    network_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, network_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.network_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.collective_intelligence_network_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, network_ref=network_ref.strip(), present=True, status="enabled")
        root.pending_events.append("NetworkCreatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class KnowledgeCivilizationRoot(AggregateRoot):
    tenant_id: str
    knowledge_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.knowledge_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.knowledge_civilization_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, knowledge_ref=knowledge_ref.strip(), present=True, status="enabled")
        root.pending_events.append("KnowledgeSharedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanCollaborationRoot(AggregateRoot):
    tenant_id: str
    collaboration_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, collaboration_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.collab_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.human_ai_collaboration_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, collaboration_ref=collaboration_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ContributionAddedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DistributedIntelligenceRoot(AggregateRoot):
    tenant_id: str
    distributed_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, distributed_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.dist_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.distributed_intelligence_fabric_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, distributed_ref=distributed_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ContributionAddedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CollectiveDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.decision_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.collective_decision_intelligence_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, decision_ref=decision_ref.strip(), present=True, status="enabled")
        root.pending_events.append("DecisionGeneratedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LearningCivilizationRoot(AggregateRoot):
    tenant_id: str
    learning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.learning_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.learning_ecosystem_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, learning_ref=learning_ref.strip(), present=True, status="enabled")
        root.pending_events.append("LearningCompletedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aiciv.twin_tenant_required")
        if not present:
            raise ValueError("ai.aiciv.digital_twin_integration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("EvolutionReachedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present
