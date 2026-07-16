"""Identity Federation API integration tests."""
import pytest

from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_federation_catalog_seed_dashboard(integration_client):
    tenant = "federation-p198"
    headers = await auth_headers(integration_client, tenant=tenant, email="fed@enterprise.dev")

    catalog = await integration_client.get("/api/v1/federation/catalog", headers=headers)
    assert catalog.status_code == 200
    data = catalog.json()["data"]
    assert "identity_federation" in data["capabilities"]
    assert len(data["provider_plugins"]) >= 15

    await integration_client.post("/api/v1/federation/seed", headers=headers)
    dashboard = await integration_client.get("/api/v1/federation/dashboard", headers=headers)
    assert dashboard.status_code == 200


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_provider_and_broker(integration_client):
    tenant = "federation-broker"
    headers = await auth_headers(integration_client, tenant=tenant, email="broker@enterprise.dev")
    await integration_client.post("/api/v1/federation/seed", headers=headers)

    reg = await integration_client.post(
        "/api/v1/federation/providers",
        headers=headers,
        json={
            "protocol": "oidc",
            "name": "Enterprise OIDC",
            "config": {"domains": ["enterprise.dev"], "issuer_url": "https://idp.example.com"},
        },
    )
    assert reg.status_code == 200
    provider_ref = reg.json()["data"]["provider_ref"]

    await integration_client.post(
        "/api/v1/federation/claims/mappings",
        headers=headers,
        json={
            "provider_ref": provider_ref,
            "source_claim": "email",
            "target_claim": "email",
        },
    )

    broker = await integration_client.post(
        "/api/v1/federation/broker/authenticate",
        headers=headers,
        json={
            "email": "user@enterprise.dev",
            "raw_claims": {"sub": "ext-001", "email": "user@enterprise.dev", "name": "Fed User"},
        },
    )
    assert broker.status_code == 200
    body = broker.json()["data"]
    assert body["brokered"] is True
    assert "session_ref" in body


@pytest.mark.integration
@pytest.mark.asyncio
async def test_identity_discovery(integration_client):
    tenant = "federation-discover"
    headers = await auth_headers(integration_client, tenant=tenant, email="discover@enterprise.dev")
    await integration_client.post("/api/v1/federation/seed", headers=headers)
    await integration_client.post(
        "/api/v1/federation/providers",
        headers=headers,
        json={"protocol": "saml", "name": "Hospital SAML", "config": {"domains": ["hospital.org"]}},
    )
    result = await integration_client.post(
        "/api/v1/federation/discover",
        headers=headers,
        json={"email": "doctor@hospital.org"},
    )
    assert result.status_code == 200
    assert result.json()["data"]["recommended_provider"] is not None
