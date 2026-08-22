"""P353 launch fabric must not fake production, digests, or collapse package vs credentials."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
MATRIX = EXEC / "MEOS_P353_PLATFORM_TARGET_MATRIX.md"
FABRIC = EXEC / "MEOS_P353_LAUNCH_FABRIC.md"
RELEASE = EXEC / "MEOS_P353_RELEASE_CONTRACT.md"
CONTRACT = EXEC / "MEOS_P353_ENVIRONMENT_CONTRACT.v1.yaml"
STATUS = EXEC / "MEOS_P353_TARGET_STATUS.v1.yaml"
READY = REPO / "scripts" / "meos-platform-target-readiness.py"
MANIFEST = EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
RUNBOOK = EXEC / "MEOS_PRODUCTION_RUNBOOK.md"
GO_LIVE = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
HELM_DEP = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "deployment.yaml"
TARGETS = REPO / "deploy" / "targets"


def _eval():
    spec = importlib.util.spec_from_file_location("meos_platform_target_readiness", READY)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate()


def test_p353_fabric_docs_and_overlays_exist():
    for path in (MATRIX, FABRIC, RELEASE, CONTRACT, STATUS, READY):
        assert path.is_file(), path
    for name in (
        "base.yaml",
        "vps.yaml",
        "hostinger-vps.yaml",
        "aws.yaml",
        "azure.yaml",
        "gcp.yaml",
        "kubernetes.yaml",
        "local.yaml",
        "local-demo.yaml",
    ):
        assert (TARGETS / name).is_file(), name
    hostinger = (TARGETS / "hostinger-vps.yaml").read_text(encoding="utf-8")
    assert "INCOMPATIBLE" in hostinger
    assert not (REPO / "deployment" / "targets").exists()
    matrix = MATRIX.read_text(encoding="utf-8")
    assert "INCOMPATIBLE" in matrix
    assert "NOT_VERIFIED" in matrix
    assert "PRODUCTION_READY" not in matrix


def test_p353_environment_contract_has_categories_no_secrets():
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    for key in (
        "APPLICATION",
        "DATABASE",
        "CACHE",
        "STORAGE",
        "EMAIL",
        "DNS",
        "TLS",
        "SECRETS",
        "OBSERVABILITY",
        "BACKUP",
        "AUTH",
        "TENANCY",
        "EXTERNAL_SERVICES",
    ):
        assert key in data, key
        assert isinstance(data[key], list) and data[key]
        for var in data[key]:
            for field in ("name", "required", "secret", "default_allowed", "production_required", "validation", "source"):
                assert field in var, (key, var, field)
    blob = CONTRACT.read_text(encoding="utf-8")
    assert "BEGIN RSA" not in blob
    assert "AKIA" not in blob
    assert data["never_commit_secret_values"] is True
    assert "JWT_SECRET" in data["secret_contract"]["never_commit"]
    assert data["localhost_is_production"] is False
    assert data["g26_ready"] is False


def test_p353_release_manifest_does_not_invent_digest_or_latest():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    digest = str(manifest["image_digest"])
    assert digest == "NOT_AVAILABLE" or digest.startswith("sha256:")
    assert "latest" not in str(manifest.get("image", "")).lower() or "p353-local" in str(manifest.get("image"))
    assert str(manifest.get("image", "")).endswith(":latest") is False
    assert manifest.get("production_certified") in {False, "FALSE", "NO"}
    compose = COMPOSE.read_text(encoding="utf-8")
    assert "COMPOSE_IS_PRODUCTION = FALSE" in compose
    assert "MEOS_IMAGE" in compose
    helm = HELM_DEP.read_text(encoding="utf-8")
    assert "/api/v1/ready" in helm
    assert "/api/v1/live" in helm
    rel = RELEASE.read_text(encoding="utf-8")
    assert "NOT_AVAILABLE" in rel
    assert "latest" in rel.lower()


def test_p353_target_status_does_not_collapse_states():
    status = yaml.safe_load(STATUS.read_text(encoding="utf-8"))
    assert status["g26_ready"] is False
    assert status["p0"] == 1
    assert status["production_ready"] == "FORBIDDEN_LABEL"
    assert status["targets"]["VPS"]["PACKAGE"] == "READY"
    assert status["targets"]["VPS"]["CREDENTIALS"] == "READY_FOR_CREDENTIALS"
    assert status["targets"]["VPS"]["STATUS"] != "READY"
    assert status["targets"]["AWS"]["DEPLOYMENT"] == "NOT_AVAILABLE"
    assert status["targets"]["PRODUCTION"]["STATUS"] == "BLOCKED"
    assert status["targets"]["LOCAL"]["PRODUCTION"] is False
    data = _eval()
    assert data["VPS_PACKAGE"] == "READY"
    assert data["AWS_PACKAGE"] == "READY"
    assert data["targets"]["AWS"]["CREDENTIALS"] == "READY_FOR_CREDENTIALS"
    assert data["targets"]["AWS"]["STATUS"] != "READY"
    assert data["targets"]["AWS"]["PRODUCTION"] is False
    assert data["targets"]["PRODUCTION"]["STATUS"] == "BLOCKED"
    assert data["G26_READY"] is False
    assert data["P313_REENTRY_READY"] is False
    assert data["replaces_g26"] is False
    assert data["localhost_is_production"] is False
    assert data["image_digest"] == "NOT_AVAILABLE" or str(data["image_digest"]).startswith("sha256:")
    if data["dirty"]:
        assert data["PRODUCTION_CERTIFIED"] is False


def test_p353_fabric_docs_do_not_create_next_phase_or_golive():
    fabric = FABRIC.read_text(encoding="utf-8")
    assert "does not create a new p354" in fabric.lower()
    assert "G26" in fabric
    assert "launch fabric" in MASTER.read_text(encoding="utf-8").lower()
    assert "launch fabric" in RUNBOOK.read_text(encoding="utf-8").lower() or "P353" in RUNBOOK.read_text(encoding="utf-8")
    assert "P353" in GO_LIVE.read_text(encoding="utf-8")
    assert G26.is_file()
    aws = (TARGETS / "aws.yaml").read_text(encoding="utf-8")
    assert "EC2_plus_Compose" in aws
    assert "CDK_app" in aws
