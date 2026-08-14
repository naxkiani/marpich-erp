"""P210-I Cyber Security ASM/CTEM foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_asm_foundation import (
    validate_cs_asm_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_asm as asm

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_asm_foundation():
    result = validate_cs_asm_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-I"
    assert result["adr"] == 369
    assert result["sor"] == "cyber_security"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_asm_catalog():
    cat = asm.catalog()
    assert cat["prompt_id"] == "P210-I"
    assert cat["adr"] == 369
    assert cat["asset_discovery_complete_required"] is True
    assert cat["ctem_lifecycle_continuous_required"] is True
    assert cat["attack_path_analysis_required"] is True
    assert cat["architecture"]["layer_count"] >= 10
    assert cat["asset_discovery"]["asset_type_count"] >= 20
    assert cat["cursor_outputs"]["count"] >= 20
    assert "asset_discovery_incomplete" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/asm" in asm.asm_surface()["routes"]
    assert "GET /cyber-security/asm/readiness" in asm.asm_surface()["routes"]


@pytest.mark.unit
def test_cs_asm_acl():
    from contexts.cyber_security.infrastructure.acl import cs_asm_acl as acls

    assert acls.to_soar_remediation(tenant_id="t1", playbook_ref="pb1")[
        "remediation_validated_required"
    ] is True
    assert acls.to_ai_explainable(tenant_id="t1", advisory_ref="a1")[
        "business_context_required"
    ] is True
    assert acls.to_threat_intel(tenant_id="t1", vuln_ref="v1")[
        "via_p210_h_intel"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_asm():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_asm"]["prompt_id"] == "P210-I"
    assert catalog["platform_asm"]["adr"] == 369
    summary = svc.platform_asm()
    assert summary["prompt_id"] == "P210-I"
    assert "P210-H" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
