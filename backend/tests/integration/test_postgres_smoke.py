"""PostgreSQL integration smoke test — skipped unless PERSISTENCE_BACKEND=postgres."""
import os

import pytest
from httpx import ASGITransport, AsyncClient

from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


pytestmark = pytest.mark.skipif(
    os.getenv("PERSISTENCE_BACKEND", "memory") != "postgres",
    reason="Set PERSISTENCE_BACKEND=postgres and run migrations",
)


@pytest.fixture(autouse=True)
def reset_memory_fallback():
    import contexts.identity.container as c

    c._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    yield
    c._container = None


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_postgres_register_persists(client):
    tenant = "pg-smoke-tenant"
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "pg@smoke.dev", "password": "SecurePass123!", "display_name": "PG User"},
        headers={"X-Tenant-ID": tenant},
    )
    assert response.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pg@smoke.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200
