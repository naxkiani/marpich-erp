"""P214-U aggregates — guardian-layer invariants."""
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
class AutonomousGovernanceRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.tenant_required")
        if not present:
            raise ValueError("ai.aigov.autonomous_ai_governance_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, governance_ref=governance_ref.strip(), present=True, status="enabled")
        root.pending_events.append("GovernanceActivatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SelfHealingRoot(AggregateRoot):
    tenant_id: str
    healing_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, healing_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.healing_tenant_required")
        if not present:
            raise ValueError("ai.aigov.self_healing_intelligence_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, healing_ref=healing_ref.strip(), present=True, status="enabled")
        root.pending_events.append("HealingTriggeredEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AlignmentRoot(AggregateRoot):
    tenant_id: str
    alignment_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.alignment_tenant_required")
        if not present:
            raise ValueError("ai.aigov.ai_alignment_platform_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, alignment_ref=alignment_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AlignmentValidatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SafetyRoot(AggregateRoot):
    tenant_id: str
    safety_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, safety_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.safety_tenant_required")
        if not present:
            raise ValueError("ai.aigov.ai_safety_framework_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, safety_ref=safety_ref.strip(), present=True, status="enabled")
        root.pending_events.append("SafetyViolationDetectedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionControlRoot(AggregateRoot):
    tenant_id: str
    evolution_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.evolution_tenant_required")
        if not present:
            raise ValueError("ai.aigov.evolution_control_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, evolution_ref=evolution_ref.strip(), present=True, status="enabled")
        root.pending_events.append("EvolutionApprovedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AGIReadinessRoot(AggregateRoot):
    tenant_id: str
    readiness_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, readiness_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.readiness_tenant_required")
        if not present:
            raise ValueError("ai.aigov.agi_readiness_model_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, readiness_ref=readiness_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AGIReadinessAssessedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class HumanCompatibilityRoot(AggregateRoot):
    tenant_id: str
    compatibility_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, compatibility_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.compatibility_tenant_required")
        if not present:
            raise ValueError("ai.aigov.human_compatibility_layer_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, compatibility_ref=compatibility_ref.strip(), present=True, status="enabled")
        root.pending_events.append("AlignmentValidatedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GuardianDigitalTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        tid = _tid(tenant_id, "ai.aigov.twin_tenant_required")
        if not present:
            raise ValueError("ai.aigov.digital_twin_integration_is_missing")
        root = cls(id=UniqueId.generate(), tenant_id=tid, twin_ref=twin_ref.strip(), present=True, status="enabled")
        root.pending_events.append("RiskPreventedEvent")
        return root
    def is_missing(self) -> bool:
        return not self.present
