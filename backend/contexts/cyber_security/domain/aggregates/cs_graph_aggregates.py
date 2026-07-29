"""P210-K Cyber Knowledge Graph aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsGraphSemanticRelationshipsRoot(AggregateRoot):
    tenant_id: str
    entity_ref: str
    has_semantic_relationships: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def link(
        cls,
        *,
        tenant_id: str,
        entity_ref: str,
        has_semantic_relationships: bool = True,
    ) -> CsGraphSemanticRelationshipsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.tenant_required")
        if not has_semantic_relationships:
            raise ValueError(
                "cyber_security.graph.security_entities_lack_semantic_relationships"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            entity_ref=entity_ref.strip(),
            has_semantic_relationships=True,
            status="linked",
        )
        root.pending_events.append("RelationshipDiscovered")
        root.pending_events.append("OrphanEntityRejected")
        root.history.append({"event": "SemanticRelationshipsBound"})
        return root

    def lacks_relationships(self) -> bool:
        return not self.has_semantic_relationships


@dataclass(eq=False, kw_only=True)
class CsGraphAttackPathCalculableRoot(AggregateRoot):
    tenant_id: str
    path_ref: str
    calculable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls, *, tenant_id: str, path_ref: str, calculable: bool = True
    ) -> CsGraphAttackPathCalculableRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.path_tenant_required")
        if not calculable:
            raise ValueError(
                "cyber_security.graph.attack_paths_cannot_be_calculated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            path_ref=path_ref.strip(),
            calculable=True,
            status="calculated",
        )
        root.pending_events.append("AttackPathGenerated")
        root.pending_events.append("IncalculablePathRejected")
        root.history.append({"event": "AttackPathCalculated"})
        return root

    def is_incalculable(self) -> bool:
        return not self.calculable


@dataclass(eq=False, kw_only=True)
class CsGraphLivingTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    living: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def sync(
        cls, *, tenant_id: str, twin_ref: str, living: bool = True
    ) -> CsGraphLivingTwinRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.twin_tenant_required")
        if not living:
            raise ValueError("cyber_security.graph.digital_twins_are_static")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            twin_ref=twin_ref.strip(),
            living=True,
            status="synchronized",
        )
        root.pending_events.append("StaticTwinRejected")
        root.history.append({"event": "LivingTwinSynced"})
        return root

    def is_static(self) -> bool:
        return not self.living


@dataclass(eq=False, kw_only=True)
class CsGraphAiReasoningRoot(AggregateRoot):
    tenant_id: str
    reasoning_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls, *, tenant_id: str, reasoning_ref: str, available: bool = True
    ) -> CsGraphAiReasoningRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.reason_tenant_required")
        if not available:
            raise ValueError("cyber_security.graph.ai_reasoning_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            reasoning_ref=reasoning_ref.strip(),
            available=True,
            status="executed",
        )
        root.pending_events.append("InsightGenerated")
        root.pending_events.append("UnavailableReasoningRejected")
        root.history.append({"event": "AiReasoningExecuted"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class CsGraphGovernanceRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assert_present(
        cls, *, tenant_id: str, governance_ref: str, present: bool = True
    ) -> CsGraphGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.gov_tenant_required")
        if not present:
            raise ValueError("cyber_security.graph.graph_governance_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            governance_ref=governance_ref.strip(),
            present=True,
            status="governed",
        )
        root.pending_events.append("MissingGovernanceRejected")
        root.history.append({"event": "GraphGovernancePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsGraphAccurateResolutionRoot(AggregateRoot):
    tenant_id: str
    resolution_ref: str
    accurate: bool
    confidence: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def resolve(
        cls,
        *,
        tenant_id: str,
        resolution_ref: str,
        accurate: bool = True,
        confidence: float = 0.9,
    ) -> CsGraphAccurateResolutionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.res_tenant_required")
        if not accurate or confidence < 0.5:
            raise ValueError(
                "cyber_security.graph.entity_resolution_inaccurate"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            resolution_ref=resolution_ref.strip(),
            accurate=True,
            confidence=confidence,
            status="resolved",
        )
        root.pending_events.append("EntityCreated")
        root.pending_events.append("InaccurateResolutionRejected")
        root.history.append({"event": "AccurateEntityResolution"})
        return root

    def is_inaccurate(self) -> bool:
        return not self.accurate or self.confidence < 0.5


@dataclass(eq=False, kw_only=True)
class CsGraphSimulationRoot(AggregateRoot):
    tenant_id: str
    simulation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls, *, tenant_id: str, simulation_ref: str, present: bool = True
    ) -> CsGraphSimulationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.sim_tenant_required")
        if not present:
            raise ValueError(
                "cyber_security.graph.simulation_capability_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            simulation_ref=simulation_ref.strip(),
            present=True,
            status="completed",
        )
        root.pending_events.append("SimulationStarted")
        root.pending_events.append("SimulationCompleted")
        root.pending_events.append("AbsentSimulationRejected")
        root.history.append({"event": "SimulationGenerated"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsGraphInsightGeneratedRoot(AggregateRoot):
    tenant_id: str
    insight_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls, *, tenant_id: str, insight_ref: str
    ) -> CsGraphInsightGeneratedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.graph.insight_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            insight_ref=insight_ref.strip(),
            status="generated",
        )
        root.pending_events.append("InsightGenerated")
        root.pending_events.append("ThreatMapped")
        root.pending_events.append("RiskPropagated")
        root.history.append({"event": "InsightGenerated"})
        return root
