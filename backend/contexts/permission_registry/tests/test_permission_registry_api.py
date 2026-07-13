"""Permission Registry — integration smoke tests."""
import pytest

from contexts.permission_registry.domain.aggregates.permission_registry_platform import RegistryCapability
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="perm-smoke",
        email="perm-smoke@enterprise.dev",
        display_name="Permission Registry Smoke",
    )
    resp = await integration_client.get("/api/v1/permissions/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert RegistryCapability.MODULE_REGISTRATION.value in caps
    assert len(caps) == 10


@pytest.mark.integration
@pytest.mark.asyncio
async def test_seed_register_role_and_bind(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="perm-flow",
        email="perm-flow@enterprise.dev",
        display_name="Permission Flow",
    )
    seed = await integration_client.post("/api/v1/permissions/seed", headers=headers)
    assert seed.status_code == 200
    assert seed.json()["data"]["seeded"] is True

    register = await integration_client.post(
        "/api/v1/permissions/register",
        headers=headers,
        json={
            "module": "construction",
            "permissions": [
                {"code": "construction.projects.read", "description": "Read construction projects"},
                {"code": "construction.projects.write", "description": "Manage construction projects"},
            ],
        },
    )
    assert register.status_code == 200
    assert register.json()["data"]["count"] == 2

    role = await integration_client.post(
        "/api/v1/permissions/roles",
        headers=headers,
        json={
            "code": "site_manager",
            "name": "Site Manager",
            "permission_codes": ["construction.projects.read", "construction.projects.write"],
        },
    )
    assert role.status_code == 200
    role_ref = role.json()["data"]["role_ref"]

    me = await integration_client.get("/api/v1/users/me", headers=headers)
    principal_id = me.json()["data"]["id"]

    bind = await integration_client.post(
        f"/api/v1/permissions/roles/{role_ref}/bindings",
        headers=headers,
        json={"principal_id": principal_id},
    )
    assert bind.status_code == 200

    resolved = await integration_client.get(
        f"/api/v1/permissions/principals/{principal_id}/permissions",
        headers=headers,
    )
    assert resolved.status_code == 200
    perms = resolved.json()["data"]["permissions"]
    assert "construction.projects.read" in perms

    authz = await integration_client.post(
        "/api/v1/authorization/check",
        headers=headers,
        json={
            "permission_code": "construction.projects.read",
            "context": {},
        },
    )
    assert authz.status_code == 200
    assert authz.json()["data"]["decision"] == "allow"

    dashboard = await integration_client.get("/api/v1/permissions/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["summary"]["roles"] >= 3
