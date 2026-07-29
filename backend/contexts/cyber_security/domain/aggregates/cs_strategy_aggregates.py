"""P210-A Cyber Security strategy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsZeroTrustRequiredRoot(AggregateRoot):
    """Security architecture must be Zero Trust."""

    tenant_id: str
    plane_ref: str
    zero_trust: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls, *, tenant_id: str, plane_ref: str, zero_trust: bool = True
    ) -> CsZeroTrustRequiredRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.tenant_required")
        if not zero_trust:
            raise ValueError(
                "cyber_security.strategy.security_architecture_not_zero_trust"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plane_ref=plane_ref.strip(),
            zero_trust=True,
            status="enforced",
        )
        root.pending_events.append("ZeroTrustEnforced")
        root.history.append({"event": "ZeroTrustEnforced"})
        return root

    def is_missing_zero_trust(self) -> bool:
        return not self.zero_trust


@dataclass(eq=False, kw_only=True)
class CsEnterpriseSocRoot(AggregateRoot):
    """SOC must be enterprise-scale."""

    tenant_id: str
    soc_ref: str
    enterprise_scale: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, soc_ref: str, enterprise_scale: bool = True
    ) -> CsEnterpriseSocRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.soc_tenant_required")
        if not enterprise_scale:
            raise ValueError("cyber_security.strategy.soc_not_enterprise_scale")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            soc_ref=soc_ref.strip(),
            enterprise_scale=True,
            status="enabled",
        )
        root.pending_events.append("SocModelEnabled")
        root.history.append({"event": "EnterpriseSocEnabled"})
        return root

    def is_not_enterprise(self) -> bool:
        return not self.enterprise_scale


@dataclass(eq=False, kw_only=True)
class CsAiSecurityRequiredRoot(AggregateRoot):
    """AI security must not be omitted."""

    tenant_id: str
    surface_ref: str
    ai_security: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, surface_ref: str, ai_security: bool = True
    ) -> CsAiSecurityRequiredRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.ai_tenant_required")
        if not ai_security:
            raise ValueError("cyber_security.strategy.ai_security_omitted")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            surface_ref=surface_ref.strip(),
            ai_security=True,
            status="enabled",
        )
        root.history.append({"event": "AiSecurityEnabled"})
        return root

    def is_omitted(self) -> bool:
        return not self.ai_security


@dataclass(eq=False, kw_only=True)
class CsThreatIntelIntegratedRoot(AggregateRoot):
    """Threat intelligence must not be isolated."""

    tenant_id: str
    binding_ref: str
    isolated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, binding_ref: str, isolated: bool = False
    ) -> CsThreatIntelIntegratedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.intel_tenant_required")
        if isolated:
            raise ValueError(
                "cyber_security.strategy.threat_intelligence_isolated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            binding_ref=binding_ref.strip(),
            isolated=False,
            status="integrated",
        )
        root.pending_events.append("ThreatIntelligenceBound")
        root.pending_events.append("IsolatedIntelRejected")
        root.history.append({"event": "ThreatIntelIntegrated"})
        return root

    def is_isolated(self) -> bool:
        return self.isolated


@dataclass(eq=False, kw_only=True)
class CsResponseAutomationRoot(AggregateRoot):
    """Incident response must not be manual-only."""

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
    ) -> CsResponseAutomationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.response_tenant_required")
        if manual_only or not automated:
            raise ValueError(
                "cyber_security.strategy.incident_response_manual_only"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            manual_only=False,
            automated=True,
            status="automated",
        )
        root.pending_events.append("ResponseAutomationEnabled")
        root.pending_events.append("ManualOnlyResponseRejected")
        root.history.append({"event": "ResponseAutomationEnabled"})
        return root

    def is_manual_only(self) -> bool:
        return self.manual_only or not self.automated


@dataclass(eq=False, kw_only=True)
class CsTelemetryCoverageRoot(AggregateRoot):
    """Security telemetry must be complete."""

    tenant_id: str
    coverage_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, coverage_ref: str, complete: bool = True
    ) -> CsTelemetryCoverageRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.telemetry_tenant_required")
        if not complete:
            raise ValueError(
                "cyber_security.strategy.security_telemetry_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            coverage_ref=coverage_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("TelemetryCoverageDeclared")
        root.pending_events.append("IncompleteTelemetryRejected")
        root.history.append({"event": "TelemetryCoverageComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class CsMeasurableControlRoot(AggregateRoot):
    """Security controls must be measurable."""

    tenant_id: str
    control_ref: str
    measurable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, control_ref: str, measurable: bool = True
    ) -> CsMeasurableControlRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.control_tenant_required")
        if not measurable:
            raise ValueError(
                "cyber_security.strategy.security_controls_not_measurable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            measurable=True,
            status="registered",
        )
        root.pending_events.append("ControlRegistered")
        root.history.append({"event": "MeasurableControlRegistered"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class CsCloudNativeRoot(AggregateRoot):
    """Architecture must be cloud-native."""

    tenant_id: str
    profile_ref: str
    cloud_native: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def require(
        cls, *, tenant_id: str, profile_ref: str, cloud_native: bool = True
    ) -> CsCloudNativeRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.strategy.cloud_tenant_required")
        if not cloud_native:
            raise ValueError(
                "cyber_security.strategy.architecture_not_cloud_native"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            cloud_native=True,
            status="cloud_native",
        )
        root.pending_events.append("CyberStrategyPublished")
        root.history.append({"event": "CloudNativeRequired"})
        return root

    def is_non_cloud_native(self) -> bool:
        return not self.cloud_native
