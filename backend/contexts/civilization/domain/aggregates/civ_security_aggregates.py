"""P219-M aggregates — civilization security intelligence core invariants."""
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
        id=UniqueId.generate(), tenant_id=tid,
        **{ref_name: ref_value.strip()}, present=True, status="enabled",
    )
    obj.pending_events.append(event)
    return obj


@dataclass(eq=False, kw_only=True)
class CivilizationSecurityIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.civilization_security_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "security_ref", security_ref,
            "civilization.security.civilization_security_intelligence_platform_is_missing",
            "ThreatDetectedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class GlobalRiskIntelligencePlatformRoot(AggregateRoot):
    tenant_id: str; risk_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, risk_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.global_risk_intelligence_platform_is_missing")
        return _mk(
            cls, tenant_id, "risk_ref", risk_ref,
            "civilization.security.global_risk_intelligence_platform_is_missing",
            "RiskIdentifiedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class ThreatIntelligenceNetworkRoot(AggregateRoot):
    tenant_id: str; threat_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, threat_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.threat_intelligence_network_is_missing")
        return _mk(
            cls, tenant_id, "threat_ref", threat_ref,
            "civilization.security.threat_intelligence_network_is_missing",
            "ThreatNeutralizedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class AdaptiveSecurityArchitectureRoot(AggregateRoot):
    tenant_id: str; adaptive_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, adaptive_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.adaptive_security_architecture_is_missing")
        return _mk(
            cls, tenant_id, "adaptive_ref", adaptive_ref,
            "civilization.security.adaptive_security_architecture_is_missing",
            "SecurityControlUpdatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CivilizationResiliencePlatformRoot(AggregateRoot):
    tenant_id: str; resilience_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, resilience_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.civilization_resilience_platform_is_missing")
        return _mk(
            cls, tenant_id, "resilience_ref", resilience_ref,
            "civilization.security.civilization_resilience_platform_is_missing",
            "ContinuityRestoredEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.security_digital_twin_is_missing")
        return _mk(
            cls, tenant_id, "twin_ref", twin_ref,
            "civilization.security.security_digital_twin_is_missing",
            "RiskForecastGeneratedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class MeosCivilizationSecurityIntelligenceCoreRoot(AggregateRoot):
    tenant_id: str; core_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, core_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.meos_civilization_security_intelligence_core_is_missing")
        return _mk(
            cls, tenant_id, "core_ref", core_ref,
            "civilization.security.meos_civilization_security_intelligence_core_is_missing",
            "IncidentResolvedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.security_knowledge_graph_is_missing")
        return _mk(
            cls, tenant_id, "kg_ref", kg_ref,
            "civilization.security.security_knowledge_graph_is_missing",
            "RiskMitigatedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecurityEventArchitectureRoot(AggregateRoot):
    tenant_id: str; events_ref: str; present: bool; status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(cls, *, tenant_id: str, events_ref: str, present: bool = True):
        if not present:
            raise ValueError("civilization.security.security_event_architecture_is_missing")
        return _mk(
            cls, tenant_id, "events_ref", events_ref,
            "civilization.security.security_event_architecture_is_missing",
            "RecoveryCompletedEvent",
        )

    def is_missing(self) -> bool:
        return not self.present
