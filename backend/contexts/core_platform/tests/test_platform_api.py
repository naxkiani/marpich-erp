"""Core Platform API tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application


@pytest.fixture(autouse=True)
def reset_stores():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    reset_platform_service()
    yield
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    reset_platform_service()


@pytest.fixture
async def client():
    application = create_app(profile="full", startup_mode="lazy")
    configure_application(application, profile="full", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@platform.com", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@platform.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_list_industry_packs(client):
    response = await client.get("/api/v1/platform/industry-packs")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) >= 26
    pack_ids = {p["pack_id"] for p in data}
    assert "hospital" in pack_ids
    assert "university" in pack_ids


@pytest.mark.asyncio
async def test_provision_hospital_tenant(client):
    response = await client.post(
        "/api/v1/platform/tenants",
        json={
            "name": "Acme Hospital",
            "slug": "acme-hospital",
            "industry_pack": "hospital",
            "optional_modules": ["healthcare.pharmacy"],
        },
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["slug"] == "acme-hospital"
    assert data["status"] == "active"
    assert data["industry_pack"] == "hospital"
    assert "healthcare.pharmacy" in data["enabled_modules"]
    assert "platform.identity" in data["enabled_modules"]

    get_resp = await client.get("/api/v1/platform/tenants/acme-hospital")
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["name"] == "Acme Hospital"


@pytest.mark.asyncio
async def test_provision_rejects_duplicate_slug(client):
    payload = {
        "name": "First",
        "slug": "dup-tenant",
        "industry_pack": "school",
    }
    assert (await client.post("/api/v1/platform/tenants", json=payload)).status_code == 201
    dup = await client.post("/api/v1/platform/tenants", json={**payload, "name": "Second"})
    assert dup.status_code == 400
    assert dup.json()["detail"] == "platform.errors.slug_exists"


@pytest.mark.asyncio
async def test_activate_optional_module(client):
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Beta Clinic", "slug": "beta-clinic", "industry_pack": "clinic"},
    )

    headers = await _auth_headers(client, "beta-clinic")

    activate = await client.post(
        "/api/v1/platform/tenants/beta-clinic/modules",
        json={"module_id": "healthcare.pharmacy"},
        headers=headers,
    )
    assert activate.status_code == 200
    modules = activate.json()["data"]["enabled_modules"]
    assert "healthcare.pharmacy" in modules


@pytest.mark.asyncio
async def test_full_bootstrap_provision_then_register(client):
    """Provision tenant → register admin → use hospital APIs."""
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "City Hospital", "slug": "city-hospital", "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    register = await client.post(
        "/api/v1/auth/register",
        json={"email": "ceo@city.com", "password": "SecurePass123!", "display_name": "CEO"},
        headers={"X-Tenant-ID": "city-hospital"},
    )
    assert register.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "ceo@city.com", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": "city-hospital"},
    )
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]

    patient = await client.post(
        "/api/v1/hospital/patients",
        json={
            "mrn": "MRN-100",
            "first_name": "Test",
            "last_name": "Patient",
            "date_of_birth": "2000-01-01",
        },
        headers={"X-Tenant-ID": "city-hospital", "Authorization": f"Bearer {token}"},
    )
    assert patient.status_code == 201
