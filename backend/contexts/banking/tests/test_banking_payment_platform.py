"""Banking Payment Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_customer_account_service,
    get_banking_payment_platform_service,
    reset_banking_customer_account_service,
)
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.policy.infrastructure.persistence.memory_store import PolicyMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    PolicyMemoryStore.reset()
    reset_financial_kernel_service()
    reset_banking_customer_account_service()
    reset_policy_service()
    get_financial_kernel_service()
    get_banking_customer_account_service()
    get_banking_payment_platform_service()
    get_policy_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "pay@bank.dev", "password": "SecurePass123!", "display_name": "Payment Ops"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pay@bank.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    kernel = get_financial_kernel_service()
    await kernel.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_policy_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "bank"}}
    )
    await get_banking_customer_account_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )
    await get_banking_payment_platform_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


async def _open_funded_accounts(client: AsyncClient, headers: dict) -> tuple[str, str, str]:
    customer = await client.post(
        "/api/v1/banking/customers",
        headers=headers,
        json={
            "customer_type": "individual",
            "display_name": "Payer",
            "legal_name": "Payer",
            "email": "payer@test",
            "phone": "+15551237777",
            "auto_submit": True,
        },
    )
    assert customer.status_code == 201
    cid = customer.json()["data"]["id"]
    await client.post(f"/api/v1/banking/customers/{cid}/approve", headers=headers)

    kyc = await client.post(
        f"/api/v1/banking/customers/{cid}/kyc",
        headers=headers,
        json={"tier": "tier1", "document_type": "passport", "document_ref": "P555444"},
    )
    kyc_id = kyc.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/kyc/{kyc_id}/verify",
        headers=headers,
        json={"verified_by": "compliance"},
    )

    source = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={"customer_id": cid, "product_code": "SAV-STD", "opening_balance": 50000.0},
    )
    assert source.status_code == 201
    source_id = source.json()["data"]["id"]
    await client.post(f"/api/v1/banking/accounts/{source_id}/approve", headers=headers)

    dest = await client.post(
        "/api/v1/banking/accounts",
        headers=headers,
        json={"customer_id": cid, "product_code": "SAV-STD", "opening_balance": 1000.0},
    )
    assert dest.status_code == 201
    dest_id = dest.json()["data"]["id"]
    await client.post(f"/api/v1/banking/accounts/{dest_id}/approve", headers=headers)

    return cid, source_id, dest_id


@pytest.mark.asyncio
async def test_payment_catalog(client):
    slug = "paycat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/payments/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "internal" in caps
    assert "inter_branch" in caps
    assert "bank_to_bank" in caps
    assert "bulk" in caps
    assert "scheduled_transfer" in caps
    assert "standing_orders" in caps
    assert "bill_payment" in caps
    assert "government_payment" in caps
    assert "salary_transfer" in caps
    assert "merchant_payment" in caps
    assert "qr_payment" in caps
    assert "real_time" in caps
    assert "transfer_limits" in caps
    assert "approval_workflow" in caps
    assert "fraud_checks" in caps
    assert "automatic_gl_posting" in caps


@pytest.mark.asyncio
async def test_internal_transfer_lifecycle(client):
    slug = "payint"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    _, source_id, dest_id = await _open_funded_accounts(client, headers)

    created = await client.post(
        "/api/v1/banking/payments/transfers",
        headers=headers,
        json={
            "transfer_type": "internal",
            "source_account_id": source_id,
            "destination_account_id": dest_id,
            "amount": 2500.0,
            "narrative": "savings move",
        },
    )
    assert created.status_code == 201
    transfer_id = created.json()["data"]["id"]

    executed = await client.post(
        f"/api/v1/banking/payments/transfers/{transfer_id}/execute",
        headers=headers,
        json={"approver_id": "teller"},
    )
    assert executed.status_code == 200
    assert executed.json()["data"]["status"] == "completed"

    detail = await client.get(f"/api/v1/banking/payments/transfers/{transfer_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["fraud_check"] is not None

    audit = await client.get(f"/api/v1/banking/payments/transfers/{transfer_id}/audit", headers=headers)
    assert audit.status_code == 200
    actions = {e["action"] for e in audit.json()["data"]}
    assert "transfer.created" in actions
    assert "transfer.executed" in actions


@pytest.mark.asyncio
async def test_real_time_transfer(client):
    slug = "payrt"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    _, source_id, dest_id = await _open_funded_accounts(client, headers)

    created = await client.post(
        "/api/v1/banking/payments/transfers",
        headers=headers,
        json={
            "transfer_type": "real_time",
            "source_account_id": source_id,
            "destination_account_id": dest_id,
            "amount": 500.0,
        },
    )
    transfer_id = created.json()["data"]["id"]
    executed = await client.post(
        f"/api/v1/banking/payments/transfers/{transfer_id}/execute",
        headers=headers,
        json={},
    )
    assert executed.status_code == 200
    assert executed.json()["data"]["channel"] == "real_time"


@pytest.mark.asyncio
async def test_bulk_salary_transfer(client):
    slug = "paybulk"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    _, source_id, dest_id = await _open_funded_accounts(client, headers)

    bulk = await client.post(
        "/api/v1/banking/payments/bulk",
        headers=headers,
        json={
            "source_account_id": source_id,
            "transfer_type": "salary_transfer",
            "items": [
                {"amount": 1500.0, "destination_account_id": dest_id, "salary_ref": "EMP-001"},
                {"amount": 2000.0, "destination_account_id": dest_id, "salary_ref": "EMP-002"},
            ],
        },
    )
    assert bulk.status_code == 201
    data = bulk.json()["data"]
    assert data["batch"]["item_count"] == 2
    assert len(data["transfers"]) == 2


@pytest.mark.asyncio
async def test_standing_order_and_beneficiary(client):
    slug = "paysto"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    cid, source_id, dest_id = await _open_funded_accounts(client, headers)

    ben = await client.post(
        "/api/v1/banking/payments/beneficiaries",
        headers=headers,
        json={
            "customer_id": cid,
            "name": "External Payee",
            "account_number": "9988776655",
            "bank_code": "BANK01",
        },
    )
    assert ben.status_code == 201

    order = await client.post(
        "/api/v1/banking/payments/standing-orders",
        headers=headers,
        json={
            "source_account_id": source_id,
            "transfer_type": "internal",
            "amount": 200.0,
            "frequency": "monthly",
            "destination_account_id": dest_id,
        },
    )
    assert order.status_code == 201
    assert order.json()["data"]["frequency"] == "monthly"


@pytest.mark.asyncio
async def test_payment_dashboard(client):
    slug = "paydash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)
    _, source_id, dest_id = await _open_funded_accounts(client, headers)

    created = await client.post(
        "/api/v1/banking/payments/transfers",
        headers=headers,
        json={
            "transfer_type": "bill_payment",
            "source_account_id": source_id,
            "destination_account_id": dest_id,
            "amount": 100.0,
            "bill_ref": "UTIL-123",
        },
    )
    transfer_id = created.json()["data"]["id"]
    await client.post(
        f"/api/v1/banking/payments/transfers/{transfer_id}/execute",
        headers=headers,
        json={},
    )

    dash = await client.get("/api/v1/banking/payments/dashboard", headers=headers)
    assert dash.status_code == 200
    assert dash.json()["data"]["summary"]["transfer_count"] >= 1
