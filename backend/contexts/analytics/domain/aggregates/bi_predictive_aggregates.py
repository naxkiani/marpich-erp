"""P213-J aggregates — quality-gate invariants."""
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
class BiPredictiveProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.predictive.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.predictive.predictive_analytics_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("ForecastPublishedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiForecastManagementRoot(AggregateRoot):
    tenant_id: str
    forecast_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, forecast_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.predictive.fc_tenant_required")
        if not present:
            raise ValueError(
                "analytics.predictive.enterprise_forecasting_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            forecast_ref=forecast_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ForecastRequestedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiPredictiveModelingRoot(AggregateRoot):
    tenant_id: str
    model_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, model_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.predictive.model_tenant_required")
        if not present:
            raise ValueError(
                "analytics.predictive.predictive_modeling_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            model_ref=model_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PredictionCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiScenarioPredictionRoot(AggregateRoot):
    tenant_id: str
    scenario_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, scenario_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.predictive.sc_tenant_required")
        if not present:
            raise ValueError(
                "analytics.predictive.scenario_prediction_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            scenario_ref=scenario_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ScenarioSimulatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiTimeSeriesIntelligenceRoot(AggregateRoot):
    tenant_id: str
    series_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, series_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.predictive.ts_tenant_required")
        if not present:
            raise ValueError(
                "analytics.predictive.time_series_intelligence_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            series_ref=series_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ForecastGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiExplainableAiRoot(AggregateRoot):
    tenant_id: str
    xai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, xai_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.predictive.xai_tenant_required")
        if not present:
            raise ValueError(
                "analytics.predictive.explainable_ai_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            xai_ref=xai_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ForecastGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
