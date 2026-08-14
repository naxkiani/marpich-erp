"""Dashboard / platform home — AuthZ + pagination + analytics pulse."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from core.presentation.api.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_list_tenants_requires_auth(client):
    res = await client.get("/api/v1/platform/tenants")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_tenant_requires_auth(client):
    res = await client.get("/api/v1/platform/tenants/demo")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_provision_tenant_is_bootstrap_public(client):
    res = await client.post(
        "/api/v1/platform/tenants",
        json={
            "name": "X Hospital",
            "slug": "x-hospital",
            "industry_pack": "hospital",
        },
    )
    assert res.status_code == 201


@pytest.mark.asyncio
async def test_analytics_home_pulse_requires_auth(client):
    res = await client.get("/api/v1/analytics/home-pulse")
    # Gateway may reject missing tenant (400) before AuthZ (401/403)
    assert res.status_code in (400, 401, 403)
