"""P212-N Data Governance deploy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_deploy_foundation import (
    validate_dg_deploy_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_deploy as deploy,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_deploy_foundation():
    result = validate_dg_deploy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-N"
    assert result["adr"] == 406
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_deploy_catalog():
    cat = deploy.catalog()
    assert cat["prompt_id"] == "P212-N"
    assert cat["adr"] == 406
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["cloud_native_deployment_architecture_present_required"] is True
    assert cat["kubernetes_platform_architecture_present_required"] is True
    assert cat["devsecops_platform_present_required"] is True
    assert cat["gitops_architecture_present_required"] is True
    assert cat["infrastructure_as_code_present_required"] is True
    assert cat["service_mesh_architecture_present_required"] is True
    assert cat["scalability_architecture_present_required"] is True
    assert cat["high_availability_architecture_present_required"] is True
    assert cat["observability_platform_present_required"] is True
    assert cat["aiops_operations_present_required"] is True
    assert cat["security_integration_present_required"] is True
    assert cat["multi_region_architecture_present_required"] is True
    assert cat["cqrs_operational_integration_present_required"] is True
    assert cat["enterprise_reliability_present_required"] is True
    assert cat["cloud_native"]["layer_count"] >= 6
    assert cat["devsecops"]["pipeline_stage_count"] >= 10
    assert cat["aiops"]["agent_count"] >= 5
    assert cat["cqrs_operational_integration"]["event_count"] >= 5
    assert cat["cursor_outputs"]["count"] >= 20
    assert cat["observability"]["via_platform_observability"] is True
    assert cat["cqrs_operational_integration"]["via_p212_m"] is True
    assert cat["api_first"]["via_api_gateway"] is True
    assert (
        "cloud_native_deployment_architecture_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/deploy" in deploy.deploy_surface()["routes"]
    assert (
        "GET /data-governance/deploy/readiness"
        in deploy.deploy_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_deploy_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_deploy_acl as acls,
    )

    assert acls.to_observability(tenant_id="t1", signal_ref="s1")[
        "via_platform_observability"
    ] is True
    assert acls.to_event_bus(tenant_id="t1", topic_ref="t1")[
        "via_enterprise_event_bus"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "via_api_gateway"
    ] is True
    assert acls.to_ops(tenant_id="t1", ops_ref="o1")["via_p212_m"] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="deploy"
    )["via_p208"] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")["via_p209"] is True
    assert acls.to_cyber_security(tenant_id="t1", posture_ref="p1")[
        "via_p210"
    ] is True
    assert acls.to_data_security(tenant_id="t1", classification_ref="c1")[
        "via_p211"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_deploy():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_deploy"]["prompt_id"] == "P212-N"
    assert catalog["platform_deploy"]["adr"] == 406
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_deploy()
    assert summary["prompt_id"] == "P212-N"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-M" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.deploy_readiness()["passed"] is True
