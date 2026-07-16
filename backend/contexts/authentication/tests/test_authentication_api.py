"""Authentication platform — integration smoke tests."""
import pytest

from contexts.authentication.domain.aggregates.authentication_platform import AuthenticationCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="authn-smoke",
        email="authn-smoke@enterprise.dev",
        display_name="Authentication Smoke",
    )
    resp = await integration_client.get("/api/v1/authentication/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert AuthenticationCapability.WEBAUTHN_AUTHENTICATION.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_register_oidc_and_authorize(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="authn-oidc",
        email="authn-oidc@enterprise.dev",
        display_name="Authentication OIDC",
    )
    seed = await integration_client.post("/api/v1/authentication/seed", headers=headers)
    assert seed.status_code == 200
    assert seed.json()["data"]["seeded"] is True

    register = await integration_client.post(
        "/api/v1/authentication/federation/providers",
        headers=headers,
        json={
            "name": "Enterprise IdP",
            "issuer_url": "https://idp.enterprise.dev",
            "client_id": "marpich-admin",
            "client_secret": "secret",
            "redirect_uri": "http://localhost:3001/login/oidc",
            "scopes": "openid profile email",
        },
    )
    assert register.status_code == 200
    provider_ref = register.json()["data"]["provider_ref"]

    providers = await integration_client.get("/api/v1/authentication/federation/providers", headers=headers)
    assert providers.status_code == 200
    assert len(providers.json()["data"]) == 1

    authorize = await integration_client.post(
        "/api/v1/authentication/federation/oidc/authorize",
        headers={"X-Tenant-ID": "authn-oidc", "Content-Type": "application/json"},
        json={"provider_ref": provider_ref},
    )
    assert authorize.status_code == 200
    data = authorize.json()["data"]
    assert data["authorization_url"].startswith("https://idp.enterprise.dev/authorize?")
    assert data["state"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_passkey_login_requires_registered_passkey(integration_client):
    tenant = "authn-passkey"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="passkey@enterprise.dev",
        display_name="Passkey User",
    )
    await integration_client.post("/api/v1/authentication/seed", headers=headers)

    options = await integration_client.post(
        "/api/v1/authentication/webauthn/login/options",
        headers={"X-Tenant-ID": tenant, "Content-Type": "application/json"},
        json={"email": "passkey@enterprise.dev"},
    )
    assert options.status_code == 400
    assert "no_passkeys" in options.json()["detail"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_webauthn_registration_options(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="authn-reg",
        email="authn-reg@enterprise.dev",
        display_name="Registration User",
    )
    await integration_client.post("/api/v1/authentication/seed", headers=headers)

    options = await integration_client.post(
        "/api/v1/authentication/webauthn/register/options",
        headers=headers,
    )
    assert options.status_code == 200
    data = options.json()["data"]
    assert data["challenge_id"]
    assert data["options"]["challenge"]
    assert data["options"]["rp"]["id"]
