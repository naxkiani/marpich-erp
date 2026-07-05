"""Enterprise Cash Forecast tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.treasury.container import (
    get_cash_forecast_service,
    get_treasury_service,
    reset_treasury_service,
)
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from core.presentation.api.main import app


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    reset_treasury_service()
    get_treasury_service()
    get_cash_forecast_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "fc@treasury.dev", "password": "SecurePass123!", "display_name": "FC Mgr"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "fc@treasury.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


async def _provision(slug: str) -> None:
    await get_treasury_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})
    await get_cash_forecast_service().handle_tenant_provisioned({"tenant_id": slug, "payload": {}})


@pytest.mark.asyncio
async def test_forecast_catalog(client):
    slug = "fccat"
    headers = await _auth_headers(client, slug)
    resp = await client.get("/api/v1/treasury/cash-forecast/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]}
    assert "daily" in caps
    assert "payroll" in caps
    assert "hospital_revenue" in caps
    assert "ai_forecast" in caps
    assert "scenario_simulation" in caps
    assert len(caps) == 17


@pytest.mark.asyncio
async def test_period_forecasts(client):
    slug = "fcperiod"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    for path, key in (
        ("/daily?days=14", 14),
        ("/weekly?weeks=8", 8),
        ("/monthly?months=6", 6),
        ("/quarterly?quarters=4", 4),
        ("/annual?years=2", 2),
    ):
        resp = await client.get(f"/api/v1/treasury/cash-forecast{path}", headers=headers)
        assert resp.status_code == 200, path
        data = resp.json()["data"]
        assert "confidence_score" in data
        assert len(data["lines"]) == key


@pytest.mark.asyncio
async def test_category_breakdown(client):
    slug = "fccatbr"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    cats = await client.get("/api/v1/treasury/cash-forecast/categories", headers=headers)
    assert cats.status_code == 200
    assert len(cats.json()["data"]) == 9

    breakdown = await client.get("/api/v1/treasury/cash-forecast/categories/breakdown", headers=headers)
    assert breakdown.status_code == 200
    data = breakdown.json()["data"]
    assert "payroll" in data["all_categories"]
    assert "hospital_revenue" in data["all_categories"]
    assert data["total_inflow"] > 0


@pytest.mark.asyncio
async def test_create_plan_with_confidence(client):
    slug = "fcplan"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    resp = await client.post(
        "/api/v1/treasury/cash-forecast/plans",
        headers=headers,
        json={
            "name": "Q4 Forecast",
            "period_type": "monthly",
            "period_start": "2025-10-01",
            "period_end": "2025-12-31",
            "scenario": "base",
            "projected_lines": [
                {"date": "2025-10-15", "label": "Payroll", "category": "payroll", "outflow": 10000},
                {"date": "2025-10-20", "label": "Tuition", "category": "student_tuition", "inflow": 12000},
            ],
        },
    )
    assert resp.status_code == 201
    plan = resp.json()["data"]
    assert plan["confidence_score"] > 0
    assert "payroll" in plan["category_totals"]


@pytest.mark.asyncio
async def test_ai_forecast_and_scenario_simulation(client):
    slug = "fcai"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    plans = await client.get("/api/v1/treasury/cash-forecast/plans", headers=headers)
    plan_id = plans.json()["data"][0]["id"]

    ai = await client.post(
        "/api/v1/treasury/cash-forecast/ai/forecast",
        headers=headers,
        json={"horizon_days": 60},
    )
    assert ai.status_code == 200
    ai_data = ai.json()["data"]
    assert "confidence_score" in ai_data
    assert ai_data["autonomous_execution"] is False
    assert "explanation" in ai_data

    sim = await client.post(
        f"/api/v1/treasury/cash-forecast/plans/{plan_id}/simulate",
        headers=headers,
        json={"name": "Q3 Scenario Run"},
    )
    assert sim.status_code == 200
    sim_data = sim.json()["data"]
    assert len(sim_data["scenarios"]) == 3
    scenarios = {s["scenario"] for s in sim_data["scenarios"]}
    assert "optimistic" in scenarios
    assert "pessimistic" in scenarios


@pytest.mark.asyncio
async def test_forecast_dashboard(client):
    slug = "fcdash"
    headers = await _auth_headers(client, slug)
    await _provision(slug)

    dash = await client.get("/api/v1/treasury/cash-forecast/dashboard", headers=headers)
    assert dash.status_code == 200
    data = dash.json()["data"]
    assert "daily_cash" in data
    assert "weekly_cash" in data
    assert "monthly_cash" in data
    assert "quarterly_cash" in data
    assert "annual_cash" in data
    assert "category_breakdown" in data
    assert "ai_forecast" in data
    assert data["summary"]["avg_confidence_score"] > 0
