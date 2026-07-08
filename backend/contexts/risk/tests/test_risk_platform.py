"""Enterprise Risk Platform tests."""
import pytest
from httpx import ASGITransport, AsyncClient

import contexts.identity.container as identity_container
from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
from contexts.policy.container import get_policy_service, reset_policy_service
from contexts.risk.container import get_risk_service, reset_risk_service
from contexts.risk.domain.aggregates.risk_platform import RiskCapability, RiskCategory
from contexts.risk.domain.services import risk_engine
from contexts.risk.infrastructure.persistence.risk_memory_store import (
    InMemoryEnterpriseRiskItemRepository,
    InMemoryRiskMatrixSnapshotRepository,
    InMemoryRiskPredictionRepository,
    InMemoryRiskTenantProfileRepository,
)
from core.presentation.api.main import app
from shared.infrastructure.messaging.event_bus import InProcessEventBus


@pytest.fixture(autouse=True)
def reset_all():
    identity_container._container = None
    InMemoryStore.reset()
    InMemoryRiskTenantProfileRepository.reset()
    InMemoryEnterpriseRiskItemRepository.reset()
    InMemoryRiskMatrixSnapshotRepository.reset()
    InMemoryRiskPredictionRepository.reset()
    InProcessEventBus.reset()
    reset_policy_service()
    reset_risk_service()
    get_policy_service()
    get_risk_service()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient, tenant: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "erp@enterprise.dev", "password": "SecurePass123!", "display_name": "ERP"},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "erp@enterprise.dev", "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_catalog_lists_risk_capabilities(client):
    headers = await _auth_headers(client, "erpcat")
    resp = await client.get("/api/v1/risk/catalog", headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    caps = {c["capability"] for c in data["capabilities"]}
    assert RiskCapability.FINANCIAL_RISK.value in caps
    assert RiskCapability.TREASURY_RISK.value in caps
    assert RiskCapability.FX_RISK.value in caps
    assert RiskCapability.RISK_MATRIX.value in caps
    assert RiskCapability.RISK_HEATMAP.value in caps
    assert RiskCapability.AI_RISK_PREDICTION.value in caps
    assert len(caps) == 15
    assert data["delegation"]["local_risk_duplication"] is False
    cats = {c["category"] for c in data["categories"]}
    assert RiskCategory.CYBER.value in cats
    assert len(cats) == 10


@pytest.mark.asyncio
async def test_seed_register_matrix_heatmap_and_predict(client):
    slug = "erpseed"
    headers = await _auth_headers(client, slug)

    seed = await client.post("/api/v1/risk/seed", headers=headers)
    assert seed.status_code == 200
    body = seed.json()["data"]
    assert body["seeded"] is True
    assert body["risks_seeded"] == 10
    assert body["enabled_categories"] == 10

    register = await client.post(
        "/api/v1/risk/register",
        headers=headers,
        json={
            "title": "Custom supply chain disruption",
            "category": "operational",
            "likelihood": 4,
            "impact": 5,
        },
    )
    assert register.status_code == 201
    reg = register.json()["data"]
    assert reg["risk_score"] == 20
    assert reg["severity"] in ("high", "critical", "escalated")

    matrix = await client.get("/api/v1/risk/matrix", headers=headers)
    assert matrix.status_code == 200
    mtx = matrix.json()["data"]
    assert mtx["matrix_size"] == 5
    assert mtx["total_mapped"] >= 10
    assert "snapshot" in mtx

    heatmap = await client.get("/api/v1/risk/heatmap", headers=headers)
    assert heatmap.status_code == 200
    hm = heatmap.json()["data"]
    assert hm["total_open"] >= 10
    assert len(hm["categories"]) >= 1

    predict = await client.post(
        "/api/v1/risk/predict",
        headers=headers,
        json={"category": "cyber"},
    )
    assert predict.status_code == 200
    pred = predict.json()["data"]
    assert pred["explainable"] is True
    assert pred["autonomous_execution"] is False
    assert "prediction" in pred
    assert "factors" in pred

    dash = await client.get("/api/v1/risk/dashboard", headers=headers)
    assert dash.status_code == 200
    d = dash.json()["data"]
    assert d["summary"]["capabilities"] == 15
    assert d["delegation"]["local_risk_duplication"] is False


@pytest.mark.asyncio
async def test_escalate_risk(client):
    slug = "erpesc"
    headers = await _auth_headers(client, slug)
    await client.post("/api/v1/risk/seed", headers=headers)

    risks = await client.get("/api/v1/risk/register", headers=headers)
    risk_ref = risks.json()["data"][0]["risk_ref"]

    esc = await client.post(f"/api/v1/risk/register/{risk_ref}/escalate", headers=headers)
    assert esc.status_code == 200
    assert esc.json()["data"]["status"] == "escalated"


def test_engine_matrix_heatmap_and_prediction():
    risks = [
        {"risk_ref": "R1", "category": "financial", "likelihood": 3, "impact": 4, "risk_score": 12, "status": "open", "severity": "high"},
        {"risk_ref": "R2", "category": "cyber", "likelihood": 4, "impact": 4, "risk_score": 16, "status": "open", "severity": "high"},
    ]
    matrix = risk_engine.build_risk_matrix(risks=risks, matrix_size=5)
    assert matrix["total_mapped"] == 2

    heatmap = risk_engine.build_heatmap(risks=risks)
    assert heatmap["total_open"] == 2

    pred = risk_engine.ai_risk_prediction(
        category="cyber", risks=risks, escalation_threshold=12, confidence_threshold=0.7
    )
    assert pred["explainable"] is True
    assert pred["autonomous_execution"] is False

    dm = risk_engine.dependency_map()
    assert dm["no_risk_duplication"] is True
