"""Tax payroll ACL → liability → file return — CAP-ENT-026."""
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
from contexts.tax.container import get_tax_service, reset_tax_service
from contexts.tax.infrastructure.persistence.memory_store import TaxMemoryStore
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
    TaxMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_human_resources_service()
    reset_payroll_service()
    reset_tax_service()
    get_tax_service()
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
            "email": "tax@dev.io",
            "password": "SecurePass123!",
            "display_name": "Tax Admin",
        },
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "tax@dev.io", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    assert login.status_code == 200, login.text
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_payroll_run_creates_liability_then_file_return(client):
    tenant = "tax-demo"
    headers = await _auth_headers(client, tenant)

    hired = await client.post(
        "/api/v1/human-resources/employees",
        json={
            "email": "ada@acme.io",
            "full_name": "Ada Lovelace",
            "job_title": "Engineer",
            "department": "R&D",
        },
        headers=headers,
    )
    assert hired.status_code == 201, hired.text

    run = await client.post(
        "/api/v1/payroll/runs",
        json={"period_label": "2026-08"},
        headers=headers,
    )
    assert run.status_code == 201, run.text
    run_id = run.json()["data"]["id"]
    gross = Decimal(run.json()["data"]["total_gross"])

    liabilities = await client.get("/api/v1/tax/liabilities?limit=50", headers=headers)
    assert liabilities.status_code == 200, liabilities.text
    body = liabilities.json()["data"]
    assert body["total"] >= 1
    liab = next(i for i in body["items"] if i["payroll_run_id"] == run_id)
    assert liab["status"] == "open"
    assert Decimal(liab["tax_amount"]) == (gross * Decimal("0.10")).quantize(Decimal("0.01"))

    filed = await client.post(
        "/api/v1/tax/returns/file",
        json={"period_label": "2026-08"},
        headers=headers,
    )
    assert filed.status_code == 201, filed.text
    ret = filed.json()["data"]
    assert ret["status"] == "filed"
    assert ret["liability_count"] >= 1
    assert Decimal(ret["total_tax"]) == Decimal(liab["tax_amount"])

    again = await client.post(
        "/api/v1/tax/returns/file",
        json={"period_label": "2026-08"},
        headers=headers,
    )
    assert again.status_code == 400
