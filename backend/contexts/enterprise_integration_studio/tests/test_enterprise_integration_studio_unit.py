"""Enterprise Integration Studio — unit tests."""
import pytest

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import StudioCapability
from contexts.enterprise_integration_studio.domain.services import enterprise_integration_studio_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_fourteen_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert StudioCapability.VISUAL_API_BUILDER.value in caps
    assert StudioCapability.DEVELOPER_PORTAL.value in caps
    assert StudioCapability.CITIZEN_DEVELOPER_WORKSPACE.value in caps
    assert len(caps) == 14


@pytest.mark.unit
def test_build_api_designer_graph_has_nodes():
    graph = engine.build_api_designer_graph(artifact={"name": "Payments API"})
    assert graph["name"] == "Payments API"
    assert len(graph["nodes"]) >= 4
    assert len(graph["edges"]) == len(graph["nodes"]) - 1


@pytest.mark.unit
def test_run_mock_test_passes_with_mock():
    result = engine.run_mock_test(artifact={"artifact_ref": "ART-1", "artifact_type": "api"}, use_mock=True)
    assert result["status"] == "passed"
    assert result["mock_used"] is True


@pytest.mark.unit
def test_build_dashboard_structure():
    projects = [{"workspace_type": "developer"}, {"workspace_type": "citizen"}]
    artifacts = [{"artifact_type": "api"}, {"artifact_type": "connector"}]
    dash = engine.build_dashboard(
        profile=None,
        projects=projects,
        artifacts=artifacts,
        versions=[],
        deployments=[{"status": "live"}],
        tests=[{"status": "passed", "created_at": "2026-01-01"}],
        marketplace=[{}],
    )
    assert dash["summary"]["capabilities"] == 14
    assert dash["summary"]["projects"] == 2
    assert dash["summary"]["deployments_live"] == 1
