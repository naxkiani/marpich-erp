"""P341 infrastructure readiness must not invent production or close G26 without evidence."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_PRODUCTION_INFRASTRUCTURE_READINESS.v1.yaml"
P340 = EXEC / "MEOS_G26_EXECUTION_ENABLEMENT.v1.yaml"
P313 = EXEC / "MEOS_P313_PRODUCTION_CERTIFICATION.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
CONTEXTS = REPO / "backend" / "contexts"


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_outcome_b_not_certified_p0_one():
    data = _overlay()
    assert data["outcome"] == "OUTCOME_B"
    assert data["overall_status"] == "BLOCKED"
    assert data["production_certified"] is False
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_ready"] is False
    assert data["p0_count"] == 1
    assert data["production_smoke"] == "NOT_EXECUTED"
    assert data["go_live_declaration"] == "FORBIDDEN"
    assert data["bind_hold_decisions"] == "FORBIDDEN"
    assert data["new_cloud_abstraction"] == "FORBIDDEN"
    assert data["new_observability_platform"] == "FORBIDDEN"
    assert data["new_secrets_platform"] == "FORBIDDEN"
    assert data["new_deployment_engine"] == "FORBIDDEN"


def test_does_not_classify_compose_or_localhost_as_production():
    data = _overlay()
    target = data["production_target"]
    assert target["status"] == "NOT_AVAILABLE"
    assert target["cloud_cluster"] == "MISSING"
    assert target["meosprod_compose_profile"] == "EXISTS"
    assert target["meosprod_runtime"] == "STOPPED"
    assert COMPOSE.is_file()
    text = COMPOSE.read_text(encoding="utf-8")
    assert "Not a cloud production cluster" in text or "not a cloud" in text.lower()
    assert data["runtime_status"] == "BLOCKED"
    assert data["deployment_status"] == "BLOCKED"
    assert data["tls"] == "MISSING"
    assert data["secrets"] == "BLOCKED"
    assert "dirty" in str(data["git_describe"])
    assert data["immutable_sha"] == "BLOCKED"


def test_critical_gates_not_downgraded():
    data = _overlay()
    gates = data["gates_reevaluated"]
    assert gates["G26"] == "BLOCKED"
    assert gates["G27"] == "BLOCKED"
    assert gates["G25"] == "FAIL"
    assert gates["G23"] == "FAIL"
    assert gates["G19"] == "FAIL"
    assert gates["G18"] == "FAIL"
    p340 = yaml.safe_load(P340.read_text(encoding="utf-8"))
    assert p340["g26"]["status"] == "BLOCKED"
    assert p340["observability"]["g23"] == "FAIL"
    matrix = P313.read_text(encoding="utf-8")
    assert "G26 | DEPLOYMENT | **BLOCKED**" in matrix
    assert "G23 | OBSERVABILITY | **FAIL**" in matrix
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "PRODUCTION_CERTIFIED" in checklist
    assert "| 14 | PRODUCTION_CERTIFIED | **BLOCKED**" in checklist or "PRODUCTION_CERTIFIED | **NO**" in checklist
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist


def test_blockers_have_owner_and_required_action():
    data = _overlay()
    ids = {row["id"] for row in data["blockers"]}
    assert {"BLK-G26", "BLK-G25", "BLK-G27", "G23", "G19", "G18"} <= ids
    for row in data["blockers"]:
        assert row["status"] in {"BLOCKED", "FAIL"}
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["required_action"]
        assert row["missing"]
    assert data["workflow_binding"] == "NOT_AVAILABLE"
    assert data["alerting"] == "FAIL"
    assert data["rollback"] == "BLOCKED"
    assert not (CONTEXTS / "pmo").exists()
    assert "Provision a real production cluster" in data["next_operational_action"]
