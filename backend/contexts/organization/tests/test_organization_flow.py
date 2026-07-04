"""Organization — tenant bootstrap, units, memberships."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.core_platform.container import reset_platform_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.notifications.container import get_notification_service, reset_notification_service
from contexts.notifications.infrastructure.persistence.memory_store import NotificationMemoryStore
from contexts.organization.container import get_organization_service, reset_organization_service
from contexts.organization.infrastructure.persistence.memory_store import OrganizationMemoryStore
from contexts.settings.container import get_settings_service, reset_settings_service
from contexts.settings.infrastructure.persistence.memory_store import SettingsMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    OrganizationMemoryStore.reset()
    SettingsMemoryStore.reset()
    NotificationMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_organization_service()
    reset_settings_service()
    reset_notification_service()
    get_organization_service()
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
        json={"email": "admin@org.dev", "password": "SecurePass123!", "display_name": "Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@org.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_creates_root_organization(client):
    slug = "org-hospital"
    provision = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Org Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert provision.status_code == 201

    headers = await _auth_headers(client, slug)

    org = await client.get("/api/v1/organizations", headers=headers)
    assert org.status_code == 200
    data = org.json()["data"]
    assert data["name"] == "Org Hospital"
    assert data["root_unit_id"] is not None


@pytest.mark.asyncio
async def test_org_tree_and_create_unit(client):
    slug = "org-tree"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Tree Co", "slug": slug, "industry_pack": "clinic"},
    )
    headers = await _auth_headers(client, slug)

    org = await client.get("/api/v1/organizations", headers=headers)
    root_id = org.json()["data"]["root_unit_id"]

    created = await client.post(
        "/api/v1/organizations/units",
        json={
            "parent_id": root_id,
            "unit_type": "department",
            "code": "ICU",
            "name": "Intensive Care",
        },
        headers=headers,
    )
    assert created.status_code == 201
    assert created.json()["data"]["code"] == "ICU"

    tree = await client.get("/api/v1/organizations/tree", headers=headers)
    assert tree.status_code == 200
    tree_data = tree.json()["data"]
    assert len(tree_data["tree"]) == 1
    assert len(tree_data["tree"][0]["children"]) == 1
    assert tree_data["tree"][0]["children"][0]["code"] == "ICU"


@pytest.mark.asyncio
async def test_user_created_auto_assigned_to_root(client):
    slug = "org-member"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Member Co", "slug": slug, "industry_pack": "school"},
    )
    headers = await _auth_headers(client, slug)

    my_units = await client.get("/api/v1/organizations/users/me/units", headers=headers)
    assert my_units.status_code == 200
    units = my_units.json()["data"]
    assert len(units) == 1
    assert units[0]["is_primary"] is True
    assert units[0]["unit"]["code"] == "ROOT"


@pytest.mark.asyncio
async def test_add_and_remove_member(client):
    slug = "org-members"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Members Co", "slug": slug, "industry_pack": "retail"},
    )
    headers = await _auth_headers(client, slug)

    org = await client.get("/api/v1/organizations", headers=headers)
    root_id = org.json()["data"]["root_unit_id"]

    added = await client.post(
        f"/api/v1/organizations/units/{root_id}/members",
        json={"user_id": "user-42", "title": "Staff", "is_primary": False},
        headers=headers,
    )
    assert added.status_code == 201

    listed = await client.get("/api/v1/organizations/users/user-42/units", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()["data"]) == 1

    removed = await client.delete(
        f"/api/v1/organizations/units/{root_id}/members/user-42",
        headers=headers,
    )
    assert removed.status_code == 200

    listed_after = await client.get("/api/v1/organizations/users/user-42/units", headers=headers)
    assert listed_after.json()["data"] == []
