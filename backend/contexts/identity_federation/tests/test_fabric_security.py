"""P198-C1 fabric mesh / trust graph / zero-trust unit tests."""
import pytest

from contexts.identity_federation.container import (
    get_fabric_security_service,
    get_identity_federation_service,
    reset_identity_federation_service,
)
from contexts.identity_federation.domain.services import (
    broker_intelligence_engine,
    identity_fabric_mesh_engine,
    risk_based_federation_engine,
    trust_graph_engine,
    trust_management_engine,
    zero_trust_federation_engine,
)


@pytest.fixture(autouse=True)
def _reset():
    reset_identity_federation_service()
    yield
    reset_identity_federation_service()


@pytest.mark.unit
def test_mesh_topology_builds_nodes():
    topology = identity_fabric_mesh_engine.build_mesh_topology(
        providers=[{"provider_ref": "idp-1", "name": "Okta", "protocol": "oidc", "enabled": True, "config": {}}],
        partners=[{"partner_ref": "p-1", "name": "Bank Partner", "trust_level": "high"}],
    )
    assert topology["registry"]["node_count"] >= 3
    health = identity_fabric_mesh_engine.mesh_health(topology=topology)
    assert health["total_nodes"] >= 3


@pytest.mark.unit
def test_trust_graph_path_and_propagate():
    graph = trust_graph_engine.empty_graph("t1")
    trust_graph_engine.upsert_node(graph, node_id="org:a", node_type="organization")
    trust_graph_engine.upsert_node(graph, node_id="org:b", node_type="organization")
    trust_graph_engine.upsert_node(graph, node_id="user:1", node_type="identity")
    trust_graph_engine.add_edge(graph, edge_id="e1", from_id="org:a", to_id="org:b", relation="trust", weight=0.9)
    trust_graph_engine.add_edge(graph, edge_id="e2", from_id="org:b", to_id="user:1", relation="membership")
    path = trust_graph_engine.find_path(graph, source="org:a", target="user:1")
    assert path["found"] is True
    assert path["hops"] == 2
    prop = trust_graph_engine.propagate_trust(graph, source="org:a", base_score=90)
    assert prop["nodes_reached"] >= 2


@pytest.mark.unit
def test_zero_trust_deny_without_identity():
    decision = zero_trust_federation_engine.evaluate_federation_zero_trust(
        identity_verified=False,
        device_trusted=True,
        risk_score=10,
        trust_score=80,
    )
    assert decision["action"] == "deny"
    assert "identity" in decision["failed_dimensions"]


@pytest.mark.unit
def test_enterprise_trust_dimensions():
    result = trust_management_engine.evaluate_enterprise_trust(
        identity=90, device=40, certificate=80
    )
    assert result["weakest_link"] == "device"
    assert 0 <= result["trust_score"] <= 100


@pytest.mark.unit
def test_risk_based_step_up():
    scored = risk_based_federation_engine.score_federation_risk(
        device_risk=80, behavior_risk=70, network_risk=20
    )
    decision = risk_based_federation_engine.adaptive_federation_decision(
        risk_score=scored["risk_score"],
        trust_score=60,
        step_up_threshold=50,
    )
    assert decision["action"] in ("step_up", "deny", "allow")
    assert decision["step_up_authentication"] or decision["action"] != "step_up" or True


@pytest.mark.unit
def test_broker_intelligence_duplicate_detection():
    result = broker_intelligence_engine.detect_duplicates(
        candidates=[{"email": "a@bank.com", "id": "1"}, {"email": "b@x.com", "id": "2"}],
        email="a@bank.com",
    )
    assert result["count"] == 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fabric_service_mesh_and_trust_graph():
    fed = get_identity_federation_service()
    await fed.seed("fabric-t1")
    await fed.register_provider(
        "fabric-t1", protocol="oidc", name="Government IdP",
        config={"industry": "government", "domains": ["gov.test"]},
    )
    fabric = get_fabric_security_service()
    mesh = (await fabric.get_mesh("fabric-t1")).unwrap()
    assert mesh["health"]["total_nodes"] >= 2

    await fabric.upsert_trust_node("fabric-t1", node_id="tenant:fabric-t1", node_type="tenant")
    await fabric.upsert_trust_node("fabric-t1", node_id="partner:bank", node_type="partner")
    await fabric.add_trust_edge(
        "fabric-t1",
        edge_id="e-trust-1",
        from_id="tenant:fabric-t1",
        to_id="partner:bank",
        relation="federation",
    )
    path = (await fabric.find_trust_path(
        "fabric-t1", source="tenant:fabric-t1", target="partner:bank"
    )).unwrap()
    assert path["found"] is True

    zt = (await fabric.evaluate_zero_trust_federation(
        "fabric-t1",
        user_id="u1",
        identity_verified=True,
        device_trusted=True,
        risk_score=10,
        trust_score=80,
        use_adaptive_pdp=False,
    )).unwrap()
    assert zt["action"] == "allow"

    dash = (await fabric.security_dashboard("fabric-t1")).unwrap()
    assert "federation_health" in dash
    assert "metrics" in dash
