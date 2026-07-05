"""Treasury → General Ledger auto-posting bridge tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.treasury.container import get_treasury_service, reset_treasury_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    reset_treasury_service()
    get_financial_kernel_service()
    get_treasury_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bridge@treasury.dev", "password": "SecurePass123!", "display_name": "Bridge"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "bridge@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_transfer_executed_auto_posts_gl_journal(client):
    slug = "glbridge"
    headers = await _auth_headers(client, slug)

    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned({"tenant_id": slug, "payload": {"industry_pack": "hospital"}})
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})

    accounts = await client.get("/api/v1/treasury/accounts", headers=headers)
    accts = {a["code"]: a for a in accounts.json()["data"]}
    from_id = accts["MAIN-CASH"]["id"]
    to_id = accts["OPERATING-BANK"]["id"]

    transfer = await client.post(
        "/api/v1/treasury/transfers",
        headers=headers,
        json={
            "from_account_id": from_id,
            "to_account_id": to_id,
            "amount": 1000,
            "currency": "USD",
            "instrument": "electronic_transfer",
            "reference": "GL-BRIDGE-1",
            "require_approval": False,
        },
    )
    assert transfer.status_code == 201
    transfer_id = transfer.json()["data"]["id"]

    journals = await client.get("/api/v1/financial-kernel/ledger/journals", headers=headers)
    assert journals.status_code == 200
    posted = [
        j for j in journals.json()["data"]
        if j.get("source_context") == "treasury" and j.get("source_document_id") == transfer_id
    ]
    assert len(posted) == 1
    journal = posted[0]
    assert journal["status"] == "posted"
    total_debit = sum(l["debit"] for l in journal["lines"])
    assert total_debit == 1000


@pytest.mark.asyncio
async def test_platform_catalog_lists_twelve_capabilities(client):
    slug = "tplat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/platform/catalog", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["data"]) == 12
    assert body["meta"]["pos_boundary"]["never_merge"] is True
    assert "treasury_transfer" in body["meta"]["gl_rule_map"].values()
