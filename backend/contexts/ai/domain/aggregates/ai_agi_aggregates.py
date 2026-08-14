"""P214-V aggregates — AGI cognitive-core invariants."""
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
class AGICoreRoot(AggregateRoot):
    tenant_id: str
    core_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.tenant_required")
        if not present:
            raise ValueError("ai.agi.enterprise_agi_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, core_ref=core_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AGICoreActivatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ReasoningRoot(AggregateRoot):
    tenant_id: str
    reasoning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.reasoning_tenant_required")
        if not present:
            raise ValueError("ai.agi.universal_reasoning_engine_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, reasoning_ref=reasoning_ref.strip(), present=True, status="enabled")
        root.pending_events.append("ReasoningCompletedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MemoryRoot(AggregateRoot):
    tenant_id: str
    memory_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, memory_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.memory_tenant_required")
        if not present:
            raise ValueError("ai.agi.enterprise_memory_architecture_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, memory_ref=memory_ref.strip(), present=True, status="enabled")
        root.pending_events.append("MemoryStateUpdatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class UnderstandingRoot(AggregateRoot):
    tenant_id: str
    understanding_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, understanding_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.understanding_tenant_required")
        if not present:
            raise ValueError("ai.agi.cognitive_intelligence_core_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, understanding_ref=understanding_ref.strip(), present=True, status="enabled")
        root.pending_events.append("KnowledgeIntegratedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class StrategicIntelligenceRoot(AggregateRoot):
    tenant_id: str
    strategic_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, strategic_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.strategic_tenant_required")
        if not present:
            raise ValueError("ai.agi.strategic_intelligence_engine_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, strategic_ref=strategic_ref.strip(), present=True, status="enabled")
        root.pending_events.append("StrategicInsightGeneratedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class LearningCoreRoot(AggregateRoot):
    tenant_id: str
    learning_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, learning_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.learning_tenant_required")
        if not present:
            raise ValueError("ai.agi.autonomous_learning_core_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, learning_ref=learning_ref.strip(), present=True, status="enabled")
        root.pending_events.append("LearningCompletedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DecisionIntelligenceRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.decision_tenant_required")
        if not present:
            raise ValueError("ai.agi.cognitive_decision_intelligence_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, decision_ref=decision_ref.strip(), present=True, status="enabled")
        root.pending_events.append("StrategicDecisionGeneratedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AGIDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.agi.twin_tenant_required")
        if not present:
            raise ValueError("ai.agi.digital_twin_integration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("CapabilityImprovedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present
