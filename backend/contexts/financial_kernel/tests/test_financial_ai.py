"""Enterprise Financial AI tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_ai_service,
    get_financial_kernel_service,
    get_payment_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_financial_ai_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "ai@kernel.dev", "password": "SecurePass123!", "display_name": "AI Admin"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "ai@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _seed_financial_data(slug: str, headers: dict) -> None:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    rev = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    cash = (await svc.resolve_account_code(slug, "cash")).unwrap()
    expense = (await svc.resolve_account_code(slug, "clinical_staff")).unwrap()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "hospital",
                "source_document_id": "enc-ai-1",
                "lines": [
                    {"account_code": cash, "debit": 5000, "credit": 0},
                    {"account_code": rev, "debit": 0, "credit": 5000},
                ],
            },
        )
        await ac.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "hospital",
                "source_document_id": "enc-ai-2",
                "lines": [
                    {"account_code": expense, "debit": 1200, "credit": 0, "cost_center": "CC-01"},
                    {"account_code": cash, "debit": 0, "credit": 1200},
                ],
            },
        )

    pay_svc = get_payment_service()
    await pay_svc.create_payment(
        tenant_id=slug,
        source_context="hospital",
        source_document_id="pay-1",
        idempotency_key="ai-pay-1",
        payment_method="bank_transfer",
        amount=15000,
        currency="USD",
        reference="large-payment",
    )
    await pay_svc.create_payment(
        tenant_id=slug,
        source_context="hospital",
        source_document_id="pay-2",
        idempotency_key="ai-pay-2",
        payment_method="card",
        amount=200,
        currency="USD",
        reference="small-payment",
    )


@pytest.mark.asyncio
async def test_list_capabilities(client):
    slug = "aicap"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/financial-kernel/financial-ai/capabilities", headers=headers)
    assert resp.status_code == 200
    caps = {c["id"] for c in resp.json()["data"]}
    assert "fraud_detection" in caps
    assert "cfo_assistant" in caps
    assert "dashboard" in caps
    assert len(caps) == 13


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "capability",
    [
        "fraud_detection",
        "cash_flow_prediction",
        "budget_forecast",
        "expense_analysis",
        "revenue_prediction",
        "financial_summary",
        "risk_analysis",
        "recommendation",
    ],
)
async def test_analyze_capabilities(client, capability):
    slug = f"ai{capability[:6].replace('_', '')}"
    headers = await _auth_headers(client, slug)
    await _seed_financial_data(slug, headers)
    resp = await client.post(
        f"/api/v1/financial-kernel/financial-ai/analyze/{capability}",
        headers=headers,
        json={"input_data": {}},
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["capability"] == capability
    assert data["status"] == "completed"
    assert data["result"] is not None
    assert data["confidence"] is not None


@pytest.mark.asyncio
async def test_fraud_detection_flags_large_payment(client):
    slug = "aifraud"
    headers = await _auth_headers(client, slug)
    await _seed_financial_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/analyze/fraud_detection",
        headers=headers,
        json={"input_data": {"threshold": 10000}},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert result["alert_count"] >= 1
    assert result["fraud_score"] > 0


@pytest.mark.asyncio
async def test_invoice_classification(client):
    slug = "aiinvoice"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/invoice/classify",
        headers=headers,
        json={"text": "Purchase invoice from supplier ACME", "amount": 500},
    )
    assert resp.status_code == 201
    assert resp.json()["data"]["result"]["document_type"] == "purchase_invoice"


@pytest.mark.asyncio
async def test_document_ocr(client):
    slug = "aiocr"
    headers = await _auth_headers(client, slug)
    text = "ACME Corp\nConsulting services\nTotal: $1,250.00"
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/document/ocr",
        headers=headers,
        json={"text": text},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert result["detected_amount"] == 1250.0
    assert result["fields"]["vendor"] == "ACME Corp"


@pytest.mark.asyncio
async def test_ai_dashboard(client):
    slug = "aidash"
    headers = await _auth_headers(client, slug)
    await _seed_financial_data(slug, headers)
    resp = await client.get("/api/v1/financial-kernel/financial-ai/dashboard", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "kpis" in data
    assert "widgets" in data
    assert len(data["widgets"]) >= 5
    assert data["kpis"]["revenue"] > 0


@pytest.mark.asyncio
async def test_financial_chatbot(client):
    slug = "aichat"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/chat",
        headers=headers,
        json={"message": "Tell me about cash flow"},
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert "cash flow" in data["reply"].lower()
    assert data["session_id"]

    follow = await client.post(
        "/api/v1/financial-kernel/financial-ai/chat",
        headers=headers,
        json={"message": "What about fraud?", "session_id": data["session_id"]},
    )
    assert follow.status_code == 201
    assert len(follow.json()["data"]["messages"]) >= 4


@pytest.mark.asyncio
async def test_cfo_assistant(client):
    slug = "aicfo"
    headers = await _auth_headers(client, slug)
    await _seed_financial_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/cfo-assistant",
        headers=headers,
        json={"message": "Give me an executive summary"},
    )
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["executive_summary"]
    assert "kpis" in data
    assert "recommended_actions" in data
    assert data["kpis"]["revenue"] > 0


@pytest.mark.asyncio
async def test_list_and_get_jobs(client):
    slug = "aijobs"
    headers = await _auth_headers(client, slug)
    await _seed_financial_data(slug, headers)
    created = await client.post(
        "/api/v1/financial-kernel/financial-ai/analyze/financial_summary",
        headers=headers,
        json={"input_data": {}},
    )
    job_id = created.json()["data"]["id"]
    listed = await client.get("/api/v1/financial-kernel/financial-ai/jobs", headers=headers)
    assert listed.status_code == 200
    assert any(j["id"] == job_id for j in listed.json()["data"])
    fetched = await client.get(
        f"/api/v1/financial-kernel/financial-ai/jobs/{job_id}",
        headers=headers,
    )
    assert fetched.status_code == 200
    assert fetched.json()["data"]["id"] == job_id


@pytest.mark.asyncio
async def test_invalid_capability_rejected(client):
    slug = "aibad"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/financial-ai/analyze/not_a_capability",
        headers=headers,
        json={"input_data": {}},
    )
    assert resp.status_code == 400
