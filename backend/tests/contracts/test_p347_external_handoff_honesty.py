"""P347 must freeze EXT-G26, not deploy, and forbid prompt-loop architecture expansion."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P347_EXTERNAL_HANDOFF.v1.yaml"
P346 = EXEC / "MEOS_P346_G26_BLOCKER_CLOSURE.v1.yaml"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
RUNBOOK = EXEC / "MEOS_PRODUCTION_RUNBOOK.md"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
HELM = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml"
FLUX = REPO / "infrastructure" / "fluxcd" / "marpich-iam-helmrelease.yaml"
CI = REPO / ".github" / "workflows" / "identity-federation-enterprise.yml"

RESOURCES = [
    "AUTHORIZED_PRODUCTION_HOSTING_ACCOUNT",
    "PRODUCTION_CLUSTER_OR_SERVER",
    "MANAGED_POSTGRESQL",
    "PUBLIC_DNS",
    "PUBLIC_CA_TLS",
    "PRODUCTION_SECRET_MANAGER",
    "CI_DEPLOY_CREDENTIALS",
    "CONTAINER_REGISTRY_ACCESS",
    "CLEAN_GIT_RELEASE_STATE",
    "PRODUCTION_DEPLOYMENT_IDENTITY",
]


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p346_stopped_and_ext_g26_unresolved():
    p346 = yaml.safe_load(P346.read_text(encoding="utf-8"))
    data = _overlay()
    assert p346["outcome"] == "STOPPED"
    assert p346["g26_status"] == "BLOCKED"
    assert data["p346_outcome"] == "STOPPED"
    assert data["outcome"] == "HANDOFF"
    assert data["status"] == "EXTERNAL_DEPENDENCY_BLOCKED"
    assert data["ext_g26_status"] == "UNRESOLVED"
    assert data["g26_status"] == "BLOCKED"
    assert data["p0_count"] == 1
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["p313_reentry"] == "NOT_STARTED"
    assert data["p347_does_not_start_p313"] is True
    assert data["p347_does_not_execute_p344"] is True
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_authorization"] == "NOT APPROVED"
    assert data["dec_p314_001"] == "NOT APPROVED"
    assert data["registry_active_count"] == 0
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["no_prompt_loop"] is True
    assert data["next_architecture_prompt"] == "FORBIDDEN"
    assert "47258dfd-dirty" in str(data["git_describe_forbidden"])
    assert data["required_external_resources"] == RESOURCES
    assert data["responsible_party"] == "NOT_AVAILABLE"


def test_reuse_existing_helm_flux_ci():
    data = _overlay()
    assert HELM.is_file()
    assert FLUX.is_file()
    assert CI.is_file()
    assert "ghcr.io" in CI.read_text(encoding="utf-8")
    path = data["reuse_path"]
    assert path["new_deployment_engine"] == "FORBIDDEN"
    assert path["new_ci_platform"] == "FORBIDDEN"
    mins = data["g26_reentry_minimum"]
    for i in range(1, 10):
        assert mins[f"G26-{i:02d}"] == "PASS"
    assert mins["G26-10"] == "VERIFIED"
    assert mins["averaging"] == "FORBIDDEN"
    seq = data["reentry_sequence"]
    assert seq[0] == "G26_REVALIDATION"
    assert seq[1] == "P313_RECERTIFICATION"
    assert seq[-1] == "P344_FINAL_GO_LIVE"
    assert "P348" in data["next_legitimate_execution_step"]


def test_docs_and_no_activation():
    checklist = CHECKLIST.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")
    master = MASTER.read_text(encoding="utf-8")
    assert "G26 re-entry" in checklist
    assert "- [ ] G26-01" in checklist
    assert "- [x] G26-01" not in checklist
    assert "EXT-G26" in runbook
    assert "helm" in runbook.lower()
    assert "P347" in report
    assert "UNRESOLVED" in report or "EXTERNAL_DEPENDENCY_BLOCKED" in report
    assert "WAIT" in master or "EXT-G26" in master
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
