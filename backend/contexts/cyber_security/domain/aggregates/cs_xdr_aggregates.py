"""P210-G Enterprise XDR/EDR/NDR aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsXdrEndpointTelemetryCompleteRoot(AggregateRoot):
    tenant_id: str
    endpoint_ref: str
    telemetry_complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def collect(
        cls,
        *,
        tenant_id: str,
        endpoint_ref: str,
        telemetry_complete: bool = True,
    ) -> CsXdrEndpointTelemetryCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.tenant_required")
        if not telemetry_complete:
            raise ValueError("cyber_security.xdr.endpoint_telemetry_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            endpoint_ref=endpoint_ref.strip(),
            telemetry_complete=True,
            status="collected",
        )
        root.pending_events.append("TelemetryCollected")
        root.pending_events.append("IncompleteTelemetryRejected")
        root.history.append({"event": "EndpointTelemetryComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.telemetry_complete


@dataclass(eq=False, kw_only=True)
class CsXdrNetworkVisibilityRoot(AggregateRoot):
    tenant_id: str
    sensor_ref: str
    visibility_sufficient: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def cover(
        cls,
        *,
        tenant_id: str,
        sensor_ref: str,
        visibility_sufficient: bool = True,
    ) -> CsXdrNetworkVisibilityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.ndr_tenant_required")
        if not visibility_sufficient:
            raise ValueError(
                "cyber_security.xdr.network_visibility_insufficient"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            sensor_ref=sensor_ref.strip(),
            visibility_sufficient=True,
            status="covered",
        )
        root.pending_events.append("InsufficientVisibilityRejected")
        root.history.append({"event": "NetworkVisibilitySufficient"})
        return root

    def is_insufficient(self) -> bool:
        return not self.visibility_sufficient


@dataclass(eq=False, kw_only=True)
class CsXdrUnifiedCorrelationRoot(AggregateRoot):
    tenant_id: str
    correlation_ref: str
    siloed: bool
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
        siloed: bool = False,
    ) -> CsXdrUnifiedCorrelationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.corr_tenant_required")
        if siloed:
            raise ValueError("cyber_security.xdr.xdr_correlation_siloed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            correlation_ref=correlation_ref.strip(),
            siloed=False,
            status="unified",
        )
        root.pending_events.append("ThreatCorrelated")
        root.pending_events.append("SiloedCorrelationRejected")
        root.history.append({"event": "UnifiedCorrelation"})
        return root

    def is_siloed(self) -> bool:
        return self.siloed


@dataclass(eq=False, kw_only=True)
class CsXdrAiAnalyticsRoot(AggregateRoot):
    tenant_id: str
    analytics_ref: str
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
        analytics_ref: str,
        present: bool = True,
        explainable: bool = True,
    ) -> CsXdrAiAnalyticsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.ai_tenant_required")
        if not present:
            raise ValueError("cyber_security.xdr.ai_analytics_absent")
        if not explainable:
            raise ValueError("cyber_security.xdr.ai_not_explainable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            analytics_ref=analytics_ref.strip(),
            present=True,
            explainable=True,
            status="enabled",
        )
        root.pending_events.append("AbsentAiRejected")
        root.history.append({"event": "AiAnalyticsEnabled"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsXdrEvolvableDetectionRoot(AggregateRoot):
    tenant_id: str
    rule_ref: str
    evolvable: bool
    version: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def deploy(
        cls,
        *,
        tenant_id: str,
        rule_ref: str,
        evolvable: bool = True,
        version: str = "1.0.0",
    ) -> CsXdrEvolvableDetectionRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.rule_tenant_required")
        if not evolvable or not version.strip():
            raise ValueError(
                "cyber_security.xdr.detection_rules_cannot_evolve"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            rule_ref=rule_ref.strip(),
            evolvable=True,
            version=version.strip(),
            status="deployed",
        )
        root.pending_events.append("UnevolvableRulesRejected")
        root.history.append({"event": "DetectionRuleDeployed"})
        return root

    def is_unevolvable(self) -> bool:
        return not self.evolvable or not self.version


@dataclass(eq=False, kw_only=True)
class CsXdrResponseSafeguardsRoot(AggregateRoot):
    tenant_id: str
    response_ref: str
    safeguards: bool
    via_workflow: bool
    via_authz: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls,
        *,
        tenant_id: str,
        response_ref: str,
        safeguards: bool = True,
        via_workflow: bool = True,
        via_authz: bool = True,
    ) -> CsXdrResponseSafeguardsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.resp_tenant_required")
        if not safeguards or not via_workflow or not via_authz:
            raise ValueError(
                "cyber_security.xdr.automated_response_lacks_safeguards"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            response_ref=response_ref.strip(),
            safeguards=True,
            via_workflow=True,
            via_authz=True,
            status="gated",
        )
        root.pending_events.append("ThreatContained")
        root.pending_events.append("UnsafeguardedResponseRejected")
        root.history.append({"event": "ResponseSafeguardsApplied"})
        return root

    def lacks_safeguards(self) -> bool:
        return not self.safeguards or not self.via_workflow or not self.via_authz


@dataclass(eq=False, kw_only=True)
class CsXdrAgentIntegrityRoot(AggregateRoot):
    tenant_id: str
    agent_ref: str
    integrity_verifiable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        agent_ref: str,
        integrity_verifiable: bool = True,
    ) -> CsXdrAgentIntegrityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.agent_tenant_required")
        if not integrity_verifiable:
            raise ValueError(
                "cyber_security.xdr.agent_integrity_cannot_be_verified"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agent_ref=agent_ref.strip(),
            integrity_verifiable=True,
            status="verified",
        )
        root.pending_events.append("UnverifiableAgentRejected")
        root.history.append({"event": "AgentIntegrityVerified"})
        return root

    def is_unverifiable(self) -> bool:
        return not self.integrity_verifiable


@dataclass(eq=False, kw_only=True)
class CsXdrThreatDetectedRoot(AggregateRoot):
    tenant_id: str
    threat_ref: str
    endpoint_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, threat_ref: str, endpoint_ref: str
    ) -> CsXdrThreatDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.xdr.threat_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            threat_ref=threat_ref.strip(),
            endpoint_ref=endpoint_ref.strip(),
            status="detected",
        )
        root.pending_events.append("ThreatDetected")
        root.pending_events.append("EndpointRegistered")
        root.history.append({"event": "ThreatDetected"})
        return root
