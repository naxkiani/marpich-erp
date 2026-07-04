"""Enterprise Payment Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import get_payment_service, reset_financial_kernel_service
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_payment_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "pay@kernel.dev", "password": "SecurePass123!", "display_name": "Pay Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "pay@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_cash_payment_with_auto_allocation(client):
    slug = "pay-cash"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/payments",
        headers=headers,
        json={
            "source_context": "pos",
            "source_document_id": "sale-100",
            "payment_method": "cash",
            "amount": 300,
            "reference": "CASH-100",
            "open_items": [
                {"document_id": "inv-1", "amount_due": 200, "due_date": "2025-07-01"},
                {"document_id": "inv-2", "amount_due": 150, "due_date": "2025-07-15"},
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "allocated"
    assert len(data["allocations"]) == 2
    assert data["allocations"][0]["document_id"] == "inv-1"


@pytest.mark.asyncio
async def test_split_payment(client):
    slug = "pay-split"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/payments/split",
        headers=headers,
        json={
            "source_context": "hospital",
            "source_document_id": "bill-50",
            "payment_method": "card",
            "total_amount": 1000,
            "reference": "SPLIT-50",
            "splits": [
                {"amount": 600, "payment_method": "card"},
                {"amount": 400, "payment_method": "bank_transfer"},
            ],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["status"] == "settled"
    assert len(data["splits"]) == 2


@pytest.mark.asyncio
async def test_partial_payment(client):
    slug = "pay-partial"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/payments",
        headers=headers,
        json={
            "source_context": "retail",
            "source_document_id": "ord-20",
            "payment_method": "bank_transfer",
            "amount": 500,
            "paid_amount": 200,
            "reference": "PART-20",
        },
    )
    payment_id = create.json()["data"]["id"]
    assert create.json()["data"]["status"] == "partial"

    partial = await client.post(
        f"/api/v1/financial-kernel/payments/{payment_id}/partial",
        headers=headers,
        json={"amount": 300},
    )
    assert partial.status_code == 200
    assert partial.json()["data"]["status"] == "settled"


@pytest.mark.asyncio
async def test_installments_and_advance(client):
    slug = "pay-install"
    headers = await _auth_headers(client, slug)

    install = await client.post(
        "/api/v1/financial-kernel/payments/installments",
        headers=headers,
        json={
            "source_context": "university",
            "source_document_id": "tuition-1",
            "payment_method": "bank_transfer",
            "total_amount": 3000,
            "reference": "INST-1",
            "installment_count": 3,
            "due_dates": ["2025-08-01", "2025-09-01", "2025-10-01"],
        },
    )
    assert install.status_code == 201
    assert "installment_plan" in install.json()["data"]
    assert len(install.json()["data"]["installment_plan"]["installments"]) == 3

    advance = await client.post(
        "/api/v1/financial-kernel/payments/advance",
        headers=headers,
        json={
            "source_context": "construction",
            "source_document_id": "proj-1",
            "payment_method": "cheque",
            "amount": 5000,
            "reference": "ADV-1",
        },
    )
    assert advance.status_code == 201
    assert advance.json()["data"]["payment_kind"] == "advance"


@pytest.mark.asyncio
async def test_refund_and_chargeback(client):
    slug = "pay-refund"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/payments",
        headers=headers,
        json={
            "source_context": "pos",
            "source_document_id": "sale-200",
            "payment_method": "card",
            "amount": 150,
            "reference": "CARD-200",
        },
    )
    payment_id = create.json()["data"]["id"]

    refund = await client.post(
        f"/api/v1/financial-kernel/payments/{payment_id}/refund",
        headers=headers,
        json={"amount": 50},
    )
    assert refund.status_code == 200
    assert refund.json()["data"]["refund_amount"] == 50

    chargeback = await client.post(
        f"/api/v1/financial-kernel/payments/{payment_id}/chargeback",
        headers=headers,
        json={"amount": 100},
    )
    assert chargeback.status_code == 200
    assert chargeback.json()["data"]["status"] == "chargeback"


@pytest.mark.asyncio
async def test_wallet_and_mobile_money(client):
    slug = "pay-wallet"
    headers = await _auth_headers(client, slug)
    for method in ("wallet", "mobile_money"):
        resp = await client.post(
            "/api/v1/financial-kernel/payments",
            headers=headers,
            json={
                "source_context": "pos",
                "source_document_id": f"sale-{method}",
                "payment_method": method,
                "amount": 75,
                "reference": method.upper(),
            },
        )
        assert resp.status_code == 201
        assert resp.json()["data"]["payment_method"] == method


@pytest.mark.asyncio
async def test_payment_matching_and_reconciliation(client):
    slug = "pay-recon"
    headers = await _auth_headers(client, slug)
    await client.post(
        "/api/v1/financial-kernel/payments",
        headers=headers,
        json={
            "source_context": "retail",
            "source_document_id": "sale-recon",
            "payment_method": "bank_transfer",
            "amount": 800,
            "reference": "BNK-800",
        },
    )

    match = await client.post(
        "/api/v1/financial-kernel/payments/matching",
        headers=headers,
        json={
            "bank_items": [{"reference": "BNK-800", "amount": 800}],
        },
    )
    assert match.status_code == 200
    assert len(match.json()["data"]["matched_pairs"]) >= 1

    recon = await client.post(
        "/api/v1/financial-kernel/payments/reconciliation",
        headers=headers,
        json={
            "reconciliation_date": "2025-06-30",
            "payment_items": [{"reference": "BNK-800", "amount": 800}],
            "bank_items": [{"reference": "BNK-800", "amount": 800}],
        },
    )
    assert recon.status_code == 201
    assert recon.json()["data"]["status"] == "matched"
