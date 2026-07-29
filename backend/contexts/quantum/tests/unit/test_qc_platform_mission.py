"""P215-B quantum mission foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.quantum.application.qc_mission_foundation import validate_qc_mission_foundation
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_mission as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service(); yield; reset_quantum_service()
@pytest.mark.unit
def test_qc_mission_foundation():
    result = validate_qc_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P215-B"
    assert result["adr"] == 448
    assert result["sor"] == "quantum"
@pytest.mark.unit
def test_qc_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P215-B"
    assert cat["quantum_mission_framework_present_required"] is True
    assert cat["governance_strategy"]["via_p215_k"] is True
    assert cat["governance_strategy"]["via_p214_y"] is True
    assert cat["builds_on_p215_a"] is True
    assert "GET /quantum/mission" in mod.mission_surface()["routes"]
@pytest.mark.unit
def test_qc_mission_acl():
    from contexts.quantum.infrastructure.acl import qc_mission_acl as acls
    assert acls.to_foundation(tenant_id="t1", foundation_ref="f1")["via_p215_a"] is True
    assert acls.to_ultimate_governance(tenant_id="t1", trust_ref="y1")["via_p214_y"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", mission_ref="m1")["module_local_quantum_mission_forbidden"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_quantum_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_mission"]["prompt_id"] == "P215-B"; assert svc.mission_readiness()["passed"] is True
