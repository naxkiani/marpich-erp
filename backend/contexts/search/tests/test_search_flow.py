"""Search — indexing and query tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.search.container import get_search_service, reset_search_service
from contexts.search.infrastructure.persistence.memory_store import SearchMemoryStore
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    SearchMemoryStore.reset()
    InProcessEventBus.reset()
    reset_platform_service()
    reset_search_service()
    get_search_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "search@dev.io", "password": "SecurePass123!", "display_name": "Search User"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "search@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_tenant_provision_seeds_search_indices(client):
    slug = "search-seed"
    response = await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Search Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    assert response.status_code == 201

    headers = await _auth_headers(client, slug)
    indices = await client.get("/api/v1/search/indices", headers=headers)
    assert indices.status_code == 200
    data = indices.json()["data"]
    assert len(data) >= 6


@pytest.mark.asyncio
async def test_user_register_is_indexed_and_searchable(client):
    slug = "search-query"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Search Query Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    results = await client.get("/api/v1/search/query", params={"q": "search@dev.io"}, headers=headers)
    assert results.status_code == 200
    items = results.json()["data"]["items"]
    assert items
    assert any("search@dev.io" in item["title"] for item in items)


@pytest.mark.asyncio
async def test_suggest_returns_prefix_matches(client):
    slug = "search-suggest"
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Suggest Hospital", "slug": slug, "industry_pack": "hospital"},
    )
    headers = await _auth_headers(client, slug)

    suggest = await client.get("/api/v1/search/suggest", params={"q": "Search"}, headers=headers)
    assert suggest.status_code == 200
    assert suggest.json()["data"]["suggestions"]
