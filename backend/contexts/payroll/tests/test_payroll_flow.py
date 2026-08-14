"""Payroll hire ACL → projection → pay run — CAP-ENT-015."""
from __future__ import annotations

from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.human_resources.container import (
    get_human_resources_service,
    reset_human_resources_service,
)
from contexts.human_resources.infrastructure.persistence.memory_store import (
    HumanResourcesMemoryStore,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.payroll.container import get_payroll_service, reset_payroll_service
from contexts.payroll.infrastructure.persistence.memory_store import PayrollMemoryStore
from core.presentation.api.app_factory import create_app
from core.presentation.api.startup_registry import configure_application
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    HumanResourcesMemoryStore.reset()
    PayrollMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_human_resources_service()
    reset_payroll_service()
    # Register payroll ACL subscription before HR hire
    get_payroll_service()
    get_human_resources_service()
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
            "email": "payroll@dev.io",
            "password": "SecurePass123!",
            "display_name": "Payroll Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "payroll@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_hr_hire_projects_employee_then_pay_run(client):
    tenant = "payroll-demo"
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
    hr_id = hired.json()["data"]["id"]

    projected = await client.get("/api/v1/payroll/employees?limit=50", headers=headers)
    assert projected.status_code == 200, projected.text
    body = projected.json()["data"]
    assert body["total"] >= 1
    emp = next(e for e in body["items"] if e["hr_employee_id"] == hr_id)
    assert emp["email"] == "ada@acme.io"

    run = await client.post(
        "/api/v1/payroll/runs",
        json={"period_label": "2026-08"},
        headers=headers,
    )
    assert run.status_code == 201, run.text
    data = run.json()["data"]
    assert data["status"] == "completed"
    assert data["employee_count"] >= 1
    assert Decimal(data["total_gross"]) > 0
    assert Decimal(data["total_net"]) == (
        Decimal(data["total_gross"]) * Decimal("0.9")
    ).quantize(Decimal("0.01"))

    empty = await client.post(
        "/api/v1/payroll/runs",
        json={"period_label": ""},
        headers=headers,
    )
    assert empty.status_code == 422 or empty.status_code == 400
