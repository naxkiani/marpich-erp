"""P214-P Continuous AI Trust / Compliance / Audit foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.ai.application.ai_aitrust_foundation import (
    validate_ai_aitrust_foundation,
)
from contexts.ai.container import get_ai_service, reset_ai_service
from contexts.ai.domain.services import ai_platform_aitrust as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_ai_service()
    yield
    reset_ai_service()


@pytest.mark.unit
def test_ai_aitrust_foundation():
    result = validate_ai_aitrust_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P214-P"
    assert result["adr"] == 436
    assert result["sor"] == "ai"
    assert result["capability"] == "CAP-PLT-AI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ai_aitrust_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P214-P"
    assert cat["adr"] == 436
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "continuous intelligent trust management" in cat["principle"]
    assert cat["domain_model"]["core_domain"] == mod.CORE_DOMAIN
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["enterprise_ai_governance_platform_present_required"] is True
    assert cat["ai_trust_platform_present_required"] is True
    assert cat["ai_audit_platform_present_required"] is True
    assert cat["certification_platform_present_required"] is True
    assert cat["sibling_ai_bc_forbidden"] is True
    assert cat["deepens_p214_h_continuous_trust"] is True
    assert cat["policies"]["via_p214_h"] is True
    assert cat["audit"]["via_audit_platform"] is True
    assert cat["trust"]["via_p214_o"] is True
    assert cat["explainability"]["via_p214_l"] is True
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_ai_governance_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P214-O" in cat["builds_on"]
    assert "P214-H" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /ai/aitrust" in mod.aitrust_surface()["routes"]
    assert "GET /ai/aitrust/trust" in mod.aitrust_surface()["routes"]
    assert "GET /ai/aitrust/audit" in mod.aitrust_surface()["routes"]


@pytest.mark.unit
def test_ai_aitrust_acl():
    from contexts.ai.infrastructure.acl import ai_aitrust_acl as acls

    assert acls.to_governance(tenant_id="t1", policy_ref="p1")[
        "via_p214_h"
    ] is True
    assert acls.to_audit_platform(tenant_id="t1", entry_ref="e1")[
        "via_audit_platform"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="pol1")[
        "via_policy_engine"
    ] is True
    assert acls.to_aiqa(tenant_id="t1", qa_ref="q1")[
        "via_p214_o"
    ] is True
    assert acls.to_modelintel(tenant_id="t1", model_ref="m1")[
        "via_p214_l"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_p211"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", trust_ref="tr1")[
        "module_local_ai_governance_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_aitrust():
    svc = get_ai_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_aitrust"]["prompt_id"] == "P214-P"
    assert catalog["platform_aitrust"]["adr"] == 436
    assert catalog["platform_aitrust"]["principle"] == mod.PRINCIPLE
    assert catalog["platform_aitrust"]["fabric"] == mod.FABRIC
    assert catalog["sor"] == "ai"
    summary = svc.platform_aitrust()
    assert summary["prompt_id"] == "P214-P"
    assert summary["fabric"] == mod.FABRIC
    assert "P214-O" in summary["builds_on"]
    assert "P214-H" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["microservice_count"] >= 10
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.aitrust_readiness()["passed"] is True
    assert svc.aitrust_policies()["via_p214_h"] is True
    assert svc.aitrust_audit()["via_audit_platform"] is True
    assert svc.aitrust_trust()["via_p214_o"] is True
    assert svc.aitrust_explainability()["via_p214_l"] is True
    assert svc.aitrust_digital_twin()["present_required"] is True
