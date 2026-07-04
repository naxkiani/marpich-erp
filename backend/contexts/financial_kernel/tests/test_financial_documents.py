"""Enterprise Financial Documents tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_document_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_document_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "fdoc@kernel.dev", "password": "SecurePass123!", "display_name": "Doc Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "fdoc@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_sales_invoice_with_pdf_and_qr(client):
    slug = "fdoc-invoice"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-documents",
        headers=headers,
        json={
            "source_context": "sales",
            "source_document_id": "order-100",
            "document_type": "sales_invoice",
            "total_amount": 1500,
            "counterparty_name": "Acme Corp",
            "reference": "SI-100",
            "lines": [{"description": "Widget", "quantity": 10, "unit_price": 150}],
        },
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["document"]["document_type"] == "sales_invoice"
    assert data["document"]["status"] == "draft"
    assert data["document"]["document_number"].startswith("SI-")
    assert len(data["versions"]) == 1
    assert data["versions"][0]["pdf_base64"]
    assert data["qr_verification_url"]

    doc_id = data["document"]["id"]
    pdf = await client.get(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/pdf",
        headers=headers,
    )
    assert pdf.status_code == 200
    assert pdf.json()["data"]["content_type"] == "application/pdf"


@pytest.mark.asyncio
async def test_document_types(client):
    slug = "fdoc-types"
    headers = await _auth_headers(client, slug)
    for doc_type in (
        "invoice",
        "bill",
        "voucher",
        "receipt",
        "payment_order",
        "purchase_invoice",
        "credit_note",
        "debit_note",
        "journal_voucher",
        "cash_voucher",
        "bank_voucher",
    ):
        resp = await client.post(
            "/api/v1/financial-kernel/financial-documents",
            headers=headers,
            json={
                "source_context": "accounting",
                "source_document_id": f"doc-{doc_type}",
                "document_type": doc_type,
                "total_amount": 100,
                "counterparty_name": "Vendor",
                "reference": doc_type.upper(),
            },
        )
        assert resp.status_code == 201, doc_type
        assert resp.json()["data"]["document"]["document_type"] == doc_type


@pytest.mark.asyncio
async def test_versioning(client):
    slug = "fdoc-version"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/financial-documents",
        headers=headers,
        json={
            "source_context": "retail",
            "source_document_id": "bill-1",
            "document_type": "bill",
            "total_amount": 500,
            "counterparty_name": "Supplier",
            "reference": "BILL-1",
        },
    )
    doc_id = create.json()["data"]["document"]["id"]

    version = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/versions",
        headers=headers,
        json={"total_amount": 550, "lines": [{"description": "Updated", "quantity": 1, "unit_price": 550}]},
    )
    assert version.status_code == 201
    assert len(version.json()["data"]["versions"]) == 2
    assert version.json()["data"]["document"]["total_amount"] == 550


@pytest.mark.asyncio
async def test_approval_workflow_and_issue(client):
    slug = "fdoc-approval"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/financial-documents",
        headers=headers,
        json={
            "source_context": "accounting",
            "source_document_id": "jv-1",
            "document_type": "journal_voucher",
            "total_amount": 2000,
            "counterparty_name": "Internal",
            "reference": "JV-1",
        },
    )
    doc_id = create.json()["data"]["document"]["id"]

    issue_early = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/issue",
        headers=headers,
    )
    assert issue_early.status_code == 400

    approval = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/approval",
        headers=headers,
    )
    assert approval.status_code == 200
    assert approval.json()["data"]["status"] == "pending_approval"

    complete = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/approval/complete",
        headers=headers,
    )
    assert complete.status_code == 200
    assert complete.json()["data"]["status"] == "approved"

    issue = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/issue",
        headers=headers,
    )
    assert issue.status_code == 200
    assert issue.json()["data"]["document"]["status"] == "issued"


@pytest.mark.asyncio
async def test_digital_signature_and_qr_verification(client):
    slug = "fdoc-sign"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/financial-documents",
        headers=headers,
        json={
            "source_context": "pos",
            "source_document_id": "rct-1",
            "document_type": "receipt",
            "total_amount": 75,
            "counterparty_name": "Walk-in Customer",
            "reference": "RCT-1",
        },
    )
    doc_id = create.json()["data"]["document"]["id"]
    qr_url = create.json()["data"]["qr_verification_url"]
    token = qr_url.split("/verify/")[-1]

    sign = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/sign",
        headers=headers,
        json={},
    )
    assert sign.status_code == 200
    assert sign.json()["data"]["document"]["signature"]["algorithm"] == "RS256"

    verify = await client.get(f"/api/v1/financial-kernel/financial-documents/verify/{token}")
    assert verify.status_code == 200
    assert verify.json()["data"]["valid"] is True


@pytest.mark.asyncio
async def test_receipt_issue_without_approval(client):
    slug = "fdoc-receipt"
    headers = await _auth_headers(client, slug)
    create = await client.post(
        "/api/v1/financial-kernel/financial-documents",
        headers=headers,
        json={
            "source_context": "pos",
            "source_document_id": "rct-2",
            "document_type": "receipt",
            "total_amount": 42,
            "counterparty_name": "Customer",
            "reference": "RCT-2",
        },
    )
    doc_id = create.json()["data"]["document"]["id"]
    issue = await client.post(
        f"/api/v1/financial-kernel/financial-documents/{doc_id}/issue",
        headers=headers,
    )
    assert issue.status_code == 200
    assert issue.json()["data"]["document"]["status"] == "issued"
