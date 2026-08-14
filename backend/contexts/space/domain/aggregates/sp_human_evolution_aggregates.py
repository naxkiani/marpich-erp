"""P218-U aggregates — human evolution intelligence invariants."""
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
        id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()},
        present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class HumanAugmentationRoot(AggregateRoot):
    tenant_id: str; augmentation_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, augmentation_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.human_augmentation_platform_is_missing")
        return _mk(cls, tenant_id, "augmentation_ref", augmentation_ref, "space.human_evolution.human_augmentation_platform_is_missing", "AugmentationApprovedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanMachineSymbiosisRoot(AggregateRoot):
    tenant_id: str; symbiosis_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, symbiosis_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.human_machine_symbiosis_is_missing")
        return _mk(cls, tenant_id, "symbiosis_ref", symbiosis_ref, "space.human_evolution.human_machine_symbiosis_is_missing", "SymbiosisSessionStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CognitiveEnhancementRoot(AggregateRoot):
    tenant_id: str; cognitive_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, cognitive_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.cognitive_enhancement_is_missing")
        return _mk(cls, tenant_id, "cognitive_ref", cognitive_ref, "space.human_evolution.cognitive_enhancement_is_missing", "CognitiveImprovementDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class NeuralIntelligenceRoot(AggregateRoot):
    tenant_id: str; neural_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, neural_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.neural_intelligence_is_missing")
        return _mk(cls, tenant_id, "neural_ref", neural_ref, "space.human_evolution.neural_intelligence_is_missing", "NeuralConsentCapturedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CapabilityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.human_capability_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.human_evolution.human_capability_digital_twin_is_missing", "HumanCapabilityExpandedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionAiRoot(AggregateRoot):
    tenant_id: str; evolution_ai_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ai_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.evolution_ai_is_missing")
        return _mk(cls, tenant_id, "evolution_ai_ref", evolution_ai_ref, "space.human_evolution.evolution_ai_is_missing", "EvolutionScenarioGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionEthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.ethics_framework_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "space.human_evolution.ethics_framework_is_missing", "EthicalAssessmentCompletedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.human_evolution.knowledge_graph_is_missing", "AICompanionConnectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class EvolutionGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.human_evolution.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.human_evolution.governance_is_missing", "HumanSovereigntyValidatedEvent")
    def is_missing(self) -> bool: return not self.present
