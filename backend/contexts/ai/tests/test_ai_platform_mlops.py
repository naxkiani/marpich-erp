"""P214-D Enterprise MLOps foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_mlops_foundation import (
    validate_ai_mlops_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_mlops as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_mlops_foundation():
    result = validate_ai_mlops_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-D"
    assert result["adr"] == 424
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_mlops_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-D"
    assert cat["adr"] == 424
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "isolated experiments" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["lifecycle"]["stage_count"] >= 13
    assert cat["enterprise_mlops_platform_present_required"] is True
    assert cat["feature_store_present_required"] is True
    assert cat["model_registry_present_required"] is True
    assert cat["continuous_training_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["feature_store"]["via_p212"] is True
    assert cat["deployment"]["via_p213_o"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["pipelines"]["pipeline_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_mlops_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-C" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/mlops" in mod.mlops_surface()["routes"]
    assert "GET /ai/mlops/features" in mod.mlops_surface()["routes"]
    assert "GET /ai/mlops/continuous-training" in mod.mlops_surface()["routes"]


@pytest.mark.unit
def test_ai_mlops_acl():
    from contexts.ai.infrastructure.acl import ai_mlops_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_predictive(tenant_id="t1", forecast_ref="f1")[
        "via_p213_j"
    ] is True
    assert acls.to_ops_deploy(tenant_id="t1", release_ref="r1")[
        "via_p213_o"
    ] is True
    assert acls.to_foundation(tenant_id="t1", profile_ref="pf1")[
        "via_p214_a"
    ] is True
    assert acls.to_domain(tenant_id="t1", context_ref="c1")[
        "via_p214_c"
    ] is True
    assert acls.to_cryptographic_trust(tenant_id="t1", secret_ref="s1")[
        "model_signing"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mlops():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mlops"]["prompt_id"] == "P214-D"
    assert catalog["platform_mlops"]["adr"] == 424
    assert catalog["platform_mlops"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_mlops"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_mlops()
    assert summary["prompt_id"] == "P214-D"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-C" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["lifecycle_stage_count"] >= 13
    assert summary["microservice_count"] >= 10
    assert summary["pipeline_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.mlops_readiness()["passed"] is True
    assert svc.mlops_features()["via_p212"] is True
    assert svc.mlops_registry()["present_required"] is True
    assert svc.mlops_continuous_training()["present_required"] is True
