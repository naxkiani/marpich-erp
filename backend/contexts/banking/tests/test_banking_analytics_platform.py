"""Banking Analytics Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.banking.container import (
    get_banking_analytics_platform_service,
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
    get_banking_analytics_platform_service()
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
        json={"email": "analytics@bank.dev", "password": "SecurePass123!", "display_name": "Analytics"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "analytics@bank.dev", "password": "SecurePass123!"},
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
    await get_banking_analytics_platform_service().handle_tenant_provisioned(
        {"tenant_id": slug, "payload": {}}
    )


@pytest.mark.asyncio
async def test_analytics_catalog(client):
    slug = "anacat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/banking/analytics/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "liquidity_kpis" in caps
    assert "executive_dashboard" in caps
    assert "ai_banking_assistant" in caps
    assert "fraud_detection" in caps
    assert "delinquency_analysis" in caps


@pytest.mark.asyncio
async def test_liquidity_and_portfolio_analytics(client):
    slug = "anakpi"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    liquidity = await client.get("/api/v1/banking/analytics/liquidity-kpis", headers=headers)
    assert liquidity.status_code == 200
    assert "kpis" in liquidity.json()["data"]

    portfolio = await client.get("/api/v1/banking/analytics/loan-portfolio", headers=headers)
    assert portfolio.status_code == 200
    assert "total_loans" in portfolio.json()["data"]

    delinquency = await client.get("/api/v1/banking/analytics/delinquency-analysis", headers=headers)
    assert delinquency.status_code == 200
    assert "delinquency_rate" in delinquency.json()["data"]


@pytest.mark.asyncio
async def test_executive_dashboard_and_recommendations(client):
    slug = "anaexec"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    executive = await client.get("/api/v1/banking/analytics/executive-dashboard", headers=headers)
    assert executive.status_code == 200
    data = executive.json()["data"]
    assert data["audience"] == "executive"
    assert data["explainable"] is True
    assert "headline" in data

    recs = await client.get("/api/v1/banking/analytics/recommendations", headers=headers)
    assert recs.status_code == 200
    assert recs.json()["data"]["explainable"] is True
    assert "recommendations" in recs.json()["data"]


@pytest.mark.asyncio
async def test_ai_assistant_and_analyze_job(client):
    slug = "anaai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    assistant = await client.post(
        "/api/v1/banking/analytics/ai-assistant",
        headers=headers,
        json={"query": "portfolio health"},
    )
    assert assistant.status_code == 200
    data = assistant.json()["data"]
    assert data["assistant"] == "banking_ai"
    assert data["explainable"] is True
    assert "insights" in data
    assert data["autonomous_execution"] is False

    analyze = await client.post(
        "/api/v1/banking/analytics/analyze/forecasting",
        headers=headers,
        json={"input_data": {}},
    )
    assert analyze.status_code == 201
    job = analyze.json()["data"]
    assert job["capability"] == "forecasting"
    assert job["status"] == "completed"

    jobs = await client.get("/api/v1/banking/analytics/jobs", headers=headers)
    assert jobs.status_code == 200
    assert len(jobs.json()["data"]) >= 1


@pytest.mark.asyncio
async def test_analytics_dashboard(client):
    slug = "anadash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/banking/analytics/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert "liquidity_kpis" in data
    assert "executive_headline" in data
    assert data["explainable"] is True

    forecast = await client.get("/api/v1/banking/analytics/forecasting", headers=headers)
    assert forecast.status_code == 200
    assert "projections" in forecast.json()["data"]

    fraud = await client.get("/api/v1/banking/analytics/fraud-detection", headers=headers)
    assert fraud.status_code == 200
    assert "flagged_transactions" in fraud.json()["data"]
