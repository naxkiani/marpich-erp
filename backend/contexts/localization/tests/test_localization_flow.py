"""Localization flow tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.localization.container import get_localization_service, reset_localization_service
from contexts.localization.infrastructure.persistence.memory_store import LocalizationMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    LocalizationMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_localization_service()
    get_localization_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "l10n@dev.io", "password": "SecurePass123!", "display_name": "L10n Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "l10n@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_seeds_locales(client):
    slug = "l10n-seed"
    response = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "L10n Corp", "slug": slug, "industry_pack": "hospital"},
    )
    assert response.status_code == 201

    headers = await _auth_headers(client, slug)
    locales = await client.get("/api/v1/localization/locales", headers=headers)
    assert locales.status_code == 200
    codes = {item["code"] for item in locales.json()["data"]}
    assert "en" in codes
    assert "fa" in codes


@pytest.mark.asyncio
async def test_define_key_and_upsert_translation(client):
    slug = "l10n-translate"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Translate Corp", "slug": slug, "industry_pack": "retail"},
    )
    headers = await _auth_headers(client, slug)

    defined = await client.post(
        "/api/v1/localization/keys",
        json={
            "namespace": "common",
            "key": "welcome",
            "default_value": "Welcome",
            "description": "Homepage greeting",
        },
        headers=headers,
    )
    assert defined.status_code == 201

    upsert = await client.put(
        "/api/v1/localization/bundles/fa/common/welcome",
        json={"value": "خوش آمدید"},
        headers=headers,
    )
    assert upsert.status_code == 200
    assert upsert.json()["data"]["entries"]["welcome"] == "خوش آمدید"

    bundle = await client.get("/api/v1/localization/bundles/fa/common", headers=headers)
    assert bundle.status_code == 200
    assert bundle.json()["data"]["entries"]["welcome"] == "خوش آمدید"
