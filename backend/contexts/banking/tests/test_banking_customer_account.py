"""Banking Customer and Account Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    reset_banking_customer_account_service,
)
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    reset_banking_customer_account_service()
    get_financial_kernel_service()
    get_banking_customer_account_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "bank@lokal.dev", "password": "SecurePass123!", "display_name": "Bank Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "bank@lokal.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_banking_customer_account_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


async def _onboard_customer(client: AsyncClient, headers: dict) -> dict:
    customer = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "individual",
            "display_name": "Jane Doe",
            "legal_name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+15551234567",
            "auto_submit": True,
        },
    )
    assert customer.status_code == 201
    cid = customer.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)

    kyc = await client.post(
        f"/api/v1/banking/customers/{cid}/kyc",
        headers=headers,
        json={"tier": "tier1", "document_type": "passport", "document_ref": "P123456"},
    )
    assert kyc.status_code == 201
    kyc_id = kyc.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/kyc/{kyc_id}/verify",
        headers=headers,
        json={"verified_by": "compliance_officer"},
    )
    return customer.json()["data"]


@pytest.mark.asyncio
async def test_banking_catalog(client):
    slug = "bankcat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "individual" in caps
    assert "business" in caps
    assert "government" in caps
    assert "ngo" in caps
    assert "joint" in caps
    assert "savings" in caps
    assert "current" in caps
    assert "fixed_deposit" in caps
    assert "loan" in caps
    assert "virtual" in caps
    assert "multi_currency" in caps
    assert "kernel_integration" in caps


@pytest.mark.asyncio
async def test_provision_products(client):
    slug = "bankprod"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    resp = await client.get("/api/v1/banking/products", headers=headers)
    assert resp.status_code == 200
    codes = {p["product_code"] for p in resp.json()["data"]}
    assert "SAV-STD" in codes
    assert "CUR-STD" in codes
    assert "LOAN-PER" in codes


@pytest.mark.asyncio
async def test_customer_lifecycle(client):
    slug = "bankcust"
    headers = await _auth_headers(client, slug)
    customer = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "business",
            "display_name": "Acme Corp",
            "legal_name": "Acme Corporation Ltd",
            "email": "ops@acme.com",
            "phone": "+15559876543",
            "risk_rating": "medium",
            "auto_submit": True,
        },
    )
    assert customer.status_code == 201
    assert customer.json()["data"]["approval_status"] == "pending"

    cid = customer.json()["data"]["id"]
    approved = await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["data"]["approval_status"] == "approved"


@pytest.mark.asyncio
async def test_open_and_approve_account_kernel_linked(client):
    slug = "bankacct"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer = await _onboard_customer(client, headers)

    account = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={
            "customer_id": customer["id"],
            "product_code": "SAV-STD",
            "opening_balance": 15000.0,
        },
    )
    assert account.status_code == 201
    assert account.json()["data"]["status"] == "pending_approval"
    assert account.json()["data"]["kernel_linked"] is False

    account_id = account.json()["data"]["id"]
    approved = await client.post(f"/api/v1/banking/accounts/{account_id}/approve", headers=headers)
    assert approved.status_code == 200
    data = approved.json()["data"]
    assert data["status"] == "active"
    assert data["kernel_linked"] is True
    assert data["gl_account_code"] is not None
    assert data["kernel_subledger_ref"].startswith("banking:")


@pytest.mark.asyncio
async def test_account_status_workflow(client):
    slug = "bankwf"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer = await _onboard_customer(client, headers)

    account = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={"customer_id": customer["id"], "product_code": "CUR-STD"},
    )
    account_id = account.json()["data"]["id"]
    await client.post(f"/api/v1/banking/accounts/{account_id}/approve", headers=headers)

    blocked = await client.post(
        f"/api/v1/banking/accounts/{account_id}/status",
        headers=headers,
        json={"status": "blocked", "reason": "compliance_hold"},
    )
    assert blocked.status_code == 200
    assert blocked.json()["data"]["status"] == "blocked"

    reactivated = await client.post(
        f"/api/v1/banking/accounts/{account_id}/status",
        headers=headers,
        json={"status": "active"},
    )
    assert reactivated.status_code == 200
    assert reactivated.json()["data"]["status"] == "active"


@pytest.mark.asyncio
async def test_minimum_balance_and_overdraft(client):
    slug = "bankrules"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    customer = await _onboard_customer(client, headers)

    account = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={"customer_id": customer["id"], "product_code": "CUR-STD", "opening_balance": 600.0},
    )
    account_id = account.json()["data"]["id"]
    await client.post(f"/api/v1/banking/accounts/{account_id}/approve", headers=headers)

    min_bal = await client.get(
        f"/api/v1/banking/accounts/{account_id}/minimum-balance", headers=headers
    )
    assert min_bal.status_code == 200
    assert min_bal.json()["data"]["compliant"] is True

    od = await client.post(
        f"/api/v1/banking/accounts/{account_id}/overdraft-check",
        headers=headers,
        json={"amount": 1200.0},
    )
    assert od.status_code == 200
    assert od.json()["data"]["allowed"] is True


@pytest.mark.asyncio
async def test_dashboard(client):
    slug = "bankdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    await _onboard_customer(client, headers)

    resp = await client.get("/api/v1/banking/dashboard", headers=headers)
    assert resp.status_code == 200
    summary = resp.json()["data"]["summary"]
    assert summary["customer_count"] >= 1
    assert "by_customer_type" in resp.json()["data"]
    assert "account_status_workflow" in resp.json()["data"]


@pytest.mark.asyncio
async def test_government_customer_types(client):
    slug = "bankgov"
    headers = await _auth_headers(client, slug)
    for ctype in ("government", "ngo"):
        resp = await client.post(
            "/api/v1/banking/customers",
            headers=headers,
            json={
                "customer_type": ctype,
                "display_name": f"Test {ctype}",
                "legal_name": f"Test {ctype} Entity",
                "email": f"{ctype}@gov.test",
                "phone": "+15550001111",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["data"]["customer_type"] == ctype
