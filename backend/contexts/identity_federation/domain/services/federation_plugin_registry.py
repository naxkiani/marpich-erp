"""Federation plugin registry — pluggable identity providers."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProviderPluginType(StrEnum):
    OIDC = "oidc"
    SAML = "saml"
    LDAP = "ldap"
    SCIM = "scim"
    CUSTOM = "custom"


@dataclass
class ProviderPluginDescriptor:
    plugin_id: str
    name: str
    protocol: str
    version: str = "1.0.0"
    vendor: str = "builtin"
    enabled: bool = True
    config_schema: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "protocol": self.protocol,
            "version": self.version,
            "vendor": self.vendor,
            "enabled": self.enabled,
        }


BUILTIN_PROVIDER_PLUGINS: list[ProviderPluginDescriptor] = [
    ProviderPluginDescriptor("builtin.oidc", "OpenID Connect", "oidc"),
    ProviderPluginDescriptor("builtin.saml", "SAML 2.0", "saml"),
    ProviderPluginDescriptor("builtin.ldap", "LDAP / Active Directory", "ldap"),
    ProviderPluginDescriptor("builtin.azure_ad", "Microsoft Entra ID", "entra_id", vendor="microsoft"),
    ProviderPluginDescriptor("builtin.google", "Google Workspace", "google", vendor="google"),
    ProviderPluginDescriptor("builtin.apple", "Sign in with Apple", "apple", vendor="apple"),
    ProviderPluginDescriptor("builtin.github", "GitHub", "github", vendor="github"),
    ProviderPluginDescriptor("builtin.gitlab", "GitLab", "gitlab", vendor="gitlab"),
    ProviderPluginDescriptor("builtin.keycloak", "Keycloak", "keycloak", vendor="redhat"),
    ProviderPluginDescriptor("builtin.okta", "Okta", "okta", vendor="okta"),
    ProviderPluginDescriptor("builtin.auth0", "Auth0", "auth0", vendor="auth0"),
    ProviderPluginDescriptor("builtin.cognito", "Amazon Cognito", "cognito", vendor="aws"),
    ProviderPluginDescriptor("builtin.government_eid", "Government eID", "government_eid"),
    ProviderPluginDescriptor("builtin.university", "University IdP", "university"),
    ProviderPluginDescriptor("builtin.hospital", "Hospital IdP", "hospital"),
    ProviderPluginDescriptor("builtin.bank", "Bank Identity", "bank"),
    ProviderPluginDescriptor("builtin.tax_authority", "Tax Authority IdP", "tax_authority"),
    ProviderPluginDescriptor("builtin.national_digital_id", "National Digital Identity", "national_digital_id"),
    ProviderPluginDescriptor("builtin.custom", "Custom Provider", "custom"),
    ProviderPluginDescriptor("builtin.legacy", "Legacy Identity System", "legacy"),
    ProviderPluginDescriptor("builtin.partner", "Partner Organization", "partner"),
]


def list_provider_plugins() -> list[dict]:
    return [p.to_dict() for p in BUILTIN_PROVIDER_PLUGINS if p.enabled]


def resolve_plugin(protocol: str) -> ProviderPluginDescriptor | None:
    for plugin in BUILTIN_PROVIDER_PLUGINS:
        if plugin.protocol == protocol and plugin.enabled:
            return plugin
    return next((p for p in BUILTIN_PROVIDER_PLUGINS if p.plugin_id == "builtin.custom"), None)
