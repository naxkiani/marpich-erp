"""P215-Z quantum supreme intelligence / master control foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_supreme_foundation import validate_qc_supreme_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_supreme as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_supreme_foundation():
    result = validate_qc_supreme_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-Z"
    assert result["adr"] == 471
    assert result["series_status"] == "P215_COMPLETE"
@pytest.mark.unit
def test_qc_supreme_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-Z"
    assert cat["fabric"] == "meos_quantum_supreme_intelligence_fabric"
    assert cat["series_status"] == "P215_COMPLETE"
    assert cat["ultimate_trust_gate"] == "P215-Y"
    assert cat["future_gate"] == "P215-X"
    assert cat["civilization_gate"] == "P215-W"
    assert cat["qgi_gate"] == "P215-V"
    assert cat["evolution_gate"] == "P215-U"
    assert cat["os_gate"] == "P215-T"
    assert cat["trust_gate"] == "P215-K"
    assert cat["quantum_master_intelligence_architecture_present_required"] is True
    assert cat["supreme_control_plane_present_required"] is True
    assert cat["enterprise_quantum_brain_present_required"] is True
    assert cat["autonomous_intelligence_nexus_present_required"] is True
    assert cat["intelligence_federation_present_required"] is True
    assert cat["evolution_intelligence_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["aggregates"]["aggregate_count"] >= 7
    assert cat["never_replace_core_platform"] is True
    assert cat["never_replace_p215_t"] is True
    assert cat["never_replace_p215_y"] is True
    assert cat["ungated_supreme_autonomy_forbidden"] is True
    assert cat["opaque_master_decisions_forbidden"] is True
    assert cat["via_p214_z"] is True
    assert cat["next_series"] == "P216"
    assert "GET /quantum/supreme" in mod.supreme_surface()["routes"]
@pytest.mark.unit
def test_qc_supreme_acl():
    from contexts.quantum.infrastructure.acl import qc_supreme_acl as acls
    assert acls.to_quantum_ultimate_trust(tenant_id="t1", ultimate_trust_ref="y1")["never_replace_p215_y"] is True
    assert acls.to_quantum_os(tenant_id="t1", os_ref="t1")["never_replace_p215_t"] is True
    assert acls.to_quantum_governance(tenant_id="t1", governance_ref="k1")["never_replace_p215_k"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["ungated_supreme_autonomy_forbidden"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["opaque_master_decisions_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_supreme():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_supreme"]["prompt_id"] == "P215-Z"; assert svc.supreme_readiness()["passed"] is True
