"""P210-N Cyber Security Deploy / DevSecOps foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_deploy_foundation import (
    validate_cs_deploy_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_deploy as deploy

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_deploy_foundation():
    result = validate_cs_deploy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-N"
    assert result["adr"] == 374
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_deploy_catalog():
    cat = deploy.catalog()
    assert cat["prompt_id"] == "P210-N"
    assert cat["adr"] == 374
    assert cat["deployment_automated_required"] is True
    assert cat["kubernetes_security_complete_required"] is True
    assert cat["observability_required"] is True
    assert cat["auto_scaling_required"] is True
    assert cat["disaster_recovery_defined_required"] is True
    assert cat["pipeline_validation_required"] is True
    assert cat["module_local_observability_stack_forbidden"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "deployment_is_not_automated" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/deploy" in deploy.deploy_surface()["routes"]
    assert "GET /cyber-security/deploy/readiness" in deploy.deploy_surface()["routes"]


@pytest.mark.unit
def test_cs_deploy_acl():
    from contexts.cyber_security.infrastructure.acl import cs_deploy_acl as acls

    assert acls.to_enterprise_observability(tenant_id="t1", service_ref="s1")[
        "module_local_observability_stack_forbidden"
    ] is True
    assert acls.to_p209_secrets(tenant_id="t1", secret_ref="sec1")[
        "via_p209"
    ] is True
    assert acls.to_workflow_promotion(tenant_id="t1", env_ref="prod")[
        "deployment_approval_required"
    ] is True
    assert acls.to_siem(tenant_id="t1", event_ref="e1")[
        "security_controls_integrated_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_deploy():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_deploy"]["prompt_id"] == "P210-N"
    assert catalog["platform_deploy"]["adr"] == 374
    summary = svc.platform_deploy()
    assert summary["prompt_id"] == "P210-N"
    assert "P210-M" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
