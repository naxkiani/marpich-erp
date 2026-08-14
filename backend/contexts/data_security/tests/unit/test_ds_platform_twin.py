"""P211-M Data Security digital twin & privacy simulation foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_twin_foundation import (
    validate_ds_twin_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_twin as twin,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_twin_foundation():
    result = validate_ds_twin_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-M"
    assert result["adr"] == 388
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_twin_catalog():
    cat = twin.catalog()
    assert cat["prompt_id"] == "P211-M"
    assert cat["adr"] == 388
    assert cat["digital_representation_complete_required"] is True
    assert cat["privacy_scenarios_simulatable_required"] is True
    assert cat["risk_prediction_available_required"] is True
    assert cat["compliance_impact_measurable_required"] is True
    assert cat["ai_privacy_risks_visible_required"] is True
    assert cat["simulation_results_explainable_required"] is True
    assert cat["architecture"]["layer_count"] >= 7
    assert cat["domain"]["context_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 15
    assert (
        "digital_representation_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/twin" in twin.twin_surface()["routes"]
    assert "GET /data-security/twin/readiness" in twin.twin_surface()["routes"]


@pytest.mark.unit
def test_ds_twin_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_twin_acl as acls,
    )

    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "simulation_results_explainable_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_discovery(tenant_id="t1", asset_ref="a1")[
        "digital_representation_complete_required"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "privacy_scenarios_simulatable_required"
    ] is True
    assert acls.to_consent(tenant_id="t1", processing_ref="pr1")[
        "via_consent_acl_only"
    ] is True
    assert acls.to_ai_security(tenant_id="t1", decision_ref="d1")[
        "ai_privacy_risks_visible_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_twin():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_twin"]["prompt_id"] == "P211-M"
    assert catalog["platform_twin"]["adr"] == 388
    summary = svc.platform_twin()
    assert summary["prompt_id"] == "P211-M"
    assert "P211-L" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
