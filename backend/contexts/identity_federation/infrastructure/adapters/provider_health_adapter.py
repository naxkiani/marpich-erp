"""Provider health probe adapter — uses protocol negotiation, not vendor SDKs."""
from __future__ import annotations

from typing import Any

from contexts.identity_federation.domain.services import protocol_engine
from contexts.identity_federation.infrastructure.observability import federation_protocol_metrics


class ProtocolHealthProbeAdapter:
    async def probe(
        self,
        *,
        tenant_id: str,
        provider_ref: str,
        protocol: str,
        endpoints: dict[str, Any] | None = None,
    ) -> dict:
        _ = tenant_id
        negotiation = protocol_engine.negotiate_protocol(requested=protocol)
        ok = negotiation.get("negotiated_protocol") is not None
        # Endpoints present improve confidence; empty still reports negotiated capability
        has_endpoint = bool(endpoints)
        health = "healthy" if ok and (has_endpoint or protocol in ("oidc", "oauth2", "saml", "scim", "ldap")) else "degraded"
        if not ok:
            health = "down"
            federation_protocol_metrics.increment("provider_health_down")
        else:
            federation_protocol_metrics.increment("provider_health_up")
        return {
            "provider_ref": provider_ref,
            "protocol": protocol,
            "health_status": health,
            "negotiated": negotiation,
            "endpoints_present": has_endpoint,
            "engine": "protocol_health_probe",
        }
