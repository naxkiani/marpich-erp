"""P349 discovery must identify infrastructure without forcing G26_READY or P313."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml"
DEPS = EXEC / "MEOS_EXT_G26_EXTERNAL_DEPENDENCIES.v1.yaml"
COMPAT = EXEC / "MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md"
BOM = EXEC / "MEOS_EXT_G26_PRODUCTION_BOM.md"
PLAN = EXEC / "MEOS_EXT_G26_INFRASTRUCTURE_IMPLEMENTATION_PLAN.md"
CONTRACT = EXEC / "MEOS_EXT_G26_INFRASTRUCTURE.v1.yaml"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
RUNBOOK = EXEC / "MEOS_PRODUCTION_RUNBOOK.md"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
HELM = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml"
FLUX = REPO / "infrastructure" / "fluxcd" / "marpich-iam-helmrelease.yaml"
CI = REPO / ".github" / "workflows" / "identity-federation-enterprise.yml"
ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE", "NOT_APPLICABLE"})
GATE_IDS = [f"G26-{i:02d}" for i in range(1, 11)]


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p349_frozen_governance_state():
    data = _overlay()
    assert data["p349_status"] == "REQUIREMENTS_IDENTIFIED"
    assert data["success_does_not_mean"] == "G26_PASS"
    assert data["ext_g26_status"] == "UNRESOLVED"
    assert data["g26_status"] == "BLOCKED"
    assert data["g26_ready"] is False
    assert data["p0_count"] == 1
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["p313_auto_start"] is False
    assert data["p313_reentry"] == "NOT_STARTED"
    assert data["p349_does_not_start_p313"] is True
    assert data["p349_does_not_execute_golive"] is True
    assert data["p349_does_not_provision"] is True
    assert data["production"] is False
    assert data["production_identity"] == "LOCAL"
    assert data["production_certified"] is False
    assert data["go_live_ready"] is False
    assert data["go_live_authorization"] == "NOT_APPROVED"
    assert data["registry_active_count"] == 0
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["g23"] == "FAIL"
    assert data["g23_production_verified"] is False
    assert data["forbidden_sha"] == "47258dfd-dirty"
    assert data["forbidden_dirty"] is True
    assert data["provider_selection"] == "BLOCKED"
    assert data["current_provider"] == "NOT_AVAILABLE"
    assert data["cost"] == "NOT_AVAILABLE"
    assert data["compose_is_production"] is False
    assert data["localhost_health_is_production"] is False
    assert data["live_production_hostname"] == "NOT_DEFINED"
    assert data["owner_default"] == "NOT_AVAILABLE"


def test_p349_g26_gates_none_pass():
    gates = _overlay()["g26_gates"]
    assert list(gates) == GATE_IDS
    assert gates["G26-01"] == "BLOCKED"
    assert gates["G26-02"] == "BLOCKED"
    assert gates["G26-03"] == "BLOCKED"
    assert gates["G26-04"] == "BLOCKED"
    assert gates["G26-05"] == "FAIL"
    assert gates["G26-06"] == "BLOCKED"
    assert gates["G26-07"] == "NOT_AVAILABLE"
    assert gates["G26-08"] == "BLOCKED"
    assert gates["G26-09"] == "NOT_AVAILABLE"
    assert gates["G26-10"] == "BLOCKED"
    assert "PASS" not in gates.values()


def test_p349_reuses_existing_helm_flux_ci_ghcr():
    data = _overlay()
    assert HELM.is_file()
    assert FLUX.is_file()
    assert CI.is_file()
    ci_text = CI.read_text(encoding="utf-8")
    assert "ghcr.io" in ci_text
    assert "helm rollback marpich-iam" in ci_text
    assert data["reuse"]["new_deployment_engine"] == "FORBIDDEN"
    assert data["reuse"]["new_ci_platform"] == "FORBIDDEN"
    assert data["deployment_path_verified"] == "CI_GHCR_HELM_OPTIONAL_FLUX_KUBERNETES"
    assert "identity-federation-enterprise.yml" in data["authoritative_path"]


def test_p349_dependency_register_statuses():
    deps = yaml.safe_load(DEPS.read_text(encoding="utf-8"))
    assert deps["g26_ready"] is False
    assert deps["p0_count"] == 1
    assert deps["external_dependency_count"] == 22
    assert deps["blocker_count"] == 21
    assert len(deps["dependencies"]) == 22
    owners = set()
    for row in deps["dependencies"]:
        assert row["current_status"] in ALLOWED
        assert row["current_status"] != "PASS"
        assert row["owner"] == "NOT_AVAILABLE"
        owners.add(row["owner"])
        assert "password" not in yaml.safe_dump(row).lower()
    assert owners == {"NOT_AVAILABLE"}


def test_p349_documents_exist_and_forbid_fake_pass():
    for path in (COMPAT, BOM, PLAN, OVERLAY, DEPS):
        assert path.is_file(), path
    blob = "\n".join(p.read_text(encoding="utf-8") for p in (COMPAT, BOM, PLAN))
    assert "47258dfd-dirty" in blob
    assert "MANAGED_KUBERNETES" in blob
    assert "NOT_AVAILABLE" in blob
    for banned in ("BEGIN PRIVATE", "AWS_SECRET_ACCESS_KEY"):
        assert banned not in blob
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert contract["g26_ready"] is False
    assert contract["p0_count"] == 1


def test_p349_cross_links():
    for path in (CHECKLIST, RUNBOOK, REPORT, MASTER):
        text = path.read_text(encoding="utf-8")
        assert "P349" in text
