"""P213-I aggregates — quality-gate invariants."""
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
class BiAdvancedProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.advanced.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.advanced.advanced_analytics_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("AnalysisCompletedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiStatisticalAnalyticsRoot(AggregateRoot):
    tenant_id: str
    stats_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, stats_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.advanced.stats_tenant_required")
        if not present:
            raise ValueError(
                "analytics.advanced.statistical_intelligence_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            stats_ref=stats_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("AnalysisCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiExperimentationRoot(AggregateRoot):
    tenant_id: str
    experiment_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, experiment_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.advanced.exp_tenant_required")
        if not present:
            raise ValueError(
                "analytics.advanced.enterprise_experimentation_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            experiment_ref=experiment_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("ExperimentCompletedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiPatternDiscoveryRoot(AggregateRoot):
    tenant_id: str
    pattern_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, pattern_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.advanced.pattern_tenant_required")
        if not present:
            raise ValueError(
                "analytics.advanced.pattern_discovery_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            pattern_ref=pattern_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("PatternDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiRootCauseRoot(AggregateRoot):
    tenant_id: str
    rca_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, rca_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.advanced.rca_tenant_required")
        if not present:
            raise ValueError(
                "analytics.advanced.root_cause_analytics_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            rca_ref=rca_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("RootCauseDetectedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiInsightManagementRoot(AggregateRoot):
    tenant_id: str
    insight_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, insight_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.advanced.insight_tenant_required")
        if not present:
            raise ValueError(
                "analytics.advanced.insight_management_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            insight_ref=insight_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("InsightGeneratedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
