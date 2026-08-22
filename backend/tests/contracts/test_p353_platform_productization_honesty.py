"""P353 platform factory must not fake production, credentials, or G26."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
DEPLOY = REPO / "deploy"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
GO_LIVE = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
CENTER = EXEC / "MEOS_EXECUTIVE_COMMAND_CENTER.md"
DOC = EXEC / "MEOS_P353_PLATFORM_PRODUCTIZATION.md"
FACTORY = EXEC / "MEOS_DEPLOYMENT_FACTORY.md"
CUSTOMER = EXEC / "MEOS_CUSTOMER_DEPLOYMENT_GUIDE.md"
MATRIX = EXEC / "MEOS_PLATFORM_READINESS.v1.yaml"
READY = REPO / "scripts" / "meos-platform-readiness.py"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
DOCKERFILE = REPO / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
CI = REPO / ".github" / "workflows" / "identity-federation-enterprise.yml"
HELM = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml"


def _eval():
    spec = importlib.util.spec_from_file_location("meos_platform_readiness", READY)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate()


def test_p353_factory_artifacts_exist():
    for path in (DOC, FACTORY, CUSTOMER, MATRIX, READY, DEPLOY / "README.md"):
        assert path.is_file(), path
    for name in (
        "docker",
        "compose",
        "vps",
        "hostinger",
        "aws",
        "azure",
        "gcp",
        "kubernetes",
        "scripts",
        "environments",
    ):
        assert (DEPLOY / name).exists(), name
    for env in (
        "ENV_LOCAL",
        "ENV_DEMO",
        "ENV_STAGING",
        "ENV_VPS",
        "ENV_HOSTINGER_VPS",
        "ENV_AWS",
        "ENV_AZURE",
        "ENV_GCP",
        "ENV_KUBERNETES",
        "ENV_PRODUCTION",
    ):
        text = (DEPLOY / "environments" / f"{env}.env.example").read_text(encoding="utf-8")
        assert "CHANGE_ME" in text or env in {"ENV_LOCAL", "ENV_DEMO"}
        assert "BEGIN RSA" not in text
        assert "AKIA" not in text
    contract = yaml.safe_load((DEPLOY / "environments" / "CONTRACT.v1.yaml").read_text(encoding="utf-8"))
    assert contract["localhost_is_production"] is False
    assert contract["compose_is_production"] is False
    assert contract["g26_ready"] is False
    assert DOCKERFILE.is_file()
    assert COMPOSE.is_file()
    assert "COMPOSE_IS_PRODUCTION = FALSE" in COMPOSE.read_text(encoding="utf-8")
    assert HELM.is_file()
    hostinger = (DEPLOY / "hostinger" / "README.md").read_text(encoding="utf-8")
    assert "INCOMPATIBLE" in hostinger
    assert "READY_FOR_CREDENTIALS" in hostinger


def test_p353_factory_reuses_canonical_image_not_a_fork():
    docker_readme = (DEPLOY / "docker" / "README.md").read_text(encoding="utf-8")
    assert "backend.Dockerfile" in docker_readme
    assert not (DEPLOY / "docker" / "Dockerfile").exists()
    assert not (DEPLOY / "kubernetes" / "Chart.yaml").exists()
    ci_matrix = yaml.safe_load((DEPLOY / "ci" / "DEPLOYMENT_MATRIX.v1.yaml").read_text(encoding="utf-8"))
    assert ci_matrix["automatic_production_deploy"] is False
    assert ci_matrix["workflow"] == ".github/workflows/identity-federation-enterprise.yml"
    ci_text = CI.read_text(encoding="utf-8")
    assert "environment: production" in ci_text
    assert "workflow_dispatch" in ci_text


def test_p353_negative_conditions():
    data = _eval()
    assert data["localhost_is_production"] is False
    assert data["compose_is_production"] is False
    assert data["ready_for_credentials_is_ready"] is False
    assert data["configured_is_verified"] is False
    assert data["dirty_sha_is_release"] is False
    assert data["missing_credentials_is_deployed"] is False
    assert data["platforms"]["LOCAL"]["database"].startswith("127.0.0.1")
    assert data["platforms"]["DEMO"]["database"].startswith("127.0.0.1")
    assert data["platforms"]["PRODUCTION"]["status"] == "BLOCKED"
    for name in ("VPS", "HOSTINGER_VPS", "AWS", "AZURE", "GCP", "KUBERNETES"):
        assert data["platforms"][name]["status"] == "READY_FOR_CREDENTIALS"
        assert data["platforms"][name]["status"] != "READY"
        assert data["platforms"][name]["deployed"] is False
        assert data["platforms"][name]["production_verified"] is False
    assert data["VPS_READY"] == "READY_FOR_CREDENTIALS"
    assert data["VPS_READY"] != "READY"
    assert data["AWS_READY"] != "READY"
    matrix = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    assert matrix["localhost_is_production"] is False
    assert matrix["compose_is_production"] is False
    assert matrix["ready_for_credentials_is_ready"] is False
    assert matrix["platforms"]["PRODUCTION"]["status"] == "BLOCKED"
    assert matrix["platforms"]["AWS"]["status"] == "READY_FOR_CREDENTIALS"
    assert matrix["g26_ready"] is False


def test_p353_factory_does_not_weaken_g26():
    data = _eval()
    assert data["G26_READY"] is False
    assert data["G26_STATUS"] == "BLOCKED"
    assert data["P0"] == 1
    assert data["P313"] == "NOT_CERTIFIED"
    assert data["P313_REENTRY_READY"] is False
    assert data["PRODUCTION_CERTIFIED"] is False
    assert data["GO_LIVE_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["PRODUCTION_TRAFFIC"] == "NOT_ENABLED"
    if data["worktree_clean"] is False:
        assert data["CLEAN_RELEASE_STATUS"] == "FORBIDDEN_FOR_RELEASE"
    assert "47258dfd-dirty" in data["forbidden_identity"]
    assert data["image_digest"] in {"NOT_AVAILABLE"} or str(data["image_digest"]).startswith("sha256:")


def test_p353_factory_docs_isolate_g26():
    for path in (DOC, FACTORY, CUSTOMER):
        text = path.read_text(encoding="utf-8")
        assert "G26" in text
        assert "NOT_APPROVED" in text or "not approved" in text.lower()
    assert "P353" in CERT.read_text(encoding="utf-8")
    master = MASTER.read_text(encoding="utf-8")
    assert "P353" in master
    assert "deployment factory" in master.lower()
    assert "P353" in GO_LIVE.read_text(encoding="utf-8")
    assert "P353" in CENTER.read_text(encoding="utf-8")
    assert G26.is_file()
    demo = (DEPLOY / "scripts" / "meos-demo.sh").read_text(encoding="utf-8")
    assert "COMPOSE_IS_PRODUCTION=FALSE" in demo
    assert "start)" in demo and "stop)" in demo and "reset)" in demo
    assert "backup)" in demo and "restore)" in demo and "health)" in demo
