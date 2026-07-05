"""Enterprise General Ledger AI Assistant tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.financial_kernel.container import (
    get_financial_kernel_service,
    get_gl_ai_service,
    reset_financial_kernel_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_financial_kernel_service()
    get_gl_ai_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "glai@kernel.dev", "password": "SecurePass123!", "display_name": "GL AI"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "glai@kernel.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _seed_gl_data(slug: str, headers: dict) -> str:
    svc = get_financial_kernel_service()
    await svc.handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {"industry_pack": "hospital"}}
    )
    rev = (await svc.resolve_account_code(slug, "patient_service_revenue")).unwrap()
    cash = (await svc.resolve_account_code(slug, "cash")).unwrap()
    expense = (await svc.resolve_account_code(slug, "clinical_staff")).unwrap()

    transport = ASGITransport(app=app)
    journal_id = ""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp1 = await ac.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "hospital",
                "source_document_id": "enc-gl-1",
                "lines": [
                    {"account_code": cash, "debit": 5000, "credit": 0},
                    {"account_code": rev, "debit": 0, "credit": 5000},
                ],
            },
        )
        journal_id = resp1.json()["data"]["id"]
        await ac.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "hospital",
                "source_document_id": "enc-gl-2",
                "lines": [
                    {"account_code": expense, "debit": 1200, "credit": 0, "cost_center": "CC-01"},
                    {"account_code": cash, "debit": 0, "credit": 1200},
                ],
            },
        )
        await ac.post(
            "/api/v1/financial-kernel/ledger/journals/automatic",
            headers=headers,
            json={
                "source_context": "hospital",
                "source_document_id": "enc-gl-1",
                "idempotency_key": "dup-key-1",
                "lines": [
                    {"account_code": cash, "debit": 5000, "credit": 0},
                    {"account_code": rev, "debit": 0, "credit": 5000},
                ],
            },
        )
    return journal_id


@pytest.mark.asyncio
async def test_list_gl_ai_catalog(client):
    slug = "glcatalog"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/financial-kernel/gl-ai/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "posting_suggestions" in caps
    assert "journal_explanation" in caps
    assert "ai_cfo_dashboard" in caps
    assert len(caps) == 12
    for cap in resp.json()["data"]:
        assert cap["autonomous_posting"] is False
        assert cap["explainable"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "capability",
    [
        "posting_suggestions",
        "account_suggestions",
        "duplicate_detection",
        "fraud_detection",
        "closing_assistant",
        "anomaly_detection",
        "financial_insights",
        "automatic_classification",
        "forecasting",
        "variance_analysis",
    ],
)
async def test_gl_ai_analyze_capabilities(client, capability):
    slug = f"gl{capability.replace('_', '')[:12]}"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    payload = {"input_data": {"description": "payroll expense", "amount": 1200}}
    if capability == "automatic_classification":
        journals = await client.get(
            "/api/v1/financial-kernel/ledger/journals", headers=headers
        )
        jid = journals.json()["data"][0]["id"]
        payload = {"input_data": {"journal_id": jid}}
    resp = await client.post(
        f"/api/v1/financial-kernel/gl-ai/analyze/{capability}",
        headers=headers,
        json=payload,
    )
    assert resp.status_code == 201
    job = resp.json()["data"]
    assert job["status"] == "completed"
    assert job["capability"] == capability
    assert job["confidence"] is not None


@pytest.mark.asyncio
async def test_posting_suggestions_explainable(client):
    slug = "glpost"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/gl-ai/analyze/posting_suggestions",
        headers=headers,
        json={"input_data": {"description": "office supplies", "amount": 250}},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert result["suggested_lines"]
    rec = result["recommendations"][0]
    assert rec["explanation"]
    assert rec["autonomous_posting"] is False
    assert "evidence" in rec


@pytest.mark.asyncio
async def test_duplicate_detection(client):
    slug = "gldup"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/gl-ai/analyze/duplicate_detection",
        headers=headers,
        json={"input_data": {}},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert result["duplicate_count"] >= 1
    assert any(r["category"] == "duplicate_detection" for r in result["recommendations"])


@pytest.mark.asyncio
async def test_journal_explanation(client):
    slug = "glexplain"
    headers = await _auth_headers(client, slug)
    journal_id = await _seed_gl_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/gl-ai/explain-journal",
        headers=headers,
        json={"journal_id": journal_id},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert "explanation" in result
    assert len(result["explanation"]) > 20
    rec = result["recommendations"][0]
    assert rec["category"] == "journal_explanation"
    assert rec["confidence"] >= 0.9


@pytest.mark.asyncio
async def test_variance_analysis(client):
    slug = "glvar"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    resp = await client.post(
        "/api/v1/financial-kernel/gl-ai/analyze/variance_analysis",
        headers=headers,
        json={"input_data": {}},
    )
    assert resp.status_code == 201
    result = resp.json()["data"]["result"]
    assert "variances" in result
    assert "recommendations" in result


@pytest.mark.asyncio
async def test_gl_cfo_dashboard(client):
    slug = "glcfo"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    resp = await client.get("/api/v1/financial-kernel/gl-ai/dashboard", headers=headers)
    assert resp.status_code == 200
    dashboard = resp.json()["data"]
    assert dashboard["explainable"] is True
    assert dashboard["autonomous_posting"] is False
    assert "kpis" in dashboard
    assert "widgets" in dashboard
    assert len(dashboard["recommendations"]) > 0
    for rec in dashboard["recommendations"]:
        assert "explanation" in rec
        assert rec["autonomous_posting"] is False


@pytest.mark.asyncio
async def test_list_recommendations(client):
    slug = "glrecs"
    headers = await _auth_headers(client, slug)
    await _seed_gl_data(slug, headers)
    await client.post(
        "/api/v1/financial-kernel/gl-ai/analyze/financial_insights",
        headers=headers,
        json={"input_data": {}},
    )
    resp = await client.get("/api/v1/financial-kernel/gl-ai/recommendations", headers=headers)
    assert resp.status_code == 200
    recs = resp.json()["data"]
    assert len(recs) >= 1
    assert all("explanation" in r for r in recs)


@pytest.mark.asyncio
async def test_invalid_capability(client):
    slug = "glbad"
    headers = await _auth_headers(client, slug)
    resp = await client.post(
        "/api/v1/financial-kernel/gl-ai/analyze/not_a_capability",
        headers=headers,
        json={"input_data": {}},
    )
    assert resp.status_code == 400
