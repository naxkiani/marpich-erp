"""P211-M Digital twin & privacy simulation aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsCompleteDigitalRepresentationRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def synchronize(
        cls, *, tenant_id: str, twin_ref: str, complete: bool = True
    ) -> DsCompleteDigitalRepresentationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.tenant_required")
        if not complete:
            raise ValueError(
                "data_security.twin.digital_representation_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            twin_ref=twin_ref.strip(),
            complete=True,
            status="synchronized",
        )
        root.pending_events.append("TwinCreated")
        root.pending_events.append("TwinUpdated")
        root.pending_events.append("IncompleteDigitalRepresentationRejected")
        root.history.append({"event": "DigitalRepresentationComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsSimulatablePrivacyScenarioRoot(AggregateRoot):
    tenant_id: str
    scenario_ref: str
    simulatable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, scenario_ref: str, simulatable: bool = True
    ) -> DsSimulatablePrivacyScenarioRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.scenario_tenant_required")
        if not simulatable:
            raise ValueError(
                "data_security.twin.privacy_scenarios_cannot_be_simulated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scenario_ref=scenario_ref.strip(),
            simulatable=True,
            status="ready",
        )
        root.pending_events.append("ScenarioStarted")
        root.pending_events.append("UnsimulatablePrivacyScenarioRejected")
        root.history.append({"event": "PrivacyScenarioSimulatable"})
        return root

    def is_unsimulatable(self) -> bool:
        return not self.simulatable


@dataclass(eq=False, kw_only=True)
class DsAvailableRiskPredictionRoot(AggregateRoot):
    tenant_id: str
    prediction_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def predict(
        cls, *, tenant_id: str, prediction_ref: str, available: bool = True
    ) -> DsAvailableRiskPredictionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.risk_tenant_required")
        if not available:
            raise ValueError(
                "data_security.twin.risk_prediction_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            prediction_ref=prediction_ref.strip(),
            available=True,
            status="predicted",
        )
        root.pending_events.append("RiskPredicted")
        root.pending_events.append("UnavailableRiskPredictionRejected")
        root.history.append({"event": "RiskPredictionAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsMeasurableComplianceImpactRoot(AggregateRoot):
    tenant_id: str
    impact_ref: str
    measurable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def measure(
        cls, *, tenant_id: str, impact_ref: str, measurable: bool = True
    ) -> DsMeasurableComplianceImpactRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.compliance_tenant_required")
        if not measurable:
            raise ValueError(
                "data_security.twin.compliance_impact_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            impact_ref=impact_ref.strip(),
            measurable=True,
            status="measured",
        )
        root.pending_events.append("SimulationCompleted")
        root.pending_events.append("UnmeasurableComplianceImpactRejected")
        root.history.append({"event": "ComplianceImpactMeasurable"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class DsVisibleAiPrivacyRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def reveal(
        cls, *, tenant_id: str, risk_ref: str, visible: bool = True
    ) -> DsVisibleAiPrivacyRiskRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.ai_privacy_tenant_required")
        if not visible:
            raise ValueError(
                "data_security.twin.ai_privacy_risks_are_invisible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            visible=True,
            status="visible",
        )
        root.pending_events.append("RiskPredicted")
        root.pending_events.append("InvisibleAiPrivacyRiskRejected")
        root.history.append({"event": "AiPrivacyRiskVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsExplainableSimulationResultRoot(AggregateRoot):
    tenant_id: str
    result_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls, *, tenant_id: str, result_ref: str, explainable: bool = True
    ) -> DsExplainableSimulationResultRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.result_tenant_required")
        if not explainable:
            raise ValueError(
                "data_security.twin.simulation_results_are_not_explainable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            result_ref=result_ref.strip(),
            explainable=True,
            status="explained",
        )
        root.pending_events.append("SimulationCompleted")
        root.pending_events.append("UnexplainableSimulationResultRejected")
        root.history.append({"event": "SimulationResultExplainable"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class DsControlOptimizedRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    optimized: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def optimize(
        cls, *, tenant_id: str, control_ref: str, optimized: bool = True
    ) -> DsControlOptimizedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.control_tenant_required")
        if not optimized:
            raise ValueError("data_security.twin.control_not_optimized")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            optimized=True,
            status="optimized",
        )
        root.pending_events.append("ControlOptimized")
        root.history.append({"event": "ControlOptimized"})
        return root


@dataclass(eq=False, kw_only=True)
class DsSimulationCompletedRoot(AggregateRoot):
    tenant_id: str
    simulation_ref: str
    completed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls, *, tenant_id: str, simulation_ref: str, completed: bool = True
    ) -> DsSimulationCompletedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.twin.simulation_tenant_required")
        if not completed:
            raise ValueError("data_security.twin.simulation_not_completed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            simulation_ref=simulation_ref.strip(),
            completed=True,
            status="completed",
        )
        root.pending_events.append("SimulationCompleted")
        root.history.append({"event": "SimulationCompleted"})
        return root
