"""P211-P Data Security QA/governance/DoD foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_qa_foundation import (
    validate_ds_qa_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_qa as qa,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_qa_foundation():
    result = validate_ds_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-P"
    assert result["adr"] == 391
    assert result["sor"] == "data_security"
    assert result["series_finalizes_p211"] is True
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_qa_catalog():
    cat = qa.catalog()
    assert cat["prompt_id"] == "P211-P"
    assert cat["adr"] == 391
    assert cat["testing_automated_required"] is True
    assert cat["compliance_evidence_available_required"] is True
    assert cat["security_validation_present_required"] is True
    assert cat["governance_ownership_clear_required"] is True
    assert cat["risks_trackable_required"] is True
    assert cat["production_readiness_defined_required"] is True
    assert cat["series_finalizes_p211"] is True
    assert cat["architecture"]["layer_count"] >= 6
    assert cat["domain"]["context_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 16
    assert "testing_is_manual_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/qa" in qa.qa_surface()["routes"]
    assert "GET /data-security/qa/readiness" in qa.qa_surface()["routes"]


@pytest.mark.unit
def test_ds_qa_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_qa_acl as acls,
    )

    assert acls.to_audit(tenant_id="t1", evidence_ref="e1")[
        "compliance_evidence_available_required"
    ] is True
    assert acls.to_devsecops(tenant_id="t1", pipeline_ref="p1")[
        "testing_automated_required"
    ] is True
    assert acls.to_governance(tenant_id="t1", control_ref="c1")[
        "governance_ownership_clear_required"
    ] is True
    assert acls.to_risk(tenant_id="t1", risk_ref="r1")[
        "risks_trackable_required"
    ] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")[
        "production_readiness_defined_required"
    ] is True
    assert acls.to_consent(tenant_id="t1", processing_ref="pr1")[
        "via_consent_acl_only"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P211-P"
    assert catalog["platform_qa"]["adr"] == 391
    assert catalog["platform_qa"]["series_finalizes_p211"] is True
    summary = svc.platform_qa()
    assert summary["prompt_id"] == "P211-P"
    assert "P211-O" in summary["builds_on"]
    assert summary["series_finalizes_p211"] is True
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
