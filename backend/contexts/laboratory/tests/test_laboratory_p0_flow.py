"""P0 — Laboratory CAP-HLT-007 order→sample→result stub."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.core_platform.container import reset_platform_service
from contexts.core_platform.infrastructure.persistence.memory_store import PlatformMemoryStore
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.laboratory.container import reset_laboratory_service
from contexts.laboratory.infrastructure.persistence.memory_store import LaboratoryMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PlatformMemoryStore.reset()
    LaboratoryMemoryStore.reset()
    EventFabric.reset_dev_state()
    reset_platform_service()
    reset_laboratory_service()
    yield


@pytest.fixture
async def client():
    application = create_app(profile="industry", startup_mode="lazy")
    configure_application(application, profile="industry", startup_mode="lazy")
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _admin(client: AsyncClient, tenant: str, email: str) -> dict[str, str]:
    await client.post(
        "/api/v1/platform/tenants",
        json={"name": "Lab Co", "slug": tenant, "industry_pack": "laboratory"},
    )
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": "Lab Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    return {
        "X-Tenant-ID": tenant,
        "Authorization": f"Bearer {login.json()['data']['access_token']}",
    }


@pytest.mark.asyncio
async def test_laboratory_order_sample_result(client):
    headers = await _admin(client, "lab-p0", "lab@demo.dev")

    order = await client.post(
        "/api/v1/laboratory/orders",
        json={
            "order_number": "LAB-2001",
            "patient_ref": "clinic-patient-uuid",
            "test_code": "CBC",
        },
        headers=headers,
    )
    assert order.status_code == 201, order.text
    order_id = order.json()["data"]["id"]

    early = await client.post(
        f"/api/v1/laboratory/orders/{order_id}/results",
        json={"result_value": "5.0", "result_unit": "10^9/L"},
        headers=headers,
    )
    assert early.status_code == 400

    sample = await client.post(
        "/api/v1/laboratory/samples",
        json={
            "order_id": order_id,
            "accession_number": "ACC-9",
            "specimen_type": "whole_blood",
        },
        headers=headers,
    )
    assert sample.status_code == 201, sample.text

    result = await client.post(
        f"/api/v1/laboratory/orders/{order_id}/results",
        json={"result_value": "5.2", "result_unit": "10^9/L"},
        headers=headers,
    )
    assert result.status_code == 200, result.text
    assert result.json()["data"]["status"] == "finalized"

    listed = await client.get("/api/v1/laboratory/orders", headers=headers)
    assert listed.json()["data"]["total"] == 1
