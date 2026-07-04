"""Settings — tenant provision seeds config via events."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_settings_service()
    reset_notification_service()
    get_settings_service()
    get_notification_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@settings.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@settings.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_seeds_settings(client):
    slug = "settings-hospital"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Settings Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    headers = await _auth_headers(client, slug)

    config = await client.get("/api/v1/settings/config", headers=headers)
    assert config.status_code == 200
    data = config.json()["data"]
    assert data["locale"] == "en-US"
    assert "healthcare.patient-management" in str(data.get("enabled_modules", [])) or "platform.identity" in data.get("enabled_modules", [])

    features = await client.get("/api/v1/settings/features", headers=headers)
    assert features.status_code == 200
    assert features.json()["data"]["advanced_analytics"] is True
    assert features.json()["data"]["saved_listings"] is False


@pytest.mark.asyncio
async def test_update_config_and_toggle_feature(client):
    slug = "settings-config"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Config Co", "slug": slug, "industry_pack": "school"},
    )
    headers = await _auth_headers(client, slug)

    updated = await client.put(
        "/api/v1/settings/config/timezone",
        json={"value": "Asia/Tehran"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["timezone"] == "Asia/Tehran"

    toggled = await client.put(
        "/api/v1/settings/features/saved_listings",
        json={"enabled": True},
        headers=headers,
    )
    assert toggled.status_code == 200
    assert toggled.json()["data"]["saved_listings"] is True


@pytest.mark.asyncio
async def test_module_activation_merges_config(client):
    slug = "settings-module"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Module Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)

    activate = await client.post(
        f"/api/v1/platform/tenants/{slug}/modules",
        json={"module_id": "healthcare.pharmacy"},
        headers=headers,
    )
    assert activate.status_code == 200

    config = await client.get("/api/v1/settings/config", headers=headers)
    module_cfg = config.json()["data"].get("module.healthcare.pharmacy")
    assert module_cfg is not None
    assert module_cfg.get("enabled") is True


@pytest.mark.asyncio
async def test_public_branding_endpoint(client):
    slug = "settings-brand"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Brand Co", "slug": slug, "industry_pack": "retail"},
    )

    branding = await client.get(f"/api/v1/settings/branding", headers={"X-Tenant-ID": slug})
    assert branding.status_code == 200
    assert branding.json()["data"]["primary_color"] == "#2563eb"
