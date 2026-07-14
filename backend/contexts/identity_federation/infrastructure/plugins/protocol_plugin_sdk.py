"""Protocol plugin SDK — hot-pluggable federation adapters."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class IProtocolPlugin(Protocol):
    plugin_id: str
    protocol: str
    version: str

    async def negotiate(self, *, tenant_id: str, context: dict[str, Any]) -> dict: ...
    async def authenticate(self, *, tenant_id: str, request: dict[str, Any]) -> dict: ...
    async def translate(self, *, raw: dict[str, Any], mappings: list[dict]) -> dict: ...


@dataclass
class ProtocolPluginDescriptor:
    plugin_id: str
    protocol: str
    name: str
    version: str = "1.0.0"
    enabled: bool = True
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "protocol": self.protocol,
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "capabilities": self.capabilities,
        }


_REGISTRY: dict[str, ProtocolPluginDescriptor] = {}


def register_protocol_plugin(descriptor: ProtocolPluginDescriptor) -> None:
    _REGISTRY[descriptor.plugin_id] = descriptor


def list_protocol_plugins(*, protocol: str | None = None) -> list[dict]:
    items = [d.to_dict() for d in _REGISTRY.values() if d.enabled]
    if protocol:
        items = [i for i in items if i["protocol"] == protocol]
    return items


def resolve_protocol_plugin(plugin_id: str) -> ProtocolPluginDescriptor | None:
    return _REGISTRY.get(plugin_id)


def bootstrap_builtin_protocol_plugins() -> None:
    builtins = [
        ProtocolPluginDescriptor("plugin.oauth2", "oauth2", "OAuth 2.1 AS", capabilities=["pkce", "dcr"]),
        ProtocolPluginDescriptor("plugin.oidc", "oidc", "OpenID Connect Provider", capabilities=["discovery", "userinfo"]),
        ProtocolPluginDescriptor("plugin.saml", "saml", "SAML 2.0 Platform", capabilities=["idp", "sp", "slo"]),
        ProtocolPluginDescriptor("plugin.scim", "scim", "SCIM 2.0", capabilities=["users", "groups", "bulk"]),
        ProtocolPluginDescriptor("plugin.ldap", "ldap", "LDAP Connector", capabilities=["sync", "bind"]),
        ProtocolPluginDescriptor("plugin.ad", "ad", "Active Directory", capabilities=["sync", "group_mapping"]),
        ProtocolPluginDescriptor("plugin.jwt", "jwt", "JWT Handler", capabilities=["jws", "jwe", "jwks"]),
    ]
    for item in builtins:
        register_protocol_plugin(item)


bootstrap_builtin_protocol_plugins()
