"""P210-M Cyber Security AI Governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_gov_foundation import (
    validate_cs_gov_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_gov as gov

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_gov_foundation():
    result = validate_cs_gov_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-M"
    assert result["adr"] == 373
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_gov_catalog():
    cat = gov.catalog()
    assert cat["prompt_id"] == "P210-M"
    assert cat["adr"] == 373
    assert cat["ai_models_inventoried_required"] is True
    assert cat["human_oversight_required"] is True
    assert cat["policies_enforceable_required"] is True
    assert cat["module_local_llm_sdk_forbidden"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["inventory"]["asset_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "ai_models_cannot_be_inventoried" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/gov" in gov.gov_surface()["routes"]
    assert "GET /cyber-security/gov/readiness" in gov.gov_surface()["routes"]


@pytest.mark.unit
def test_cs_gov_acl():
    from contexts.cyber_security.infrastructure.acl import cs_gov_acl as acls

    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "policies_enforceable_required"
    ] is True
    assert acls.to_workflow_oversight(tenant_id="t1", gate_ref="g1")[
        "human_oversight_required"
    ] is True
    assert acls.to_compliance(tenant_id="t1", evidence_ref="e1")[
        "compliance_evidence_generatable_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_gov():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_gov"]["prompt_id"] == "P210-M"
    assert catalog["platform_gov"]["adr"] == 373
    summary = svc.platform_gov()
    assert summary["prompt_id"] == "P210-M"
    assert "P210-L" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
