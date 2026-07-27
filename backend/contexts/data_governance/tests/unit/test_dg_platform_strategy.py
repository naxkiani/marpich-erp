"""P212-A Data Governance strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_strategy_foundation import (
    validate_dg_strategy_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import (
    dg_platform_strategy as strat,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_strategy_foundation():
    result = validate_dg_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-A"
    assert result["adr"] == 392
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["forbidden_sibling_present"] is False
    assert result["registry"] is True
    assert result["startup"] is True


@pytest.mark.unit
def test_dg_strategy_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P212-A"
    assert cat["adr"] == 392
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["governance_architecture_complete_required"] is True
    assert cat["data_mesh_native_required"] is True
    assert cat["ai_native_governance_present_required"] is True
    assert cat["privacy_by_design_present_required"] is True
    assert cat["architecture"]["layer_count"] >= 6
    assert cat["microservices"]["service_count"] >= 11
    assert cat["cursor_outputs"]["count"] >= 16
    assert (
        "enterprise_data_governance_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-governance/strategy" in strat.strategy_surface()["routes"]
    assert (
        "GET /data-governance/strategy/readiness"
        in strat.strategy_surface()["routes"]
    )


@pytest.mark.unit
def test_dg_strategy_acl():
    from contexts.data_governance.infrastructure.acl import (
        dg_strategy_acl as acls,
    )

    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "via_data_security_p211"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["zero_trust_alignment_present_required"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")["via_p209"] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="sig1")[
        "via_p210"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P212-A"
    assert catalog["platform_strategy"]["adr"] == 392
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_strategy()
    assert summary["prompt_id"] == "P212-A"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "ADR-376" in summary["builds_on"]
    assert "P212-B" in summary["follow_up_modules"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
