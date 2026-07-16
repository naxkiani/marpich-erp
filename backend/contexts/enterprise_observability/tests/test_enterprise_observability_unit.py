"""Enterprise Observability — unit tests."""
import pytest

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import ObservabilityCapability
from contexts.enterprise_observability.domain.services import enterprise_observability_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_fourteen_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert ObservabilityCapability.DISTRIBUTED_TRACING.value in caps
    assert ObservabilityCapability.OPERATIONAL_DASHBOARD.value in caps
    assert ObservabilityCapability.SERVICE_DEPENDENCY_GRAPH.value in caps
    assert len(caps) == 14


@pytest.mark.unit
def test_policy_keys_defined():
    assert "enterprise_observability.tracing.enabled" in engine.list_policy_keys()
    assert "enterprise_observability.alerting.enabled" in engine.list_policy_keys()


@pytest.mark.unit
def test_dependency_map_includes_observability():
    graph = engine.dependency_map()
    node_ids = {n["id"] for n in graph["nodes"]}
    assert "enterprise_observability" in node_ids
    assert "analytics" in node_ids


@pytest.mark.unit
def test_service_dependency_graph_from_registry():
    graph = engine.build_service_dependency_graph()
    assert graph["total_services"] >= 1
    assert graph["graph_type"] == "service_dependency"
    assert len(graph["nodes"]) >= 1
    assert isinstance(graph["edges"], list)
    node_ids = {n["id"] for n in graph["nodes"]}
    assert "enterprise_observability" in node_ids or len(node_ids) >= 1
    for edge in graph["edges"]:
        assert "from" in edge and "to" in edge and "type" in edge


@pytest.mark.unit
def test_alert_evaluation():
    assert engine.evaluate_alert(value=350, operator="gt", threshold=300) is True
    assert engine.evaluate_alert(value=100, operator="gt", threshold=300) is False


@pytest.mark.unit
def test_operational_dashboard_structure():
    seed = engine.generate_seed_data()
    dashboard = engine.build_operational_dashboard(
        profile=None,
        health_checks=seed["health_checks"],
        metrics=seed["metrics"],
        logs=seed["logs"],
        traces=seed["traces"],
        alerts=seed["alerts"],
        incidents=[],
    )
    assert dashboard["dashboard_id"] == "platform.system-health"
    assert "summary" in dashboard
    assert dashboard["summary"]["capabilities"] == 14
    assert len(dashboard["rows"]) >= 3
