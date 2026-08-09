"""P219-E aggregates — civilization AI operating system invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class CivilizationAiOperatingSystemRoot(AggregateRoot):
    tenant_id: str; aios_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, aios_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.civilization_ai_operating_system_is_missing")
        return _mk(
            cls, tenant_id, "aios_ref", aios_ref,
            "civilization.ai_os.civilization_ai_operating_system_is_missing",
            "AIKernelActivatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiGovernanceKernelRoot(AggregateRoot):
    tenant_id: str; gov_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, gov_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.ai_governance_kernel_is_missing")
        return _mk(
            cls, tenant_id, "gov_ref", gov_ref,
            "civilization.ai_os.ai_governance_kernel_is_missing", "PolicyValidatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AutonomousCivilizationAgentsRoot(AggregateRoot):
    tenant_id: str; agents_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, agents_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.autonomous_civilization_agents_is_missing")
        return _mk(
            cls, tenant_id, "agents_ref", agents_ref,
            "civilization.ai_os.autonomous_civilization_agents_is_missing", "AgentActivatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationReasoningEngineRoot(AggregateRoot):
    tenant_id: str; reasoning_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, reasoning_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.civilization_reasoning_engine_is_missing")
        return _mk(
            cls, tenant_id, "reasoning_ref", reasoning_ref,
            "civilization.ai_os.civilization_reasoning_engine_is_missing",
            "ReasoningCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationAiFoundationModelsRoot(AggregateRoot):
    tenant_id: str; models_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, models_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.civilization_ai_foundation_models_is_missing")
        return _mk(
            cls, tenant_id, "models_ref", models_ref,
            "civilization.ai_os.civilization_ai_foundation_models_is_missing",
            "AIModelCreatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationAiCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.meos_civilization_ai_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.ai_os.meos_civilization_ai_core_is_missing",
            "DecisionGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AiDigitalTwinIntelligenceRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.ai_digital_twin_intelligence_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.ai_os.ai_digital_twin_intelligence_is_missing",
            "LearningCycleCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationAiKnowledgeRoot(AggregateRoot):
    tenant_id: str; knowledge_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, knowledge_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.civilization_ai_knowledge_architecture_is_missing")
        return _mk(
            cls, tenant_id, "knowledge_ref", knowledge_ref,
            "civilization.ai_os.civilization_ai_knowledge_architecture_is_missing",
            "AIModelUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationAiEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.ai_os.civilization_ai_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.ai_os.civilization_ai_event_architecture_is_missing",
            "RiskDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
