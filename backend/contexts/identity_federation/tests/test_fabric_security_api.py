"""P198-C1 fabric security API integration tests."""
import pytest

from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fabric_mesh_trust_dashboard(integration_client):
    tenant = "federation-fabric-c1"
    headers = await auth_headers(integration_client, tenant=tenant, email="fabric@enterprise.dev")
    await integration_client.post("/api/v1/federation/seed", headers=headers)
    await integration_client.post(
        "/api/v1/federation/providers",
        headers=headers,
        json={"protocol": "saml", "name": "Hospital IdP", "config": {"industry": "hospital"}},
    )

    mesh = await integration_client.get("/api/v1/federation/fabric/mesh", headers=headers)
    assert mesh.status_code == 200
    assert mesh.json()["data"]["controller"] == "identity_mesh_controller"

    node = await integration_client.post(
        "/api/v1/federation/fabric/trust-graph/nodes",
        headers=headers,
        json={"node_id": "org:hospital", "node_type": "organization"},
    )
    assert node.status_code == 200

    await integration_client.post(
        "/api/v1/federation/fabric/trust-graph/nodes",
        headers=headers,
        json={"node_id": "app:erp", "node_type": "application"},
    )
    edge = await integration_client.post(
        "/api/v1/federation/fabric/trust-graph/edges",
        headers=headers,
        json={
            "edge_id": "e1",
            "from_id": "org:hospital",
            "to_id": "app:erp",
            "relation": "ownership",
        },
    )
    assert edge.status_code == 200

    zt = await integration_client.post(
        "/api/v1/federation/fabric/zero-trust/evaluate",
        headers=headers,
        json={
            "user_id": "doc-1",
            "identity_verified": True,
            "device_trusted": True,
            "risk_score": 15,
            "trust_score": 75,
            "use_adaptive_pdp": False,
        },
    )
    assert zt.status_code == 200
    assert zt.json()["data"]["action"] in ("allow", "step_up", "deny")

    dash = await integration_client.get(
        "/api/v1/federation/fabric/security/dashboard", headers=headers
    )
    assert dash.status_code == 200
    body = dash.json()["data"]
    assert "identity_trust" in body
    assert "threat_detection" in body
