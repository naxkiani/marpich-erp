"""P211-O Data Security deploy/DevSecOps foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_deploy_foundation import (
    validate_ds_deploy_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_deploy as deploy,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_deploy_foundation():
    result = validate_ds_deploy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-O"
    assert result["adr"] == 390
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_deploy_catalog():
    cat = deploy.catalog()
    assert cat["prompt_id"] == "P211-O"
    assert cat["adr"] == 390
    assert cat["deployment_automated_required"] is True
    assert cat["security_scanning_present_required"] is True
    assert cat["infrastructure_scalable_required"] is True
    assert cat["monitoring_complete_required"] is True
    assert cat["disaster_recovery_defined_required"] is True
    assert cat["runtime_security_present_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["kubernetes"]["cluster_count"] >= 4
    assert cat["cursor_outputs"]["count"] >= 16
    assert "deployment_is_manual" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/deploy" in deploy.deploy_surface()["routes"]
    assert (
        "GET /data-security/deploy/readiness"
        in deploy.deploy_surface()["routes"]
    )


@pytest.mark.unit
def test_ds_deploy_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_deploy_acl as acls,
    )

    assert acls.to_observability(tenant_id="t1", service_ref="s1")[
        "monitoring_complete_required"
    ] is True
    assert acls.to_secrets_signing(tenant_id="t1", image_ref="img1")[
        "security_scanning_present_required"
    ] is True
    assert acls.to_gitops(tenant_id="t1", env_ref="prod")[
        "deployment_automated_required"
    ] is True
    assert acls.to_dr(tenant_id="t1", plan_ref="dr1")[
        "disaster_recovery_defined_required"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="sig1")[
        "via_p210_siem"
    ] is True
    assert acls.to_ops(tenant_id="t1", fabric_ref="f1")[
        "infrastructure_scalable_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_deploy():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_deploy"]["prompt_id"] == "P211-O"
    assert catalog["platform_deploy"]["adr"] == 390
    summary = svc.platform_deploy()
    assert summary["prompt_id"] == "P211-O"
    assert "P211-N" in summary["builds_on"]
    assert summary["cluster_count"] >= 4
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
