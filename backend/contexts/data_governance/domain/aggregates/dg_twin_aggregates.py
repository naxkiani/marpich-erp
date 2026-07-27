"""P212-L Digital Twin aggregates — quality-gate invariants."""
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
class DgTwinArchitectureRoot(AggregateRoot):
    tenant_id: str
    architecture_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, architecture_ref: str, complete: bool = True
    ) -> "DgTwinArchitectureRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_0_required")
        if not complete:
            raise ValueError("data_governance.twin.data_governance_digital_twin_architecture_is_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            architecture_ref=architecture_ref.strip(),
            complete=True,
            status="ok",
        )
        root.pending_events.append("DigitalTwinCreatedEvent")
        root.history.append({"event": "DgTwinArchitectureRoot"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete



@dataclass(eq=False, kw_only=True)
class DgTwinStateModelRoot(AggregateRoot):
    tenant_id: str
    state_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, state_ref: str, present: bool = True
    ) -> "DgTwinStateModelRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_1_required")
        if not present:
            raise ValueError("data_governance.twin.governance_state_model_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            state_ref=state_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("StateCapturedEvent")
        root.history.append({"event": "DgTwinStateModelRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinSimulationEngineRoot(AggregateRoot):
    tenant_id: str
    simulation_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, simulation_ref: str, present: bool = True
    ) -> "DgTwinSimulationEngineRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_2_required")
        if not present:
            raise ValueError("data_governance.twin.simulation_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            simulation_ref=simulation_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SimulationStartedEvent")
        root.history.append({"event": "DgTwinSimulationEngineRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinWhatIfRoot(AggregateRoot):
    tenant_id: str
    whatif_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, whatif_ref: str, present: bool = True
    ) -> "DgTwinWhatIfRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_3_required")
        if not present:
            raise ValueError("data_governance.twin.what_if_analysis_platform_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            whatif_ref=whatif_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SimulationCompletedEvent")
        root.history.append({"event": "DgTwinWhatIfRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinRiskPredictionRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, risk_ref: str, present: bool = True
    ) -> "DgTwinRiskPredictionRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_4_required")
        if not present:
            raise ValueError("data_governance.twin.risk_prediction_intelligence_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            risk_ref=risk_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RiskPredictedEvent")
        root.history.append({"event": "DgTwinRiskPredictionRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinOptimizationRoot(AggregateRoot):
    tenant_id: str
    opt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, opt_ref: str, present: bool = True
    ) -> "DgTwinOptimizationRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_5_required")
        if not present:
            raise ValueError("data_governance.twin.optimization_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            opt_ref=opt_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("OptimizationGeneratedEvent")
        root.history.append({"event": "DgTwinOptimizationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinAiGovernanceRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> "DgTwinAiGovernanceRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_6_required")
        if not present:
            raise ValueError("data_governance.twin.ai_governance_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RiskPredictedEvent")
        root.history.append({"event": "DgTwinAiGovernanceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, graph_ref: str, present: bool = True
    ) -> "DgTwinKnowledgeGraphRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_7_required")
        if not present:
            raise ValueError("data_governance.twin.knowledge_graph_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DigitalTwinCreatedEvent")
        root.history.append({"event": "DgTwinKnowledgeGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinMeshIntegrationRoot(AggregateRoot):
    tenant_id: str
    mesh_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, mesh_ref: str, present: bool = True
    ) -> "DgTwinMeshIntegrationRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_8_required")
        if not present:
            raise ValueError("data_governance.twin.data_mesh_integration_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            mesh_ref=mesh_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SimulationStartedEvent")
        root.history.append({"event": "DgTwinMeshIntegrationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinPolicySimulationRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, policy_ref: str, present: bool = True
    ) -> "DgTwinPolicySimulationRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_9_required")
        if not present:
            raise ValueError("data_governance.twin.policy_simulation_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            policy_ref=policy_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SimulationCompletedEvent")
        root.history.append({"event": "DgTwinPolicySimulationRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinCqrsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, cqrs_ref: str, present: bool = True
    ) -> "DgTwinCqrsRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_10_required")
        if not present:
            raise ValueError("data_governance.twin.cqrs_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("StateCapturedEvent")
        root.history.append({"event": "DgTwinCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinEventSourcingRoot(AggregateRoot):
    tenant_id: str
    es_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, es_ref: str, present: bool = True
    ) -> "DgTwinEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_11_required")
        if not present:
            raise ValueError("data_governance.twin.event_sourcing_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("SimulationCompletedEvent")
        root.history.append({"event": "DgTwinEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinMicroservicesRoot(AggregateRoot):
    tenant_id: str
    ms_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, ms_ref: str, present: bool = True
    ) -> "DgTwinMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_12_required")
        if not present:
            raise ValueError("data_governance.twin.microservices_architecture_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("DigitalTwinCreatedEvent")
        root.history.append({"event": "DgTwinMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinZeroTrustRoot(AggregateRoot):
    tenant_id: str
    zt_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, zt_ref: str, present: bool = True
    ) -> "DgTwinZeroTrustRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_13_required")
        if not present:
            raise ValueError("data_governance.twin.zero_trust_security_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            zt_ref=zt_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("OptimizationGeneratedEvent")
        root.history.append({"event": "DgTwinZeroTrustRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present



@dataclass(eq=False, kw_only=True)
class DgTwinScalabilityRoot(AggregateRoot):
    tenant_id: str
    scale_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, scale_ref: str, present: bool = True
    ) -> "DgTwinScalabilityRoot":
        tid = _tid(tenant_id, "data_governance.twin.tenant_14_required")
        if not present:
            raise ValueError("data_governance.twin.enterprise_scalability_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scale_ref=scale_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("RiskPredictedEvent")
        root.history.append({"event": "DgTwinScalabilityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
