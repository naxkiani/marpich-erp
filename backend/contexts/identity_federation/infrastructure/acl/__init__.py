"""Anti-Corruption Layer package — translate peer/vendor payloads to local commands.

Existing runtime ACL adapters live in infrastructure/adapters/*_acl.py and are
the production implementations. This package defines the strategic ACL contract.
"""
from __future__ import annotations

from typing import Any, Protocol


class IAntiCorruptionLayer(Protocol):
    """Translate external/peer model → local command/DTO (never persist peer aggregates)."""

    def translate_inbound(self, payload: dict[str, Any]) -> dict[str, Any]: ...


class IdentityEventAcl:
    """Maps identity.* integration payloads to federation-local unlink/terminate intents."""

    def translate_inbound(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "command": "federation.sync_principal_state",
            "tenant_id": payload.get("tenant_id"),
            "subject_id": payload.get("user_id") or payload.get("subject_id"),
            "state": payload.get("state") or payload.get("status") or "unknown",
            "source_event": payload.get("event_name"),
        }


class IntegrationConnectorAcl:
    """Strips vendor-specific fields from connector callbacks before domain entry."""

    VENDOR_KEYS = ("okta_", "entra_", "auth0_", "keycloak_raw")

    def translate_inbound(self, payload: dict[str, Any]) -> dict[str, Any]:
        clean = {
            k: v
            for k, v in payload.items()
            if not any(k.startswith(p) or k == p for p in self.VENDOR_KEYS)
        }
        return {
            "command": "federation.external_assertion_accepted",
            "protocol": clean.get("protocol"),
            "external_subject": clean.get("sub") or clean.get("external_subject"),
            "claims": clean.get("claims") or {},
            "provider_ref": clean.get("provider_ref"),
        }
