"""P207-F Identity Digital Twin Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

SIMULATION_TYPES = frozenset(
    {
        "access_simulation",
        "privilege_simulation",
        "organization_simulation",
        "security_simulation",
        "lifecycle_simulation",
    }
)

IMPACT_DIMENSIONS = frozenset(
    {
        "business_impact",
        "security_impact",
        "compliance_impact",
        "operational_impact",
    }
)


@dataclass(eq=False, kw_only=True)
class IdentityTwinOrchestrationContractRoot(AggregateRoot):
    """Twin orchestration — never data-copy-only; never owns twin SoR."""

    tenant_id: str
    twin_ref: str
    peer_twin_ref: str
    intelligent: bool
    data_copy_only: bool
    owns_twin_sor: bool
    simulation_capable: bool
    realtime_sync: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        twin_ref: str,
        peer_twin_ref: str,
        intelligent: bool = True,
        data_copy_only: bool = False,
        owns_twin_sor: bool = False,
        simulation_capable: bool = True,
        realtime_sync: bool = True,
    ) -> IdentityTwinOrchestrationContractRoot:
        if not tenant_id.strip():
            raise ValueError("ii.twin.tenant_required")
        if data_copy_only or not intelligent:
            raise ValueError("ii.twin.twin_only_data_copy")
        if owns_twin_sor:
            raise ValueError("ii.twin.duplicates_twin_sor")
        if not simulation_capable:
            raise ValueError("ii.twin.simulation_capability_missing")
        if not realtime_sync:
            raise ValueError("ii.twin.realtime_sync_absent")
        if not peer_twin_ref.strip():
            raise ValueError("ii.twin.peer_ref_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            twin_ref=twin_ref.strip(),
            peer_twin_ref=peer_twin_ref.strip(),
            intelligent=True,
            data_copy_only=False,
            owns_twin_sor=False,
            simulation_capable=True,
            realtime_sync=True,
            status="active",
        )
        root.pending_events.append("TwinCreated")
        root.history.append({"event": "TwinCreated"})
        return root

    def is_data_copy_only(self) -> bool:
        return self.data_copy_only or not self.intelligent


@dataclass(eq=False, kw_only=True)
class TwinSyncSessionRoot(AggregateRoot):
    tenant_id: str
    session_ref: str
    twin_ref: str
    source_event: str
    realtime: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls,
        *,
        tenant_id: str,
        session_ref: str,
        twin_ref: str,
        source_event: str = "directory_changes",
        realtime: bool = True,
    ) -> TwinSyncSessionRoot:
        if not tenant_id.strip() or not twin_ref.strip():
            raise ValueError("ii.twin.sync_required")
        if not realtime:
            raise ValueError("ii.twin.realtime_sync_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            session_ref=session_ref.strip(),
            twin_ref=twin_ref.strip(),
            source_event=source_event.strip(),
            realtime=True,
            status="syncing",
        )
        root.history.append({"event": "TwinSyncStarted"})
        return root

    def complete(self) -> None:
        self.status = "synced"
        self.pending_events.append("TwinSynced")
        self.pending_events.append("TwinUpdated")
        self.history.append({"event": "TwinSynced"})

    def is_sync_absent(self) -> bool:
        return not self.realtime


@dataclass(eq=False, kw_only=True)
class TwinSimulationRunRoot(AggregateRoot):
    tenant_id: str
    run_ref: str
    twin_ref: str
    scenario_type: str
    isolated: bool
    mutation_applied: bool
    result_summary: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls,
        *,
        tenant_id: str,
        run_ref: str,
        twin_ref: str,
        scenario_type: str,
        isolated: bool = True,
        mutation_applied: bool = False,
        result_summary: str = "pending",
    ) -> TwinSimulationRunRoot:
        if not tenant_id.strip():
            raise ValueError("ii.twin.sim_tenant_required")
        st = scenario_type.strip().lower()
        if st not in SIMULATION_TYPES:
            raise ValueError("ii.twin.simulation_capability_missing")
        if not isolated:
            raise ValueError("ii.twin.simulation_not_isolated")
        if mutation_applied:
            raise ValueError("ii.twin.simulation_mutates_production")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            run_ref=run_ref.strip(),
            twin_ref=twin_ref.strip(),
            scenario_type=st,
            isolated=True,
            mutation_applied=False,
            result_summary=result_summary.strip() or "pending",
            status="running",
        )
        root.history.append({"event": "SimulationStarted"})
        return root

    def complete(self, *, result_summary: str) -> None:
        self.result_summary = result_summary.strip()
        self.status = "completed"
        self.pending_events.append("SimulationCompleted")
        self.history.append({"event": "SimulationCompleted"})

    def is_simulation_missing(self) -> bool:
        return self.scenario_type not in SIMULATION_TYPES


@dataclass(eq=False, kw_only=True)
class TwinImpactAnalysisRoot(AggregateRoot):
    tenant_id: str
    analysis_ref: str
    twin_ref: str
    dimensions: tuple[str, ...]
    available: bool
    summary: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def analyze(
        cls,
        *,
        tenant_id: str,
        analysis_ref: str,
        twin_ref: str,
        dimensions: tuple[str, ...] | None = None,
        available: bool = True,
        summary: str = "pending",
    ) -> TwinImpactAnalysisRoot:
        if not tenant_id.strip():
            raise ValueError("ii.twin.impact_tenant_required")
        if not available:
            raise ValueError("ii.twin.impact_analysis_unavailable")
        dims = dimensions if dimensions is not None else tuple(IMPACT_DIMENSIONS)
        if not dims or not set(dims).issubset(IMPACT_DIMENSIONS):
            raise ValueError("ii.twin.impact_analysis_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            analysis_ref=analysis_ref.strip(),
            twin_ref=twin_ref.strip(),
            dimensions=tuple(dims),
            available=True,
            summary=summary.strip() or "pending",
            status="analyzed",
        )
        root.pending_events.append("ImpactDetected")
        root.history.append({"event": "ImpactDetected"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available or len(self.dimensions) == 0


@dataclass(eq=False, kw_only=True)
class TwinPredictionCaseRoot(AggregateRoot):
    tenant_id: str
    case_ref: str
    twin_ref: str
    prediction: str
    confidence: float
    ai_strong: bool
    via_ai_platform: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def predict(
        cls,
        *,
        tenant_id: str,
        case_ref: str,
        twin_ref: str,
        prediction: str,
        confidence: float = 0.8,
        ai_strong: bool = True,
        via_ai_platform: bool = True,
    ) -> TwinPredictionCaseRoot:
        if not tenant_id.strip():
            raise ValueError("ii.twin.pred_tenant_required")
        if not prediction.strip():
            raise ValueError("ii.twin.ai_integration_weak")
        if not ai_strong or not via_ai_platform:
            raise ValueError("ii.twin.ai_integration_weak")
        if confidence < 0 or confidence > 1:
            raise ValueError("ii.twin.confidence_invalid")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            case_ref=case_ref.strip(),
            twin_ref=twin_ref.strip(),
            prediction=prediction.strip(),
            confidence=confidence,
            ai_strong=True,
            via_ai_platform=True,
            status="generated",
        )
        root.pending_events.append("PredictionGenerated")
        root.history.append({"event": "PredictionGenerated"})
        return root

    def is_weak_ai(self) -> bool:
        return not self.ai_strong or not self.via_ai_platform


@dataclass(eq=False, kw_only=True)
class TwinDecisionRecommendationRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    twin_ref: str
    recommendation: str
    confidence: float
    high_impact: bool
    hitl_approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def recommend(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        twin_ref: str,
        recommendation: str,
        confidence: float = 0.85,
        high_impact: bool = False,
        hitl_approved: bool = True,
    ) -> TwinDecisionRecommendationRoot:
        if not tenant_id.strip() or not recommendation.strip():
            raise ValueError("ii.twin.decision_required")
        if high_impact and not hitl_approved:
            raise ValueError("ii.twin.skips_hitl_high_impact")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            twin_ref=twin_ref.strip(),
            recommendation=recommendation.strip(),
            confidence=confidence,
            high_impact=high_impact,
            hitl_approved=hitl_approved if high_impact else True,
            status="recommended",
        )
        root.pending_events.append("OptimizationRecommended")
        root.history.append({"event": "OptimizationRecommended"})
        return root


@dataclass(eq=False, kw_only=True)
class TwinSecurityPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    security_controls_defined: bool
    simulation_isolation: bool
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        security_controls_defined: bool = True,
        simulation_isolation: bool = True,
        audited: bool = True,
    ) -> TwinSecurityPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.twin.sec_tenant_required")
        if not security_controls_defined:
            raise ValueError("ii.twin.security_controls_undefined")
        if not simulation_isolation:
            raise ValueError("ii.twin.simulation_not_isolated")
        if not audited:
            raise ValueError("ii.twin.actions_not_audited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            security_controls_defined=True,
            simulation_isolation=True,
            audited=True,
            status="active",
        )
        root.history.append({"event": "TwinSecurityDefined"})
        return root

    def is_undefined_security(self) -> bool:
        return not self.security_controls_defined
