"""P354 release-candidate factory must reject dirty trees and must not fake G26 or digests."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
ENGINE = REPO / "scripts" / "meos_release_engine.py"
RC = REPO / "scripts" / "meos-release-candidate-readiness.py"
LAUNCH = REPO / "scripts" / "meos-launch-readiness.py"
REL = REPO / "scripts" / "meos-release-readiness.py"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"
SCAN = REPO / "scripts" / "meos-secret-scan.py"
MANIFEST = EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml"
STATUS = EXEC / "MEOS_P354_RELEASE_STATUS.v1.yaml"
DOC = EXEC / "MEOS_P354_RELEASE_CANDIDATE.md"
MIG = EXEC / "MEOS_MIGRATION_MANIFEST.v1.yaml"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
RUNBOOK = EXEC / "MEOS_PRODUCTION_RUNBOOK.md"
GO_LIVE = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
SBOM = REPO / "infrastructure" / "launch" / "MEOS_RELEASE_PACKAGE" / "SBOM.declared.json"
PACKAGE = REPO / "infrastructure" / "launch" / "MEOS_RELEASE_PACKAGE"
RESTORE = EXEC / ".last_p352_restore.json"
APP_FACTORY = REPO / "backend" / "core" / "presentation" / "api" / "app_factory.py"
DOCKERFILE = REPO / "infrastructure" / "docker" / "images" / "backend.Dockerfile"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p354_rc_artifacts_exist():
    for path in (RC, LAUNCH, REL, G26, SCAN, MANIFEST, STATUS, DOC, MIG, SBOM):
        assert path.is_file(), path
    assert not (REPO / "release").is_dir()
    doc = DOC.read_text(encoding="utf-8")
    assert "RELEASE_CANDIDATE" in doc
    assert "PRODUCTION_CERTIFIED" in doc
    assert "LOCAL_EVIDENCE" in doc
    assert "NOT_AVAILABLE" in doc
    sbom = json.loads(SBOM.read_text(encoding="utf-8"))
    assert sbom["SBOM_STATUS"] == "DECLARED_DEPENDENCIES_ONLY"
    rollback = (PACKAGE / "ROLLBACK.md").read_text(encoding="utf-8")
    assert "BEGIN PRIVATE" not in rollback
    assert "kubeconfig" not in rollback.lower()


def test_p354_manifest_nested_contract_no_invented_digest():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    for key in ("release", "application", "validation", "targets", "certification"):
        assert key in manifest, key
    rel = manifest["release"]
    for key in ("id", "version", "commit", "build_id", "image", "digest"):
        assert key in rel, key
    assert str(rel["digest"]) == "NOT_AVAILABLE"
    assert str(manifest["image_digest"]) == "NOT_AVAILABLE"
    assert str(manifest.get("image", "")).endswith(":latest") is False
    assert "latest" not in str(rel["image"]).lower()
    assert manifest.get("production_certified") in {False, "FALSE", "NO"}
    assert manifest.get("g26_ready") in {False, "FALSE", "NO"}
    assert manifest.get("release_candidate") in {False, "FALSE", "NO"}
    assert manifest["worktree_state"] == "DIRTY" or manifest.get("release_candidate") is False
    for target in ("local", "docker", "vps", "hostinger_vps", "aws", "azure", "gcp", "kubernetes"):
        row = manifest["targets"][target]
        assert row["PRODUCTION_STATUS"] != "PASS"
        assert "PRODUCTION_READY" not in str(row)
    assert manifest["certification"]["g26"] == "BLOCKED"
    assert manifest["certification"]["p313"] == "NOT_CERTIFIED"
    assert manifest["application"]["migrations"]["current"] == "055"
    assert manifest["application"]["migrations"]["production_database"] == "NOT_VERIFIED"
    assert manifest["validation"]["backup_class"] == "LOCAL_EVIDENCE"


def test_p354_dirty_tree_rejection_and_clean_acceptance():
    mod = _load(RC, "meos_release_candidate_readiness")
    assert (
        mod.release_candidate_ok(
            worktree_clean=False,
            forbidden_dirty=False,
            version="0.1.0",
            commit_sha="dd967051ab05c6ff57262502b456ad51b7d748fd",
            image="meos/backend:p353-local",
            schema="055",
        )
        is False
    )
    assert (
        mod.release_candidate_ok(
            worktree_clean=True,
            forbidden_dirty=True,
            version="0.1.0",
            commit_sha="dd967051ab05c6ff57262502b456ad51b7d748fd",
            image="meos/backend:p353-local",
            schema="055",
        )
        is False
    )
    assert (
        mod.release_candidate_ok(
            worktree_clean=True,
            forbidden_dirty=False,
            version="0.1.0",
            commit_sha="dd967051ab05c6ff57262502b456ad51b7d748fd",
            image="meos/backend:p353-local",
            schema="055",
        )
        is True
    )
    data = mod.evaluate()
    assert data["RELEASE_CANDIDATE"] is False
    assert data["WORKTREE_STATUS"] == "DIRTY"
    assert data["P354_STATUS"] == "BLOCKED"
    assert data["blocker"] == "DIRTY_WORKTREE"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["PRODUCTION_CERTIFIED"] is False
    assert data["image_digest"] == "NOT_AVAILABLE"
    assert data["DIGEST_STATUS"] == "NOT_AVAILABLE"
    assert data["localhost_is_production"] is False
    assert data["REGISTRY_ARTIFACT"] == "READY_FOR_CREDENTIALS"
    assert data["BACKUP_CLASS"] == "LOCAL_EVIDENCE"
    assert data["production_backup"] == "NOT_VERIFIED"
    assert "47258dfd-dirty" in str(data["forbidden_identity"])


def test_p354_version_identity_and_mutable_tag_rejection():
    engine = _load(ENGINE, "meos_release_engine")
    rc = _load(RC, "meos_release_candidate_readiness")
    rel = engine.meos_release()
    assert rel["release_version"] == "0.1.0"
    assert rel["source_commit"]
    assert rel["source_commit"] != "NOT_AVAILABLE"
    ident = engine.identity_ok(
        {
            **rel,
            "image": "ghcr.io/marpich/marpich-backend:latest",
            "image_digest": "NOT_AVAILABLE",
        }
    )
    assert ident["mutable_only"] is True
    assert ident["ok"] is False
    missing = engine.identity_ok(rel, require_digest=True)
    assert missing["ok"] is False
    assert "IMAGE_DIGEST_MISSING" in (missing["blocked"] or [])
    assert (
        rc.release_candidate_ok(
            worktree_clean=True,
            forbidden_dirty=False,
            version="0.1.0",
            commit_sha="abc123",
            image="meos/backend:latest",
            schema="055",
        )
        is False
    )
    assert (
        rc.release_candidate_ok(
            worktree_clean=True,
            forbidden_dirty=False,
            version="",
            commit_sha="abc123",
            image="meos/backend:p353-local",
            schema="055",
        )
        is False
    )
    schema = engine.schema_version()
    assert schema == "055"
    mig = yaml.safe_load(MIG.read_text(encoding="utf-8"))
    assert mig["migration_count"] == 55
    assert mig["apply"] == "NOT_EXECUTED"
    assert mig["production_database"] == "NOT_VERIFIED"


def test_p354_health_readiness_backup_tenant_and_packages():
    factory = APP_FACTORY.read_text(encoding="utf-8")
    assert '@application.get("/api/v1/health"' in factory
    assert '@application.get("/api/v1/live"' in factory or '@application.get("/live"' in factory
    assert '@application.get("/api/v1/ready"' in factory
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    assert "USER app" in dockerfile
    restore = json.loads(RESTORE.read_text(encoding="utf-8"))
    assert restore["restore_test"] == "PASS"
    assert restore["class"] == "LOCAL_NON_PRODUCTION"
    assert restore["production_restore"] == "NOT_VERIFIED"
    status = yaml.safe_load(STATUS.read_text(encoding="utf-8"))
    assert status["G26_READY"] is False
    assert status["P0"] == 1
    assert status["PRODUCTION_CERTIFIED"] is False
    assert status["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert status["ACTIVE_APPLICATIONS"] == 0
    assert status["PRODUCTION_TRAFFIC"] == "NOT_ENABLED"
    assert status["RELEASE_CANDIDATE"] is False
    assert status["VPS_PACKAGE"] == "READY"
    assert status["AWS_PACKAGE"] == "READY"
    assert status["KUBERNETES_PACKAGE"] == "READY"
    assert status["KUBERNETES_VALIDATION"] == "STATIC_VALIDATION_LIMITED"
    assert status["BACKUP_CLASS"] == "LOCAL_EVIDENCE"
    assert "secret" in SCAN.read_text(encoding="utf-8").lower()
    crm = (REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py").read_text(encoding="utf-8")
    assert "test_crm_tenant_b_cannot_list_tenant_a_contacts" in crm


def test_p354_does_not_force_g26_or_p313_or_golive():
    assert "P354" in CERT.read_text(encoding="utf-8")
    master = MASTER.read_text(encoding="utf-8")
    assert "P354" in master
    assert "RELEASE_CANDIDATE" in master or "release-candidate" in master.lower()
    assert "P354" in RUNBOOK.read_text(encoding="utf-8")
    assert "P354" in GO_LIVE.read_text(encoding="utf-8")
    assert "G26_READY" in G26.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    assert "does not start P313" in doc.lower() or "does not start p313" in doc.lower()
    assert "NOT_APPROVED" in doc
    status = yaml.safe_load(STATUS.read_text(encoding="utf-8"))
    assert status["P313_REENTRY_READY"] is False
    assert status["GO_LIVE_READY"] is False
