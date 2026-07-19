"""P200-B7 Identity Provider Management + Protocol Layer tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.provider_management_commands import (
    ActivateIdentityProviderCommand,
    ConfigureProviderCommand,
    CreateMappingRuleCommand,
    InstallProtocolPluginCommand,
    RegisterManagedProviderCommand,
    RotateProviderCertificateCommand,
    SuspendIdentityProviderCommand,
    SynchronizeIdentityCommand,
    ValidateProviderTrustCommand,
    VerifyProviderCommand,
    handle_activate_identity_provider,
    handle_configure_provider,
    handle_create_mapping_rule,
    handle_install_protocol_plugin,
    handle_register_managed_provider,
    handle_rotate_provider_certificate,
    handle_suspend_identity_provider,
    handle_synchronize_identity,
    handle_validate_provider_trust,
    handle_verify_provider,
)
from contexts.identity_federation.application.queries.provider_management_queries import (
    handle_get_provider_surface,
)
from contexts.identity_federation.container import (
    get_identity_provider_repository,
    get_sync_job_repository,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.services.eiftp_identity_providers import (
    validate_identity_providers_foundation,
)
from contexts.identity_federation.domain.value_objects.provider_types import ProviderType

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_identity_providers_foundation_passes():
    result = validate_identity_providers_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B8"
    assert result["plugin_install"] is True
    assert result["no_hardcoded_vendor_types"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register_configure_verify_trust_activate_sync_lifecycle():
    providers = get_identity_provider_repository()
    registered = await handle_register_managed_provider(
        RegisterManagedProviderCommand(
            tenant_id="tenant-a",
            protocol="oidc",
            name="Partner IdP",
            provider_type="partner",
            config={"endpoints": {"discovery": "https://idp.example/.well-known"}},
        ),
        providers=providers,
    )
    assert registered["lifecycle_status"] == "registered"
    assert registered["enabled"] is False
    assert registered["provider_type"] == ProviderType.PARTNER.value
    assert registered["plugin_id"]
    ref = registered["provider_ref"]

    configured = await handle_configure_provider(
        ConfigureProviderCommand(
            tenant_id="tenant-a",
            provider_ref=ref,
            config={"endpoints": {"token": "https://idp.example/token"}},
            security_profile={"mtls": True},
        ),
        providers=providers,
    )
    assert configured["security_profile"]["mtls"] is True

    verified = await handle_verify_provider(
        VerifyProviderCommand(tenant_id="tenant-a", provider_ref=ref),
        providers=providers,
    )
    assert verified["lifecycle_status"] == "verified"

    trusted = await handle_validate_provider_trust(
        ValidateProviderTrustCommand(
            tenant_id="tenant-a",
            provider_ref=ref,
            inputs={
                "identity_assurance": 85,
                "authentication_strength": 80,
                "risk_signals": 15,
                "compliance_status": 80,
                "device_security": 75,
            },
        ),
        providers=providers,
    )
    assert trusted["permit_deny"] is None
    assert trusted["evaluation"]["provider_trust_level"] >= 1

    activated = await handle_activate_identity_provider(
        ActivateIdentityProviderCommand(tenant_id="tenant-a", provider_ref=ref),
        providers=providers,
    )
    assert activated["lifecycle_status"] == "active"
    assert activated["enabled"] is True

    synced = await handle_synchronize_identity(
        SynchronizeIdentityCommand(tenant_id="tenant-a", provider_ref=ref, mode="batch"),
        providers=providers,
        sync_jobs=get_sync_job_repository(),
    )
    assert synced["status"] == "queued"

    suspended = await handle_suspend_identity_provider(
        SuspendIdentityProviderCommand(tenant_id="tenant-a", provider_ref=ref, reason="incident"),
        providers=providers,
    )
    assert suspended["lifecycle_status"] == "suspended"
    assert suspended["enabled"] is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_plugin_install_and_mapping_and_cert_rotation():
    installed = await handle_install_protocol_plugin(
        InstallProtocolPluginCommand(
            plugin_id="plugin.future_fedcm",
            protocol="fedcm",
            name="FedCM Preview",
            version="0.1.0",
            capabilities=["passive"],
        )
    )
    assert installed["plugin_id"] == "plugin.future_fedcm"
    assert installed["sandboxed"] is True

    mapped = await handle_create_mapping_rule(
        CreateMappingRuleCommand(
            tenant_id="tenant-a",
            source_claims={"sub": "u1", "email": "a@example.com"},
            rules=[
                {"source_claim": "sub", "target_claim": "user_id", "transform_type": "direct"},
                {"source_claim": "email", "target_claim": "email", "transform_type": "direct"},
            ],
        )
    )
    assert mapped["valid"] is True
    assert mapped["mapped_claims"]["user_id"] == "u1"

    providers = get_identity_provider_repository()
    registered = await handle_register_managed_provider(
        RegisterManagedProviderCommand(
            tenant_id="tenant-a",
            protocol="saml",
            name="Gov IdP",
            provider_type="government",
            config={"endpoints": {"metadata": "https://gov.example/meta"}},
        ),
        providers=providers,
    )
    rotated = await handle_rotate_provider_certificate(
        RotateProviderCertificateCommand(
            tenant_id="tenant-a",
            provider_ref=registered["provider_ref"],
        ),
        providers=providers,
    )
    assert rotated["rotation"]["rotated"] is True


@pytest.mark.unit
def test_surface_and_no_sibling_bc():
    surface = handle_get_provider_surface()
    assert surface["adr"] == 221
    assert surface["validation"]["passed"] is True
    assert "oidc" in {p["protocol"] for p in surface["plugins"]}
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
