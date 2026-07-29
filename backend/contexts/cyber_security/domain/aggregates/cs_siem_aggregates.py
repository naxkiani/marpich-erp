"""P210-E Enterprise SIEM aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsSiemNormalizationCompleteRoot(AggregateRoot):
    tenant_id: str
    event_ref: str
    normalized: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def normalize(
        cls, *, tenant_id: str, event_ref: str, normalized: bool = True
    ) -> CsSiemNormalizationCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.tenant_required")
        if not normalized:
            raise ValueError("cyber_security.siem.event_normalization_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            event_ref=event_ref.strip(),
            normalized=True,
            status="normalized",
        )
        root.pending_events.append("EventNormalized")
        root.pending_events.append("IncompleteNormalizationRejected")
        root.history.append({"event": "EventNormalized"})
        return root

    def is_incomplete(self) -> bool:
        return not self.normalized


@dataclass(eq=False, kw_only=True)
class CsSiemMultiDomainCorrelationRoot(AggregateRoot):
    tenant_id: str
    correlation_ref: str
    multi_domain: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def correlate(
        cls,
        *,
        tenant_id: str,
        correlation_ref: str,
        multi_domain: bool = True,
    ) -> CsSiemMultiDomainCorrelationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.corr_tenant_required")
        if not multi_domain:
            raise ValueError(
                "cyber_security.siem.correlation_cannot_span_multiple_domains"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            correlation_ref=correlation_ref.strip(),
            multi_domain=True,
            status="correlated",
        )
        root.pending_events.append("ThreatCorrelated")
        root.pending_events.append("SingleDomainCorrelationRejected")
        root.history.append({"event": "MultiDomainCorrelated"})
        return root

    def is_single_domain_only(self) -> bool:
        return not self.multi_domain


@dataclass(eq=False, kw_only=True)
class CsSiemExtensibleDetectionRoot(AggregateRoot):
    tenant_id: str
    rule_ref: str
    extensible: bool
    version: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def update(
        cls,
        *,
        tenant_id: str,
        rule_ref: str,
        extensible: bool = True,
        version: str = "1.0.0",
    ) -> CsSiemExtensibleDetectionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.rule_tenant_required")
        if not extensible or not version.strip():
            raise ValueError(
                "cyber_security.siem.detection_rules_not_extensible"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            rule_ref=rule_ref.strip(),
            extensible=True,
            version=version.strip(),
            status="updated",
        )
        root.pending_events.append("RuleTriggered")
        root.pending_events.append("NonExtensibleRulesRejected")
        root.history.append({"event": "DetectionRuleUpdated"})
        return root

    def is_non_extensible(self) -> bool:
        return not self.extensible or not self.version


@dataclass(eq=False, kw_only=True)
class CsSiemAiIntelligenceRoot(AggregateRoot):
    tenant_id: str
    intelligence_ref: str
    present: bool
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        intelligence_ref: str,
        present: bool = True,
        explainable: bool = True,
    ) -> CsSiemAiIntelligenceRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.ai_tenant_required")
        if not present:
            raise ValueError("cyber_security.siem.ai_intelligence_absent")
        if not explainable:
            raise ValueError("cyber_security.siem.ai_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            intelligence_ref=intelligence_ref.strip(),
            present=True,
            explainable=True,
            status="enabled",
        )
        root.pending_events.append("AbsentAiRejected")
        root.history.append({"event": "AiIntelligenceEnabled"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsSiemTelemetryIntegrityRoot(AggregateRoot):
    tenant_id: str
    telemetry_ref: str
    integrity_validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        telemetry_ref: str,
        integrity_validated: bool = True,
    ) -> CsSiemTelemetryIntegrityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.telemetry_tenant_required")
        if not integrity_validated:
            raise ValueError(
                "cyber_security.siem.telemetry_lacks_integrity_validation"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            telemetry_ref=telemetry_ref.strip(),
            integrity_validated=True,
            status="validated",
        )
        root.pending_events.append("TelemetryReceived")
        root.pending_events.append("UnvalidatedTelemetryRejected")
        root.history.append({"event": "TelemetryIntegrityValidated"})
        return root

    def lacks_integrity(self) -> bool:
        return not self.integrity_validated


@dataclass(eq=False, kw_only=True)
class CsSiemImmutableStorageRoot(AggregateRoot):
    tenant_id: str
    store_ref: str
    immutable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, store_ref: str, immutable: bool = True
    ) -> CsSiemImmutableStorageRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.store_tenant_required")
        if not immutable:
            raise ValueError("cyber_security.siem.storage_not_immutable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            store_ref=store_ref.strip(),
            immutable=True,
            status="bound",
        )
        root.pending_events.append("MutableStorageRejected")
        root.history.append({"event": "ImmutableStorageBound"})
        return root

    def is_mutable(self) -> bool:
        return not self.immutable


@dataclass(eq=False, kw_only=True)
class CsSiemHorizontalScaleRoot(AggregateRoot):
    tenant_id: str
    plane_ref: str
    horizontal: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, plane_ref: str, horizontal: bool = True
    ) -> CsSiemHorizontalScaleRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.scale_tenant_required")
        if not horizontal:
            raise ValueError(
                "cyber_security.siem.platform_cannot_scale_horizontally"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plane_ref=plane_ref.strip(),
            horizontal=True,
            status="enabled",
        )
        root.pending_events.append("VerticalOnlyScaleRejected")
        root.history.append({"event": "HorizontalScaleEnabled"})
        return root

    def is_vertical_only(self) -> bool:
        return not self.horizontal


@dataclass(eq=False, kw_only=True)
class CsSiemAlertGeneratedRoot(AggregateRoot):
    tenant_id: str
    alert_ref: str
    severity: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls, *, tenant_id: str, alert_ref: str, severity: str = "high"
    ) -> CsSiemAlertGeneratedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.siem.alert_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            alert_ref=alert_ref.strip(),
            severity=severity.strip(),
            status="generated",
        )
        root.pending_events.append("AlertGenerated")
        root.pending_events.append("AlertEscalated")
        root.history.append({"event": "AlertGenerated"})
        return root
