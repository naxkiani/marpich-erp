"""P213-O BI deploy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_deploy_foundation import (
    validate_bi_deploy_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_deploy as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_deploy_foundation():
    result = validate_bi_deploy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-O"
    assert result["adr"] == 419
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_deploy_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-O"
    assert cat["adr"] == 419
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "secure GitOps" in cat["principle"]
    assert cat["enterprise_production_deployment_present_required"] is True
    assert cat["kubernetes_runtime_present_required"] is True
    assert cat["gitops_platform_present_required"] is True
    assert cat["devsecops_pipeline_present_required"] is True
    assert cat["observability_platform_present_required"] is True
    assert cat["sre_processes_present_required"] is True
    assert cat["scalability_architecture_present_required"] is True
    assert cat["disaster_recovery_present_required"] is True
    assert cat["definition_of_done_present_required"] is True
    assert cat["cloud_native_deployment_present_required"] is True
    assert cat["zero_trust_security_present_required"] is True
    assert cat["continuous_governance_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_analytics_operational_excellence"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "BiOperationsPlatformAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["environments"]["environment_count"] >= 11
    assert cat["definition_of_done"]["criterion_count"] >= 23
    assert cat["aiops"]["agent_count"] >= 9
    assert cat["aiops"]["via_enterprise_ai"] is True
    assert cat["devsecops"]["via_p209"] is True
    assert cat["devsecops"]["via_p210"] is True
    assert cat["observability"]["via_enterprise_observability"] is True
    assert cat["cqrs"]["command_count"] >= 6
    assert cat["events"]["core_event_count"] >= 6
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "bi_deploy_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert (
        "definition_of_done_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-N" in cat["builds_on"]
    assert "P209" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/deploy" in mod.deploy_surface()["routes"]
    assert "GET /analytics/deploy/kubernetes" in mod.deploy_surface()["routes"]
    assert (
        "GET /analytics/deploy/definition-of-done"
        in mod.deploy_surface()["routes"]
    )


@pytest.mark.unit
def test_bi_deploy_acl():
    from contexts.analytics.infrastructure.acl import bi_deploy_acl as acls

    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="deploy.read"
    )["via_p208"] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", secret_ref="s1")[
        "image_signing_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", control_ref="c1")[
        "via_p210"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_ops(tenant_id="t1", service_ref="svc1")[
        "via_p213_n"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_observability(tenant_id="t1", signal_ref="sig1")[
        "via_enterprise_observability"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_deploy():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_deploy"]["prompt_id"] == "P213-O"
    assert catalog["platform_deploy"]["adr"] == 419
    assert catalog["platform_deploy"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_deploy"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "analytics"
    summary = svc.platform_deploy()
    assert summary["prompt_id"] == "P213-O"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-N" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["environment_count"] >= 11
    assert summary["definition_of_done_count"] >= 23
    assert summary["aiops_agent_count"] >= 9
    assert summary["microservice_count"] >= 8
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.deploy_readiness()["passed"] is True
    assert svc.deploy_kubernetes()["control_plane"] is True
    assert svc.deploy_gitops()["git_as_source_of_truth"] is True
    assert svc.deploy_devsecops()["via_p209"] is True
    assert svc.deploy_definition_of_done()["criterion_count"] >= 23
