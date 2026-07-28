"""P213-G aggregates — quality-gate invariants."""
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
class BiOlapProfileRoot(AggregateRoot):
    tenant_id: str
    profile_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, profile_ref: str, complete: bool = True):
        tid = _tid(tenant_id, "analytics.olap.tenant_required")
        if not complete:
            raise ValueError(
                "analytics.olap.olap_semantic_architecture_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            profile_ref=profile_ref.strip(),
            complete=True,
            status="published",
        )
        root.pending_events.append("MetricDefined")
        root.pending_events.append("SemanticModelPublishedEvent")
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class BiSemanticLayerRoot(AggregateRoot):
    tenant_id: str
    layer_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(cls, *, tenant_id: str, layer_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.olap.semantic_tenant_required")
        if not present:
            raise ValueError(
                "analytics.olap.enterprise_semantic_layer_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            layer_ref=layer_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("SemanticModelPublishedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiMetricPlatformRoot(AggregateRoot):
    tenant_id: str
    catalog_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, catalog_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.olap.metric_tenant_required")
        if not present:
            raise ValueError(
                "analytics.olap.enterprise_metric_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            catalog_ref=catalog_ref.strip(),
            present=True,
            status="published",
        )
        root.pending_events.append("MetricCreatedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiKpiGovernanceRoot(AggregateRoot):
    tenant_id: str
    governance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, governance_ref: str, present: bool = True
    ):
        tid = _tid(tenant_id, "analytics.olap.kpi_tenant_required")
        if not present:
            raise ValueError("analytics.olap.kpi_governance_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            governance_ref=governance_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("MetricApprovedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class BiCalculationEngineRoot(AggregateRoot):
    tenant_id: str
    engine_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, engine_ref: str, present: bool = True):
        tid = _tid(tenant_id, "analytics.olap.calc_tenant_required")
        if not present:
            raise ValueError("analytics.olap.calculation_engine_is_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            engine_ref=engine_ref.strip(),
            present=True,
            status="enabled",
        )
        root.pending_events.append("FormulaChangedEvent")
        return root

    def is_missing(self) -> bool:
        return not self.present
