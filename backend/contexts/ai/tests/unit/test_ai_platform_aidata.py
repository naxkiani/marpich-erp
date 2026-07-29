"""P214-K Enterprise AI Data Intelligence / Feature Engineering foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aidata_foundation import (
    validate_ai_aidata_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aidata as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aidata_foundation():
    result = validate_ai_aidata_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-K"
    assert result["adr"] == 431
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aidata_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-K"
    assert cat["adr"] == 431
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "governed" in cat["principle"]
    assert "reusable AI assets" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 8
    assert cat["enterprise_ai_data_platform_present_required"] is True
    assert cat["feature_store_platform_present_required"] is True
    assert cat["synthetic_data_platform_present_required"] is True
    assert cat["ai_data_lineage_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["feature_store"]["via_p214_d"] is True
    assert cat["synthetic"]["via_p214_h"] is True
    assert cat["lineage"]["via_p212_k"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_data_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aidata" in mod.aidata_surface()["routes"]
    assert "GET /ai/aidata/feature-store" in mod.aidata_surface()["routes"]
    assert "GET /ai/aidata/marketplace" in mod.aidata_surface()["routes"]


@pytest.mark.unit
def test_ai_aidata_acl():
    from contexts.ai.infrastructure.acl import ai_aidata_acl as acls

    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_metadata(tenant_id="t1", lineage_ref="l1")[
        "via_p212_k"
    ] is True
    assert acls.to_mlops(tenant_id="t1", model_ref="m1")[
        "via_p214_d"
    ] is True
    assert acls.to_governance(tenant_id="t1", policy_ref="p1")[
        "via_p214_h"
    ] is True
    assert acls.to_aisec(tenant_id="t1", security_ref="sec1")[
        "via_p214_i"
    ] is True
    assert acls.to_aiops(tenant_id="t1", pipeline_ref="pipe1")[
        "via_p214_j"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", aidata_ref="ad1")[
        "module_local_feature_store_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aidata():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aidata"]["prompt_id"] == "P214-K"
    assert catalog["platform_aidata"]["adr"] == 431
    assert catalog["platform_aidata"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aidata"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aidata()
    assert summary["prompt_id"] == "P214-K"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-J" in summary["builds_on"]
    assert summary["context_count"] >= 8
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aidata_readiness()["passed"] is True
    assert svc.aidata_feature_store()["via_p214_d"] is True
    assert svc.aidata_synthetic()["via_p214_h"] is True
    assert svc.aidata_lineage()["via_p212_k"] is True
    assert svc.aidata_marketplace()["present_required"] is True
