"""P198-B federation gateway API integration tests."""
import pytest

from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_federation_gateway_oauth_flow(integration_client):
    tenant = "federation-gateway"
    headers = {"X-Tenant-ID": tenant}

    reg = await integration_client.post(
        "/api/v1/federation/clients/register",
        headers=headers,
        json={
            "client_name": "Gateway Test",
            "redirect_uris": ["https://app.test/callback"],
            "grant_types": ["authorization_code", "client_credentials"],
            "require_pkce": False,
        },
    )
    assert reg.status_code == 200
    client = reg.json()["data"]

    login = await integration_client.post(
        "/api/v1/federation/login",
        headers=headers,
        json={
            "client_id": client["client_id"],
            "redirect_uri": "https://app.test/callback",
            "scope": "openid profile",
            "state": "state-1",
            "user_id": "user-gateway",
        },
    )
    assert login.status_code == 200
    auth_code = login.json()["data"]["authorization_code"]

    token = await integration_client.post(
        "/api/v1/federation/token",
        headers=headers,
        json={
            "grant_type": "authorization_code",
            "client_id": client["client_id"],
            "code": auth_code,
            "redirect_uri": "https://app.test/callback",
        },
    )
    assert token.status_code == 200
    assert "access_token" in token.json()

    discovery = await integration_client.get(
        "/api/v1/federation/.well-known/openid-configuration",
        headers=headers,
    )
    assert discovery.status_code == 200
    assert "token_endpoint" in discovery.json()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_identity_gateway_metadata(integration_client):
    tenant = "federation-metadata"
    headers = await auth_headers(integration_client, tenant=tenant, email="meta@enterprise.dev")
    await integration_client.post("/api/v1/federation/seed", headers=headers)

    providers = await integration_client.get("/api/v1/identity/providers", headers={"X-Tenant-ID": tenant})
    assert providers.status_code == 200

    metadata = await integration_client.get("/api/v1/identity/metadata", headers={"X-Tenant-ID": tenant})
    assert metadata.status_code == 200
    body = metadata.json()["data"]
    assert body["tenant_id"] == tenant
    assert "protocol_catalog" in body
