"""Directory platform — integration smoke tests."""
import pytest

from contexts.directory.application.service import DirectoryApplicationService
from contexts.directory.domain.aggregates.directory_platform import DirectoryCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="dir-smoke",
        email="dir-smoke@enterprise.dev",
        display_name="Directory Smoke",
    )
    resp = await integration_client.get("/api/v1/directory/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert DirectoryCapability.LDAP_DIRECTORY_SYNC.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_saml_register_authorize_and_acs(integration_client):
    tenant = "dir-saml"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="dir-saml-admin@enterprise.dev",
        display_name="Directory SAML Admin",
    )
    await integration_client.post("/api/v1/directory/seed", headers=headers)

    register = await integration_client.post(
        "/api/v1/directory/federation/saml/providers",
        headers=headers,
        json={
            "name": "Enterprise SAML IdP",
            "entity_id": "https://idp.enterprise.dev/metadata",
            "sso_url": "https://idp.enterprise.dev/sso",
            "x509_cert": "MIIB...",
        },
    )
    assert register.status_code == 200
    provider_ref = register.json()["data"]["provider_ref"]

    authorize = await integration_client.post(
        "/api/v1/directory/federation/saml/authorize",
        headers={"X-Tenant-ID": tenant, "Content-Type": "application/json"},
        json={"provider_ref": provider_ref},
    )
    assert authorize.status_code == 200
    data = authorize.json()["data"]
    assert data["authorization_url"].startswith("https://idp.enterprise.dev/sso?")
    assert data["relay_state"]

    saml_response = DirectoryApplicationService.build_test_saml_response("saml-user@enterprise.dev")
    acs = await integration_client.post(
        "/api/v1/directory/federation/saml/acs",
        headers={"X-Tenant-ID": tenant, "Content-Type": "application/json"},
        json={"SAMLResponse": saml_response, "RelayState": data["relay_state"]},
    )
    assert acs.status_code == 200
    tokens = acs.json()["data"]
    assert tokens["access_token"]
    assert tokens["auth_method"] == "saml"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ldap_register_sync_and_worker(integration_client):
    tenant = "dir-ldap"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="dir-ldap-admin@enterprise.dev",
        display_name="Directory LDAP Admin",
    )
    await integration_client.post("/api/v1/directory/seed", headers=headers)

    register = await integration_client.post(
        "/api/v1/directory/ldap/connectors",
        headers=headers,
        json={
            "name": "Corporate AD",
            "host": "ad.enterprise.mock",
            "port": 389,
            "bind_dn": "cn=sync,dc=enterprise,dc=dev",
            "bind_password": "secret",
            "base_dn": "ou=users,dc=enterprise,dc=dev",
        },
    )
    assert register.status_code == 200
    connector_ref = register.json()["data"]["connector_ref"]

    sync = await integration_client.post(
        "/api/v1/directory/ldap/sync",
        headers=headers,
        json={"connector_ref": connector_ref},
    )
    assert sync.status_code == 200
    assert sync.json()["data"]["created"] >= 1

    enqueue = await integration_client.post(
        "/api/v1/directory/sync/enqueue",
        headers=headers,
        json={"connector_ref": connector_ref},
    )
    assert enqueue.status_code == 200
    assert enqueue.json()["data"]["status"] == "pending"

    run = await integration_client.post("/api/v1/directory/sync/run", headers=headers)
    assert run.status_code == 200
    assert run.json()["data"]["processed"] >= 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_scim_register_and_provision_user(integration_client):
    tenant = "dir-scim"
    headers = await auth_headers(
        integration_client,
        tenant=tenant,
        email="dir-scim-admin@enterprise.dev",
        display_name="Directory SCIM Admin",
    )
    await integration_client.post("/api/v1/directory/seed", headers=headers)

    register = await integration_client.post(
        "/api/v1/directory/scim/providers",
        headers=headers,
        json={"name": "Okta SCIM"},
    )
    assert register.status_code == 200
    bearer_token = register.json()["data"]["bearer_token"]

    scim_headers = {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    create = await integration_client.post(
        "/api/v1/directory/scim/v2/Users",
        headers=scim_headers,
        json={
            "userName": "scim-user@enterprise.dev",
            "displayName": "SCIM User",
            "externalId": "okta-12345",
            "emails": [{"value": "scim-user@enterprise.dev", "primary": True}],
        },
    )
    assert create.status_code == 200
    body = create.json()
    assert body["userName"] == "scim-user@enterprise.dev"
    assert body["id"]

    dashboard = await integration_client.get("/api/v1/directory/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["scim_providers"] == 1
