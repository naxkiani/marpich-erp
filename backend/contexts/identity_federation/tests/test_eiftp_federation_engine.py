"""P200-B5 Federation Engine foundation + CQRS tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.identity_federation.application.commands.connect_federation_provider import (
    ConnectFederationProviderCommand,
    ProbeProviderHealthCommand,
    handle_connect_federation_provider,
    handle_probe_provider_health,
)
from contexts.identity_federation.application.commands.federation_engine_commands import (
    ExchangeFederatedTokenCommand,
    MapIdentityCommand,
    ResolveSyncConflictCommand,
    handle_exchange_federated_token,
    handle_map_identity,
    handle_resolve_sync_conflict,
)
from contexts.identity_federation.application.commands.register_identity_provider import (
    RegisterIdentityProviderCommand,
    handle_register_identity_provider,
)
from contexts.identity_federation.container import (
    get_federation_health_probe,
    get_identity_link_repository,
    get_identity_provider_repository,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.services.eiftp_federation_engine import (
    validate_federation_engine_foundation,
)
from contexts.identity_federation.domain.services.identity_federation_engine import (
    get_identity_federation_engine,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_federation_engine_foundation_passes():
    result = validate_federation_engine_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["foundation_for"] == "P200-B6"
    assert result["federation_connection"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_register_connect_and_health_probe():
    providers = get_identity_provider_repository()
    registered = await handle_register_identity_provider(
        RegisterIdentityProviderCommand(
            tenant_id="tenant-a",
            protocol="oidc",
            name="Corp IdP",
            config={"endpoints": {"discovery": "https://idp.example/.well-known"}},
        ),
        providers=providers,
    )
    assert registered["connections"]
    assert registered["connections"][0]["status"] == "draft"
    ref = registered["provider_ref"]
    connected = await handle_connect_federation_provider(
        ConnectFederationProviderCommand(tenant_id="tenant-a", provider_ref=ref),
        providers=providers,
    )
    assert connected["primary_connection"]["status"] == "connected"
    assert connected["enabled"] is True
    health = await handle_probe_provider_health(
        ProbeProviderHealthCommand(tenant_id="tenant-a", provider_ref=ref),
        providers=providers,
        health=get_federation_health_probe(),
    )
    assert health["probe"]["health_status"] in ("healthy", "degraded", "down")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_exchange_token_and_map_identity():
    exchanged = await handle_exchange_federated_token(
        ExchangeFederatedTokenCommand(
            tenant_id="tenant-a",
            source_type="access_token",
            target_type="id_token",
            subject="user-1",
            audience="api",
        )
    )
    assert exchanged["exchanged"] is True
    mapped = await handle_map_identity(
        MapIdentityCommand(
            tenant_id="tenant-a",
            user_id="user-1",
            provider_id="idp-1",
            external_subject="ext-1",
            raw_claims={"email": "a@b.c", "sub": "ext-1"},
            mappings=[
                {
                    "source_claim": "email",
                    "target_claim": "mail",
                    "transform_type": "direct",
                    "enabled": True,
                }
            ],
        ),
        links=get_identity_link_repository(),
    )
    assert mapped["mapped_claims"].get("mail") == "a@b.c"
    assert mapped["link"]["link_status"] == "active"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_resolve_sync_conflict():
    result = await handle_resolve_sync_conflict(
        ResolveSyncConflictCommand(
            tenant_id="tenant-a",
            primary={"id": "a", "verified": True, "email": "a@b.c"},
            secondary={"id": "b", "verified": False, "email": "a@b.c"},
            strategy="prefer_verified",
        )
    )
    assert result["resolution"]["resolved"]["id"] == "a"


@pytest.mark.unit
def test_engine_facade_composes_protocols():
    catalog = get_identity_federation_engine().protocol_catalog()
    assert "oidc" in catalog["protocols"]
    assert "adapters" in catalog


@pytest.mark.unit
def test_no_eiftp_sibling():
    assert not (REPO_ROOT / "backend/contexts/eiftp").exists()
