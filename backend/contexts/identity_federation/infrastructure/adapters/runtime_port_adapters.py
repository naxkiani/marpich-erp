"""Infrastructure adapters implementing federation runtime ports."""
from __future__ import annotations

from typing import Any

from contexts.identity_federation.infrastructure.adapters.adaptive_auth_acl import AdaptiveAuthAcl
from contexts.identity_federation.infrastructure.adapters.identity_risk_acl import IdentityRiskAcl
from contexts.identity_federation.infrastructure.observability import federation_ai_metrics
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics
from contexts.identity_federation.infrastructure.observability import federation_trust_metrics
from contexts.identity_federation.infrastructure.persistence.federation_audit_store import (
    FederationAuditStore,
)


class ProtocolMetricsAdapter:
    def increment(self, metric: str, value: float = 1.0) -> None:
        federation_protocol_metrics.increment(metric, value)

    def record_latency(self, metric: str, ms: float) -> None:
        federation_protocol_metrics.record_latency(metric, ms)

    def snapshot(self) -> dict:
        return federation_protocol_metrics.snapshot()


class TrustMetricsAdapter:
    def increment(self, metric: str, value: float = 1.0) -> None:
        federation_trust_metrics.increment(metric, value)

    def record_latency(self, metric: str, ms: float) -> None:
        if hasattr(federation_trust_metrics, "record_latency"):
            federation_trust_metrics.record_latency(metric, ms)

    def snapshot(self) -> dict:
        return federation_trust_metrics.snapshot()


class AiMetricsAdapter:
    def increment(self, metric: str, value: float = 1.0) -> None:
        federation_ai_metrics.increment(metric, value)

    def record_latency(self, metric: str, ms: float) -> None:
        if hasattr(federation_ai_metrics, "record_latency"):
            federation_ai_metrics.record_latency(metric, ms)

    def snapshot(self) -> dict:
        return federation_ai_metrics.snapshot()


class FederationAuditTrailAdapter:
    def append(self, **kwargs: Any) -> dict:
        return FederationAuditStore.append(**kwargs)

    def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[dict]:
        return FederationAuditStore.list_by_tenant(tenant_id, limit=limit)


class AdaptiveAuthFederationAdapter(AdaptiveAuthAcl):
    """Port-facing adaptive auth ACL (peer calls stay in infrastructure)."""


class IdentityRiskFederationAdapter(IdentityRiskAcl):
    """Port-facing identity risk ACL (peer calls stay in infrastructure)."""
