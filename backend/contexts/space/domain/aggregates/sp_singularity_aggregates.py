"""P218-X aggregates — civilization singularity intelligence invariants."""
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
class SingularityCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.civilization_singularity_platform_is_missing")
        return _mk(cls, tenant_id, "core_ref", core_ref, "space.singularity.civilization_singularity_platform_is_missing", "IntelligenceCapabilityExpandedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class HumanAiSingularityRoot(AggregateRoot):
    tenant_id: str; singularity_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, singularity_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.human_ai_singularity_architecture_is_missing")
        return _mk(cls, tenant_id, "singularity_ref", singularity_ref, "space.singularity.human_ai_singularity_architecture_is_missing", "HumanAIIntegrationCreatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class PostHumanCivilizationRoot(AggregateRoot):
    tenant_id: str; post_human_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, post_human_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.post_human_civilization_systems_is_missing")
        return _mk(cls, tenant_id, "post_human_ref", post_human_ref, "space.singularity.post_human_civilization_systems_is_missing", "CivilizationModelOptimizedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CognitiveEvolutionRoot(AggregateRoot):
    tenant_id: str; evolution_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, evolution_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.cognitive_evolution_framework_is_missing")
        return _mk(cls, tenant_id, "evolution_ref", evolution_ref, "space.singularity.cognitive_evolution_framework_is_missing", "EvolutionStageReachedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationTransformationRoot(AggregateRoot):
    tenant_id: str; transformation_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, transformation_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.future_intelligence_modeling_is_missing")
        return _mk(cls, tenant_id, "transformation_ref", transformation_ref, "space.singularity.future_intelligence_modeling_is_missing", "CivilizationTransformationStartedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SingularityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "space.singularity.knowledge_graph_is_missing", "FutureScenarioGeneratedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SingularityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "space.singularity.digital_twin_is_missing", "SingularityRiskDetectedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SingularityAlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.alignment_architecture_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "space.singularity.alignment_architecture_is_missing", "IntelligenceAlignmentValidatedEvent")
    def is_missing(self) -> bool: return not self.present


@dataclass(eq=False, kw_only=True)
class SingularityGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str] = field(default_factory=list); history: list[dict] = field(default_factory=list); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("space.singularity.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "space.singularity.governance_is_missing", "GovernancePolicyUpdatedEvent")
    def is_missing(self) -> bool: return not self.present
