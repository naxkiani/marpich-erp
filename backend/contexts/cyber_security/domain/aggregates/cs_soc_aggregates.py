"""P210-D Enterprise SOC aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsSoc24x7Root(AggregateRoot):
    tenant_id: str
    profile_ref: str
    operating_24x7: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, profile_ref: str, operating_24x7: bool = True
    ) -> CsSoc24x7Root:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.tenant_required")
        if not operating_24x7:
            raise ValueError("cyber_security.soc.soc_not_24x7")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            operating_24x7=True,
            status="enabled",
        )
        root.pending_events.append("Non24x7Rejected")
        root.history.append({"event": "Soc24x7Enabled"})
        return root

    def is_non_24x7(self) -> bool:
        return not self.operating_24x7


@dataclass(eq=False, kw_only=True)
class CsAlertCorrelationRoot(AggregateRoot):
    tenant_id: str
    alert_ref: str
    correlated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def correlate(
        cls, *, tenant_id: str, alert_ref: str, correlated: bool = True
    ) -> CsAlertCorrelationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.corr_tenant_required")
        if not correlated:
            raise ValueError("cyber_security.soc.alerts_cannot_be_correlated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            alert_ref=alert_ref.strip(),
            correlated=True,
            status="correlated",
        )
        root.pending_events.append("AlertCorrelated")
        root.pending_events.append("UncorrelatedAlertsRejected")
        root.history.append({"event": "AlertCorrelated"})
        return root

    def cannot_correlate(self) -> bool:
        return not self.correlated


@dataclass(eq=False, kw_only=True)
class CsSocAiAssistanceRoot(AggregateRoot):
    tenant_id: str
    surface_ref: str
    ai_assistance: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, surface_ref: str, ai_assistance: bool = True
    ) -> CsSocAiAssistanceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.ai_tenant_required")
        if not ai_assistance:
            raise ValueError("cyber_security.soc.ai_assistance_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            surface_ref=surface_ref.strip(),
            ai_assistance=True,
            status="enabled",
        )
        root.pending_events.append("MissingAiRejected")
        root.history.append({"event": "SocAiAssistanceEnabled"})
        return root

    def is_absent(self) -> bool:
        return not self.ai_assistance


@dataclass(eq=False, kw_only=True)
class CsSocResponseAutomationRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    manual_only: bool
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        manual_only: bool = False,
        automated: bool = True,
    ) -> CsSocResponseAutomationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.resp_tenant_required")
        if manual_only or not automated:
            raise ValueError(
                "cyber_security.soc.incident_response_manual_only"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            manual_only=False,
            automated=True,
            status="automated",
        )
        root.pending_events.append("PlaybookIntentExecuted")
        root.pending_events.append("ManualOnlyResponseRejected")
        root.history.append({"event": "SocResponseAutomationEnabled"})
        return root

    def is_manual_only(self) -> bool:
        return self.manual_only or not self.automated


@dataclass(eq=False, kw_only=True)
class CsThreatHuntingRequiredRoot(AggregateRoot):
    tenant_id: str
    hunt_ref: str
    hunting_enabled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls, *, tenant_id: str, hunt_ref: str, hunting_enabled: bool = True
    ) -> CsThreatHuntingRequiredRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.hunt_tenant_required")
        if not hunting_enabled:
            raise ValueError("cyber_security.soc.threat_hunting_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            hunt_ref=hunt_ref.strip(),
            hunting_enabled=True,
            status="active",
        )
        root.pending_events.append("ThreatHuntStarted")
        root.history.append({"event": "ThreatHuntingEnabled"})
        return root

    def is_missing(self) -> bool:
        return not self.hunting_enabled


@dataclass(eq=False, kw_only=True)
class CsSocMetricsCompleteRoot(AggregateRoot):
    tenant_id: str
    metrics_ref: str
    complete: bool
    metric_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        metrics_ref: str,
        complete: bool = True,
        metric_count: int = 7,
    ) -> CsSocMetricsCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.metrics_tenant_required")
        if not complete or metric_count < 5:
            raise ValueError("cyber_security.soc.metrics_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            metrics_ref=metrics_ref.strip(),
            complete=True,
            metric_count=metric_count,
            status="registered",
        )
        root.pending_events.append("IncompleteMetricsRejected")
        root.history.append({"event": "SocMetricsComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete or self.metric_count < 5


@dataclass(eq=False, kw_only=True)
class CsSocKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str
    link_ref: str
    integrated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def link(
        cls, *, tenant_id: str, link_ref: str, integrated: bool = True
    ) -> CsSocKnowledgeGraphRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.kg_tenant_required")
        if not integrated:
            raise ValueError(
                "cyber_security.soc.knowledge_graph_integration_absent"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            link_ref=link_ref.strip(),
            integrated=True,
            status="linked",
        )
        root.history.append({"event": "SocKnowledgeGraphLinked"})
        return root

    def is_absent(self) -> bool:
        return not self.integrated


@dataclass(eq=False, kw_only=True)
class CsSocAlertRoot(AggregateRoot):
    tenant_id: str
    alert_ref: str
    severity: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, alert_ref: str, severity: str = "high"
    ) -> CsSocAlertRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.soc.alert_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            alert_ref=alert_ref.strip(),
            severity=severity.strip() or "high",
            status="open",
        )
        root.pending_events.append("AlertGenerated")
        root.history.append({"event": "AlertCreated"})
        return root
