"""EIFTP Identity Provider Management (P200-B7) foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/221-enterprise-identity-federation-identity-providers.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_IDENTITY_PROVIDERS.md",
    "docs/architecture/identity/eiftp/IDENTITY_PROVIDERS_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/IDENTITY_PROVIDERS_PROTOCOLS.v1.yaml",
    "docs/architecture/identity/eiftp/IDENTITY_PROVIDERS_SURFACE.v1.yaml",
    "backend/contexts/identity_federation/domain/value_objects/provider_types.py",
    "backend/contexts/identity_federation/domain/services/identity_provider_platform.py",
    "backend/contexts/identity_federation/domain/services/provider_mapping_engine.py",
    "backend/contexts/identity_federation/infrastructure/plugins/protocol_plugin_sdk.py",
    "backend/contexts/identity_federation/application/commands/provider_management_commands.py",
    "backend/contexts/identity_federation/application/queries/provider_management_queries.py",
    "backend/contexts/identity_federation/presentation/providers_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_identity_providers_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    from contexts.identity_federation.domain.aggregates.federation_platform import IdentityProvider
    from contexts.identity_federation.domain.services.identity_provider_platform import (
        IdentityProviderPlatform,
    )
    from contexts.identity_federation.domain.value_objects.provider_types import ProviderType
    from contexts.identity_federation.infrastructure.plugins import protocol_plugin_sdk

    lifecycle_ok = all(
        hasattr(IdentityProvider, m)
        for m in ("configure", "verify", "activate", "suspend_provider", "apply_trust")
    )
    platform_ok = all(
        hasattr(IdentityProviderPlatform, m)
        for m in ("evaluate_provider_trust", "activation_gate", "resolve_plugin_for_protocol")
    )
    plugins_ok = len(protocol_plugin_sdk.list_protocol_plugins()) >= 5
    types_ok = len(ProviderType) >= 8
    install_ok = hasattr(protocol_plugin_sdk, "install_protocol_plugin")
    no_hardcode_vendor = "okta" not in str(ProviderType.__members__).lower()
    passed = (
        not missing
        and not sibling
        and lifecycle_ok
        and platform_ok
        and plugins_ok
        and types_ok
        and install_ok
        and no_hardcode_vendor
    )
    return {
        "prompt": "P200-B7",
        "adr": 221,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "lifecycle_methods": lifecycle_ok,
        "platform_facade": platform_ok,
        "protocol_plugins": plugins_ok,
        "provider_types": types_ok,
        "plugin_install": install_ok,
        "no_hardcoded_vendor_types": no_hardcode_vendor,
        "foundation_for": "P200-B8",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
