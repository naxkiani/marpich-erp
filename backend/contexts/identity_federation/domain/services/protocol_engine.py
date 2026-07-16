"""Federation protocol engine — abstraction, negotiation, pluggable adapters."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol


class FederationProtocol(StrEnum):
    OAUTH2 = "oauth2"
    OIDC = "oidc"
    SAML = "saml"
    SCIM = "scim"
    LDAP = "ldap"
    LDAPS = "ldaps"
    AD = "ad"
    KERBEROS = "kerberos"
    CAS = "cas"
    WS_FEDERATION = "ws_federation"
    JWT = "jwt"


SUPPORTED_PROTOCOLS = [p.value for p in FederationProtocol]


@dataclass
class ProtocolCapabilities:
    protocol: str
    grants: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"protocol": self.protocol, "grants": self.grants, "features": self.features}


PROTOCOL_CAPABILITIES: dict[str, ProtocolCapabilities] = {
    "oauth2": ProtocolCapabilities(
        "oauth2",
        grants=["authorization_code", "client_credentials", "refresh_token", "device_code", "token_exchange"],
        features=["pkce", "par", "jar", "rar", "dpop", "revocation", "introspection", "dynamic_client_registration"],
    ),
    "oidc": ProtocolCapabilities(
        "oidc",
        grants=["authorization_code", "implicit_disabled", "hybrid_disabled"],
        features=["discovery", "userinfo", "jwks", "end_session", "backchannel_logout", "frontchannel_logout"],
    ),
    "saml": ProtocolCapabilities(
        "saml",
        grants=["sso", "slo"],
        features=["idp", "sp", "metadata", "assertion_signing", "encryption", "attribute_statements"],
    ),
    "scim": ProtocolCapabilities(
        "scim",
        grants=[],
        features=["users", "groups", "patch", "bulk", "filter", "incremental_sync"],
    ),
    "ldap": ProtocolCapabilities(
        "ldap",
        grants=[],
        features=["bind", "search", "sync", "group_mapping", "ou_mapping"],
    ),
}


class IProtocolAdapter(Protocol):
    protocol: str

    async def negotiate(self, *, tenant_id: str, context: dict) -> dict: ...
    async def authenticate(self, *, tenant_id: str, request: dict) -> dict: ...
    async def translate(self, *, raw: dict, mappings: list[dict]) -> dict: ...


@dataclass
class ProtocolAdapterDescriptor:
    adapter_id: str
    protocol: str
    name: str
    version: str = "1.0.0"
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "adapter_id": self.adapter_id,
            "protocol": self.protocol,
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
        }


_BUILTIN_ADAPTERS = [
    ProtocolAdapterDescriptor("adapter.oauth2", "oauth2", "OAuth 2.1 Authorization Server"),
    ProtocolAdapterDescriptor("adapter.oidc", "oidc", "OpenID Connect Provider"),
    ProtocolAdapterDescriptor("adapter.saml", "saml", "SAML 2.0 Platform"),
    ProtocolAdapterDescriptor("adapter.scim", "scim", "SCIM 2.0 Provisioning"),
    ProtocolAdapterDescriptor("adapter.ldap", "ldap", "LDAP / Active Directory"),
    ProtocolAdapterDescriptor("adapter.jwt", "jwt", "JWT Token Handler"),
]


def list_protocol_adapters() -> list[dict]:
    return [a.to_dict() for a in _BUILTIN_ADAPTERS if a.enabled]


def negotiate_protocol(
    *,
    requested: str | None,
    supported: list[str] | None = None,
    client_capabilities: list[str] | None = None,
) -> dict:
    """Select best protocol based on client and server capabilities."""
    available = supported or SUPPORTED_PROTOCOLS
    if requested and requested in available:
        caps = PROTOCOL_CAPABILITIES.get(requested)
        return {
            "negotiated_protocol": requested,
            "capabilities": caps.to_dict() if caps else {},
            "method": "explicit",
        }
    if client_capabilities:
        for proto in ("oidc", "oauth2", "saml", "ldap"):
            if proto in client_capabilities and proto in available:
                caps = PROTOCOL_CAPABILITIES.get(proto)
                return {
                    "negotiated_protocol": proto,
                    "capabilities": caps.to_dict() if caps else {},
                    "method": "client_capability",
                }
    return {"negotiated_protocol": "oidc", "capabilities": PROTOCOL_CAPABILITIES["oidc"].to_dict(), "method": "default"}


def build_protocol_catalog() -> dict:
    return {
        "protocols": SUPPORTED_PROTOCOLS,
        "capabilities": {k: v.to_dict() for k, v in PROTOCOL_CAPABILITIES.items()},
        "adapters": list_protocol_adapters(),
        "token_formats": ["jwt", "opaque"],
        "signing_algorithms": ["RS256", "ES256", "HS256"],
        "encryption": ["JWE", "X509", "mTLS"],
    }
