"""HR employee hire/list/terminate — CAP-ENT-010."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.human_resources.container import reset_human_resources_service
from contexts.human_resources.infrastructure.persistence.memory_store import (
    HumanResourcesMemoryStore,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HumanResourcesMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_human_resources_service()
    yield


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
        json={
            "email": "hr@dev.io",
            "password": "SecurePass123!",
            "display_name": "HR Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "hr@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hire_list_terminate_employee(client):
    tenant = "hr-demo"
    headers = await _auth_headers(client, tenant)

    hired = await client.post(
        "/api/v1/human-resources/employees",
        json={
            "email": "ada@acme.io",
            "full_name": "Ada Lovelace",
            "job_title": "Engineer",
            "department": "R&D",
            "employee_number": "E-1001",
        },
        headers=headers,
    )
    assert hired.status_code == 201, hired.text
    body = hired.json()["data"]
    assert body["status"] == "active"
    assert body["email"] == "ada@acme.io"
    employee_id = body["id"]

    listed = await client.get("/api/v1/human-resources/employees?limit=50", headers=headers)
    assert listed.status_code == 200, listed.text
    assert listed.json()["data"]["total"] >= 1
    assert any(e["id"] == employee_id for e in listed.json()["data"]["items"])

    dup = await client.post(
        "/api/v1/human-resources/employees",
        json={"email": "ada@acme.io", "full_name": "Ada Dup"},
        headers=headers,
    )
    assert dup.status_code == 400

    terminated = await client.post(
        f"/api/v1/human-resources/employees/{employee_id}/terminate",
        json={"reason": "Contract ended"},
        headers=headers,
    )
    assert terminated.status_code == 200, terminated.text
    assert terminated.json()["data"]["status"] == "terminated"
    assert terminated.json()["data"]["terminated_at"] is not None

    again = await client.post(
        f"/api/v1/human-resources/employees/{employee_id}/terminate",
        json={"reason": "again"},
        headers=headers,
    )
    assert again.status_code == 400
