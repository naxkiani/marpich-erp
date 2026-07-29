"""P211-A Data Security strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_security.application.ds_strategy_foundation import (
    validate_ds_strategy_foundation,
)
from contexts.data_security.container import (
    get_data_security_service,
    reset_data_security_service,
)
from contexts.data_security.domain.services import ds_platform_strategy as strat

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_security_service()
    yield
    reset_data_security_service()


@pytest.mark.unit
def test_ds_strategy_foundation():
    result = validate_ds_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P211-A"
    assert result["adr"] == 376
    assert result["sor"] == "data_security"
    assert result["capability"] == "CAP-PLT-DS-001"
    assert result["forbidden_sibling_present"] is False
    assert result["registry"] is True
    assert result["startup"] is True


@pytest.mark.unit
def test_ds_strategy_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P211-A"
    assert cat["adr"] == 376
    assert cat["sor"] == "data_security"
    assert cat["capability"] == "CAP-PLT-DS-001"
    assert cat["data_assets_discoverable_required"] is True
    assert cat["sensitive_data_classifiable_required"] is True
    assert cat["privacy_risks_measurable_required"] is True
    assert cat["data_access_governed_required"] is True
    assert cat["ai_data_protected_required"] is True
    assert cat["data_lineage_available_required"] is True
    assert cat["compliance_evidence_generatable_required"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["inventory"]["asset_count"] >= 10
    assert cat["cursor_outputs"]["count"] >= 20
    assert "data_assets_cannot_be_discovered" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /data-security/strategy" in strat.strategy_surface()["routes"]
    assert "GET /data-security/strategy/readiness" in strat.strategy_surface()["routes"]


@pytest.mark.unit
def test_ds_strategy_acl():
    from contexts.data_security.infrastructure.acl import ds_strategy_acl as acls

    assert acls.to_consent(tenant_id="t1", subject_ref="s1")[
        "consent_ledger_owned_by_consent"
    ] is True
    assert acls.to_secrets(tenant_id="t1", key_ref="k1")[
        "crypto_owned_by_secrets"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["data_access_governed_required"] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="sig1")[
        "threat_defense_owned_by_cyber_security"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_data_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P211-A"
    assert catalog["platform_strategy"]["adr"] == 376
    assert catalog["sor"] == "data_security"
    summary = svc.platform_strategy()
    assert summary["prompt_id"] == "P211-A"
    assert summary["capability"] == "CAP-PLT-DS-001"
    assert "ADR-361" in summary["builds_on"]
    assert "P211-O" in summary["follow_up_modules"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
