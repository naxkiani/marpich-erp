"""P345 must not treat compose as production or close G26 without credentials."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P345_G26_PROVISIONING.v1.yaml"
P344 = EXEC / "MEOS_P344_GO_LIVE_EXECUTION.v1.yaml"
P341 = EXEC / "MEOS_PRODUCTION_INFRASTRUCTURE_READINESS.v1.yaml"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
HELM = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
ALLOWED_EV = frozenset(
    {"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE", "IMPLEMENTED_UNVERIFIED", "MISSING", "DESIGNED"}
)


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p344_stop_and_g26_still_blocked():
    p344 = yaml.safe_load(P344.read_text(encoding="utf-8"))
    p341 = yaml.safe_load(P341.read_text(encoding="utf-8"))
    data = _overlay()
    assert p344["outcome"] == "STOPPED"
    assert p344["deployment_executed"] is False
    assert data["p344_entry_gate"] == "STOPPED"
    assert data["outcome"] == "OUTCOME_B"
    assert data["g26_status"] == "BLOCKED"
    assert data["g26_ready_for_revalidation"] is False
    assert data["provisioning"] == "BLOCKED"
    assert data["credentials_required"] is True
    assert data["p0_count"] == 1
    assert p341["p0_count"] == 1
    assert p341["production_target"]["cloud_cluster"] == "MISSING"
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_authorization"] == "NOT APPROVED"
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["runtime_status"] == "NOT_LAUNCHED"
    assert "dirty" in str(data["git_describe"])
    assert data["immutable_release"] == "FORBIDDEN"


def test_compose_exists_but_is_not_production():
    data = _overlay()
    assert COMPOSE.is_file()
    text = COMPOSE.read_text(encoding="utf-8")
    assert "Not a cloud production cluster" in text or "not a cloud" in text.lower()
    assert data["production_target"]["meosprod_compose_profile"] == "EXISTS"
    assert data["production_target"]["meosprod_compose_is_production"] is False
    assert data["production_target"]["status"] == "MISSING"
    assert HELM.is_dir()
    assert data["production_target"]["helm_chart"] == "DESIGNED"
    assert data["cloud_hosting"]["status"] == "CREDENTIALS_REQUIRED"
    assert data["new_deployment_platform"] == "FORBIDDEN"
    assert data["go_live_declaration"] == "FORBIDDEN"
    assert data["application_activation"] == "FORBIDDEN"


def test_evidence_states_and_no_activation():
    data = _overlay()
    for key, val in data["evidence"].items():
        assert val in ALLOWED_EV, f"{key}={val}"
    assert data["evidence"]["tls"] == "MISSING"
    assert data["evidence"]["secrets"] == "BLOCKED"
    assert data["evidence"]["artifact_digest"] == "NOT_AVAILABLE"
    assert data["evidence"]["clean_commit"] == "FAIL"
    assert data["p313_gates_affected"]["G26"] == "BLOCKED"
    assert data["p313_gates_affected"]["G25"] == "FAIL"
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert registry["overall_status"] == "NOT_READY"
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    report = REPORT.read_text(encoding="utf-8")
    assert "P345" in report
    assert "G26" in report
    assert "INIT-G26" in data["next_operational_action"] or "Helm" in data["next_operational_action"]
