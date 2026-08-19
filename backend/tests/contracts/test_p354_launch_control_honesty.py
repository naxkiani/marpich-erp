"""P354 launch control must not fake production, bypass G26, or auto-deploy."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
ENGINE = REPO / "scripts" / "meos_launch_engine.py"
CLI = REPO / "scripts" / "meos-launch.py"
REG = EXEC / "MEOS_ENVIRONMENT_REGISTRY.v1.yaml"
CTRL = EXEC / "MEOS_LAUNCH_CONTROL.v1.yaml"
REPORT = EXEC / "MEOS_P354_LAUNCH_CONTROL_REPORT.md"
INSTALL_DOC = EXEC / "MEOS_P354_UNIVERSAL_INSTALLATION.md"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"


def _engine():
    spec = importlib.util.spec_from_file_location("meos_launch_engine", ENGINE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p354_launch_artifacts_exist():
    for path in (ENGINE, CLI, REG, CTRL, REPORT, INSTALL_DOC):
        assert path.is_file(), path
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    assert reg["g26_ready"] is False
    assert reg["environments"]["PRODUCTION"]["status"] == "DEPLOYMENT_BLOCKED"
    assert reg["environments"]["HOSTINGER_VPS"]["status"] == "READY_FOR_CREDENTIALS"
    assert reg["hostinger_shared"] == "INCOMPATIBLE"
    assert reg["environments"]["AWS"]["status"] != "READY"
    ctrl = yaml.safe_load(CTRL.read_text(encoding="utf-8"))
    assert ctrl["automatic_deploy"] is False
    assert "--skip-g26" in ctrl["forbidden_overrides"]
    assert ctrl["environments"]["PRODUCTION"]["CERTIFICATION"] == "NOT_CERTIFIED"


def test_p354_plan_does_not_deploy_and_rfc_is_not_ready():
    mod = _engine()
    planned = mod.plan("aws")
    assert planned["deployment_occurs"] is False
    assert planned["executed"] is False
    assert planned["status"] == "READY_FOR_CREDENTIALS"
    assert planned["status"] != "READY"
    assert planned["confirmation_required"] is True
    local = mod.plan("local")
    assert local["deployment_occurs"] is False
    prod = mod.plan("production")
    assert prod["status"] == "DEPLOYMENT_BLOCKED"
    assert prod["DATABASE"] != "PRODUCTION"


def test_p354_deploy_requires_confirm_and_blocks_unsafe(monkeypatch):
    mod = _engine()
    no = mod.deploy("demo", confirm="")
    assert no["executed"] is False
    assert no["status"] == "NOT_EXECUTED"
    aws = mod.deploy("aws", confirm="yes")
    assert aws["executed"] is False
    assert aws["status"] == "READY_FOR_CREDENTIALS"
    prod = mod.deploy("production", confirm="yes")
    assert prod["executed"] is False
    assert prod["status"] == "DEPLOYMENT_BLOCKED"
    assert "G26_READY=FALSE" in prod["blockers"]
    refused = mod.refuse_overrides(["deploy", "--env", "production", "--force"])
    assert refused["status"] == "DEPLOYMENT_BLOCKED"
    assert "FORBIDDEN_OVERRIDE" in refused["reason"]
    for flag in ("--skip-g26", "--production-anymore", "--ignore-certification"):
        if flag == "--production-anymore":
            flag = "--production-anyway"
        hit = mod.refuse_overrides([flag])
        assert hit is not None
        assert hit["executed"] is False
    shared = mod.preflight("hostinger-shared")
    assert shared["status"] == "DEPLOYMENT_BLOCKED"
    assert shared["hostinger_shared"] == "INCOMPATIBLE"


def test_p354_negative_preflight(monkeypatch):
    mod = _engine()
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    monkeypatch.delenv("MEOS_PUBLIC_CA_TLS", raising=False)
    monkeypatch.delenv("MEOS_SECRET_MANAGER_AVAILABLE", raising=False)
    monkeypatch.setenv("PGHOST", "127.0.0.1")
    monkeypatch.setenv("PGPORT", "5433")
    pf = mod.preflight("production")
    assert pf["status"] == "DEPLOYMENT_BLOCKED"
    assert pf["localhost_is_production"] is False
    assert pf["compose_is_production"] is False
    assert "LOCALHOST_OR_COMPOSE_DB_NOT_PRODUCTION" in pf["blockers"] or "G26_READY=FALSE" in pf["blockers"]
    aws = mod.preflight("aws")
    assert aws["status"] == "READY_FOR_CREDENTIALS"
    assert aws["status"] != "READY"
    creds = aws["credentials"]["missing"]
    assert creds
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
    missing_docker = mod.preflight("local")
    docker_check = next(c for c in missing_docker["checks"] if c["name"] == "docker")
    assert docker_check["state"] == "MISSING"
    assert missing_docker["status"] in {"NOT_READY", "DEPLOYMENT_BLOCKED"}
    ident = mod.meos_release()
    assert ident["image_digest"] == "NOT_AVAILABLE" or str(ident["image_digest"]).startswith("sha256:")
    dirty = mod.dirty_report()
    if dirty["dirty"]:
        blocked_cloud = mod.preflight("kubernetes")
        assert "DIRTY_TREE_BLOCKS_RELEASE_DEPLOY" in blocked_cloud["blockers"]
        assert blocked_cloud["status"] != "READY"


def test_p354_verify_does_not_infer_production():
    mod = _engine()
    demo = mod.verify("demo")
    assert demo["localhost_is_production"] is False
    assert demo["compose_is_production"] is False
    assert demo["production_certified"] is False
    assert demo["g26_ready"] is False
    prod = mod.verify("production")
    assert prod["DEPLOYMENT_VERIFIED"] is False
    assert prod["status"] == "DEPLOYMENT_BLOCKED"
    rb = mod.rollback("production", confirm="yes")
    assert rb["executed"] is False
    assert rb["configured_equals_exercised"] is False


def test_p354_local_demo_deploy_uses_existing_scripts():
    mod = _engine()
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="DEMO_START=TRUE\n", stderr="")

    monkey_result = None

    def _deploy():
        return mod.deploy("demo", confirm="yes", runner=fake_run)

    monkey_result = _deploy()
    assert monkey_result["executed"] is True
    assert monkey_result["class"] == "NON_PRODUCTION"
    assert monkey_result["CONFIRM"] is True
    assert any("meos-demo.sh" in str(c) for c in calls)
    assert monkey_result["g26_ready"] is False
    assert "Success is not inferred from exit code alone" in monkey_result["verification"]["note"]


def test_p354_launch_docs_isolate_g26():
    assert "P354" in CERT.read_text(encoding="utf-8")
    assert "launch control" in MASTER.read_text(encoding="utf-8").lower() or "P354" in MASTER.read_text(
        encoding="utf-8"
    )
    report = REPORT.read_text(encoding="utf-8")
    assert "NOT_APPROVED" in report
    assert "READY_FOR_CREDENTIALS" in report
    assert G26.is_file()
    st = _engine().status()
    assert st["G26_READY"] is False
    assert st["P0"] == 1
    assert st["P313"] == "NOT_CERTIFIED"
    assert st["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert st["ACTIVE_APPLICATIONS"] == 0
    assert st["environments"]["AWS"] != "READY"
    assert st["environments"]["PRODUCTION"] == "DEPLOYMENT_BLOCKED"
