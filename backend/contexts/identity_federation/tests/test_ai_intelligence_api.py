"""P198-C2 intelligence API integration tests."""
import pytest

from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_intelligence_predict_dashboard_copilot(integration_client):
    tenant = "federation-intel-c2"
    headers = await auth_headers(integration_client, tenant=tenant, email="intel@enterprise.dev")
    await integration_client.post("/api/v1/federation/seed", headers=headers)

    models = await integration_client.get("/api/v1/federation/intelligence/models", headers=headers)
    assert models.status_code == 200
    assert len(models.json()["data"]["models"]) >= 1

    predict = await integration_client.post(
        "/api/v1/federation/intelligence/predict",
        headers=headers,
        json={
            "model_id": "identity_risk_predictor_v1",
            "features": {"failed_logins": 4, "device_confidence": 0.35, "geo_risk": 0.4},
        },
    )
    assert predict.status_code == 200
    body = predict.json()["data"]
    assert "explanation" in body
    assert body["explanation"]["explainable"] is True

    dash = await integration_client.get(
        "/api/v1/federation/intelligence/dashboard", headers=headers
    )
    assert dash.status_code == 200
    assert "performance_targets" in dash.json()["data"]

    copilot = await integration_client.post(
        "/api/v1/federation/intelligence/copilot",
        headers=headers,
        json={"question": "Summarize audit events", "context": {}},
    )
    assert copilot.status_code == 200

    compliance = await integration_client.get(
        "/api/v1/federation/intelligence/compliance/controls", headers=headers
    )
    assert compliance.status_code == 200
    assert "privacy" in compliance.json()["data"]
