"""P211-K Data Security intelligence graph foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_intelligence_foundation import (
    validate_ds_intelligence_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import (
    ds_platform_intelligence as intel,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_intelligence_foundation():
    result = validate_ds_intelligence_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-K"
    assert result["adr"] == 386
    assert result["sor"] == "data_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_ds_intelligence_catalog():
    cat = intel.catalog()
    assert cat["prompt_id"] == "P211-K"
    assert cat["adr"] == 386
    assert cat["data_origin_known_required"] is True
    assert cat["data_movement_visible_required"] is True
    assert cat["metadata_complete_required"] is True
    assert cat["relationships_queryable_required"] is True
    assert cat["impact_analysis_available_required"] is True
    assert cat["ai_reasoning_over_context_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["domain"]["context_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 15
    assert "data_origin_is_unknown" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/intelligence" in intel.intelligence_surface()["routes"]
    assert (
        "GET /data-security/intelligence/readiness"
        in intel.intelligence_surface()["routes"]
    )


@pytest.mark.unit
def test_ds_intelligence_acl():
    from contexts.data_security.infrastructure.acl import (
        ds_intelligence_acl as acls,
    )

    assert acls.to_discovery(tenant_id="t1", asset_ref="a1")[
        "data_origin_known_required"
    ] is True
    assert acls.to_enterprise_search(tenant_id="t1", query_ref="q1")[
        "module_local_search_forbidden"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "ai_reasoning_over_context_required"
    ] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")[
        "impact_analysis_available_required"
    ] is True
    assert acls.to_protection(tenant_id="t1", asset_ref="p1")[
        "via_p211_j_protection"
    ] is True
    assert acls.to_dlp(tenant_id="t1", policy_ref="d1")[
        "data_movement_visible_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_intelligence():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_intelligence"]["prompt_id"] == "P211-K"
    assert catalog["platform_intelligence"]["adr"] == 386
    summary = svc.platform_intelligence()
    assert summary["prompt_id"] == "P211-K"
    assert "P211-J" in summary["builds_on"]
    assert summary["context_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
