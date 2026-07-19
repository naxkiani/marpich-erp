"""Identity Provider Management facade (P200-B7)."""
from __future__ import annotations

from contexts.identity_federation.domain.services import (
    provider_mapping_engine,
    trust_fabric_engine,
)
from contexts.identity_federation.domain.services.identity_federation_engine import (
    get_identity_federation_engine,
)
from contexts.identity_federation.domain.value_objects.provider_types import (
    ProviderType,
    can_transition_status,
    normalize_provider_type,
    provider_trust_label,
)
from contexts.identity_federation.domain.value_objects.trust_levels import level_from_score
from contexts.identity_federation.infrastructure.plugins import protocol_plugin_sdk


class IdentityProviderPlatform:
    """Universal IdP + protocol layer — facts only, no Permit/Deny."""

    def negotiate_protocol(self, *, requested: str) -> dict:
        return get_identity_federation_engine().negotiate_protocol(requested=requested)

    def normalize_type(self, provider_type: str | None) -> str:
        return normalize_provider_type(provider_type)

    def resolve_plugin_for_protocol(self, protocol: str) -> dict | None:
        plugins = protocol_plugin_sdk.list_protocol_plugins(protocol=protocol)
        return plugins[0] if plugins else None

    def evaluate_provider_trust(
        self,
        *,
        inputs: dict | None = None,
        prior_score: int | None = None,
        zero_trust_ctx: dict | None = None,
    ) -> dict:
        evaluation = trust_fabric_engine.get_trust_fabric_engine().evaluate_continuous(
            inputs=inputs or {},
            prior_score=prior_score,
            zero_trust_ctx=zero_trust_ctx or {},
        )
        level = int(evaluation.get("enterprise_level") or level_from_score(evaluation["trust_score"]))
        return {
            **evaluation,
            "provider_trust_level": level,
            "provider_trust_label": provider_trust_label(level),
            "permit_deny": None,
        }

    def activation_gate(
        self,
        *,
        lifecycle_status: str,
        has_endpoints: bool,
        has_plugin: bool,
        trust_level: int,
        min_trust_level: int = 1,
    ) -> dict:
        reasons: list[str] = []
        if lifecycle_status not in ("verified", "suspended", "active"):
            reasons.append("lifecycle_not_verified")
        if not has_endpoints:
            reasons.append("missing_endpoints")
        if not has_plugin:
            reasons.append("missing_protocol_plugin")
        if trust_level < min_trust_level:
            reasons.append("trust_below_minimum")
        return {
            "allowed": not reasons,
            "reasons": reasons,
            "min_trust_level": min_trust_level,
        }

    def status_transition(self, *, from_status: str, to_status: str) -> dict:
        return can_transition_status(from_status=from_status, to_status=to_status)

    def map_identity(self, *, source_claims: dict, rules: list[dict]) -> dict:
        return provider_mapping_engine.apply_mapping_pipeline(
            source_claims=source_claims, rules=rules
        )

    def plugin_catalog(self) -> list[dict]:
        return protocol_plugin_sdk.list_protocol_plugins(include_disabled=True)

    def provider_types(self) -> list[str]:
        return [t.value for t in ProviderType]

    def surface(self) -> dict:
        return {
            "prompt": "P200-B7",
            "adr": 221,
            "provider_types": self.provider_types(),
            "plugins": self.plugin_catalog(),
            "mapping": provider_mapping_engine.catalog(),
            "principles": [
                "no_hardcoded_providers",
                "protocol_independence",
                "plugin_first",
                "trust_fabric_facts",
                "tenant_isolation",
                "zero_trust_validation",
            ],
        }


_platform: IdentityProviderPlatform | None = None


def get_identity_provider_platform() -> IdentityProviderPlatform:
    global _platform
    if _platform is None:
        _platform = IdentityProviderPlatform()
    return _platform
