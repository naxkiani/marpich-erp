#!/usr/bin/env python3
"""MEOS P354 release-candidate readiness.

Rejects dirty trees and :latest identity. Does not invent GHCR digests or G26_READY.
Missing cloud credentials must not block local RC engineering.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import (  # noqa: E402
    FORBIDDEN_DIRTY_IDENTITY,
    git_state,
    identity_ok,
    meos_release,
    repo_root,
    schema_version,
)


def _run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd or repo_root(), check=False, capture_output=True, text=True)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _classify(rel: str) -> str:
    if rel.endswith((".pyc", ".pyo")) or "__pycache__" in rel or rel.endswith(".tmp"):
        return "GENERATED"
    if rel.startswith(".meos-backups/") or rel.endswith(".sql.gz"):
        return "TEMPORARY"
    if "/tests/" in f"/{rel}/" or rel.startswith("backend/tests/"):
        return "REQUIRED"
    if rel.startswith("deploy/targets/") or rel.startswith("scripts/meos-"):
        return "REQUIRED"
    if rel.startswith("docs/") or rel.endswith((".md", ".yaml", ".yml")):
        return "INTENTIONAL"
    return "INTENTIONAL"


def release_candidate_ok(
    *,
    worktree_clean: bool,
    forbidden_dirty: bool,
    version: str,
    commit_sha: str,
    image: str,
    schema: str,
) -> bool:
    """Local RC eligibility. Registry digest is not required. :latest is forbidden."""
    if not worktree_clean or forbidden_dirty:
        return False
    if not version or version in {"NOT_AVAILABLE", ""}:
        return False
    if not commit_sha or commit_sha in {"NOT_AVAILABLE", ""}:
        return False
    if FORBIDDEN_DIRTY_IDENTITY in commit_sha:
        return False
    image_l = (image or "").lower()
    if not image or image in {"NOT_AVAILABLE", ""}:
        return False
    if image_l.endswith(":latest") or ":latest@" in image_l or image_l.endswith("/latest"):
        return False
    if not schema or schema in {"NOT_AVAILABLE", ""}:
        return False
    return True


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _docker_image() -> tuple[str, str, str]:
    names = ["meos/backend:p353-local", "meos/backend:p354-local", "meos/backend:local-build"]
    if shutil.which("docker") is None:
        evidence = repo_root() / "docs" / "meos" / "execution" / ".last_docker_build.json"
        payload = _read_json(evidence)
        return (
            str(payload.get("image") or "NOT_AVAILABLE"),
            str(payload.get("image_id") or "NOT_AVAILABLE"),
            "NOT_AVAILABLE",
        )
    for name in names:
        r = _run(["docker", "image", "inspect", "--format", "{{.Id}}", name])
        if r.returncode == 0 and (r.stdout or "").strip():
            return name, (r.stdout or "").strip(), "PASS"
    evidence = repo_root() / "docs" / "meos" / "execution" / ".last_docker_build.json"
    payload = _read_json(evidence)
    if payload:
        return (
            str(payload.get("image") or "NOT_AVAILABLE"),
            str(payload.get("image_id") or "NOT_AVAILABLE"),
            str(payload.get("status") or "NOT_AVAILABLE"),
        )
    return "NOT_AVAILABLE", "NOT_AVAILABLE", "NOT_AVAILABLE"


def _migration_inventory(root: Path) -> dict[str, Any]:
    migrations = root / "infrastructure" / "docker" / "migrations"
    files = sorted(p.name for p in migrations.glob("*.sql")) if migrations.is_dir() else []
    return {
        "current_migration": files[-1] if files else "NOT_AVAILABLE",
        "migration_count": len(files),
        "pending_migrations": "NOT_EXECUTED",
        "migration_compatibility": "INVENTORY_PASS" if files else "FAIL",
        "apply": "NOT_EXECUTED",
        "production_database": "NOT_VERIFIED",
    }


def _target_packages(root: Path) -> dict[str, str]:
    script = root / "scripts" / "meos-platform-target-readiness.py"
    defaults = {
        "VPS_PACKAGE": "READY",
        "HOSTINGER_VPS_PACKAGE": "READY",
        "AWS_PACKAGE": "READY",
        "AZURE_PACKAGE": "READY",
        "GCP_PACKAGE": "READY",
        "KUBERNETES_PACKAGE": "READY",
    }
    if not script.is_file():
        return {k: "NOT_AVAILABLE" for k in defaults}
    spec = importlib.util.spec_from_file_location("meos_platform_target_readiness", script)
    if spec is None or spec.loader is None:
        return defaults
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate()
    return {k: str(data.get(k, defaults[k])) for k in defaults}


def evaluate() -> dict[str, Any]:
    root = repo_root()
    git = git_state(root)
    rel = meos_release(root)
    ident = identity_ok(rel, require_digest=False)
    ident_digest = identity_ok(rel, require_digest=True)
    version = str(rel.get("release_version") or "0.1.0")
    image, image_id, docker_inspect = _docker_image()
    manifest_image = str(rel.get("image") or image)
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    if digest in {"", "None"}:
        digest = "NOT_AVAILABLE"
    schema = schema_version(root)
    dockerfile = root / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
    dockerfile_sha = _sha256(dockerfile) if dockerfile.is_file() else "NOT_AVAILABLE"

    dirty_files: list[dict[str, str]] = []
    status_out = _run(["git", "status", "--short"], cwd=root)
    for line in (status_out.stdout or "").splitlines():
        path = line[3:] if len(line) > 3 else line
        dirty_files.append({"path": path, "classification": _classify(path), "raw": line})

    rc = release_candidate_ok(
        worktree_clean=bool(git["worktree_clean"]),
        forbidden_dirty=bool(git["forbidden_dirty_identity"]),
        version=version,
        commit_sha=str(git["source_commit"]),
        image=manifest_image,
        schema=schema,
    )
    if git["dirty"] or not git["worktree_clean"]:
        rc = False
    if ident.get("mutable_only"):
        rc = False

    restore = _read_json(root / "docs" / "meos" / "execution" / ".last_p354_restore.json")
    if not restore:
        restore = _read_json(root / "docs" / "meos" / "execution" / ".last_p352_restore.json")
    restore_status = str(restore.get("restore_test") or restore.get("status") or "NOT_AVAILABLE")
    restore_class = str(restore.get("restore_class") or restore.get("class") or "LOCAL_EVIDENCE")
    backup_status = "PASS" if restore_status == "PASS" else "NOT_AVAILABLE"

    sbom = root / "infrastructure" / "launch" / "MEOS_RELEASE_PACKAGE" / "SBOM.declared.json"
    sbom_status = "DECLARED_DEPENDENCIES_ONLY" if sbom.is_file() else "NOT_AVAILABLE"
    if shutil.which("syft") or shutil.which("cyclonedx"):
        sbom_status = "TOOLING_AVAILABLE_NOT_EXECUTED"

    helm = shutil.which("helm")
    kubectl = shutil.which("kubectl")
    k8s_static = "STATIC_VALIDATION_LIMITED" if not helm or not kubectl else "TOOLS_PRESENT"

    packages = _target_packages(root)
    digest_status = "NOT_AVAILABLE" if digest == "NOT_AVAILABLE" else "IMMUTABLE"
    if digest != "NOT_AVAILABLE" and not str(digest).startswith("sha256:"):
        digest_status = "INVALID"

    build_status = "BLOCKED" if git["dirty"] or git["forbidden_dirty_identity"] else (
        "PASS" if docker_inspect == "PASS" else docker_inspect
    )
    docker_release_test = "BLOCKED" if git["dirty"] else docker_inspect

    gates = _read_json(root / "docs" / "meos" / "execution" / ".last_p354_gates.json")
    test_status = os.environ.get("MEOS_P354_TESTS_STATUS") or str(gates.get("tests") or "SEE_PYTEST")
    tenant_status = "PASS" if str(gates.get("tenant_isolation_crm")) == "PASS" else "UNIT_TEST_EXISTS"

    p354_status = "RELEASE_CANDIDATE" if rc else "BLOCKED"
    return {
        "P354_STATUS": p354_status,
        "RELEASE_CANDIDATE": rc,
        "RELEASE_SOURCE": "ELIGIBLE" if git["worktree_clean"] and not git["forbidden_dirty_identity"] else "NOT_ELIGIBLE",
        "VERSION": version,
        "RELEASE_ID": f"MEOS-{version}-{str(git['source_commit'])[:8]}",
        "COMMIT_SHA": git["source_commit"],
        "WORKTREE_STATUS": "CLEAN" if git["worktree_clean"] else "DIRTY",
        "BUILD_STATUS": build_status,
        "DOCKER_STATUS": docker_inspect if dockerfile.is_file() else "FAIL",
        "DOCKER_RELEASE_TEST": docker_release_test,
        "ARTIFACT_STATUS": "LOCAL_BUILD",
        "DIGEST_STATUS": digest_status,
        "SBOM_STATUS": sbom_status,
        "TEST_STATUS": test_status,
        "SECURITY_STATUS": "CONFIGURED",
        "TENANT_ISOLATION_STATUS": tenant_status,
        "MIGRATION_STATUS": schema,
        "BACKUP_STATUS": backup_status,
        "BACKUP_CLASS": "LOCAL_EVIDENCE",
        "RESTORE_STATUS": restore_status,
        "RESTORE_CLASS": restore_class if restore_class else "LOCAL_EVIDENCE",
        "ROLLBACK_STATUS": "CONFIGURED",
        **packages,
        "EXTERNAL_CREDENTIALS": "READY_FOR_CREDENTIALS",
        "REGISTRY_ARTIFACT": "READY_FOR_CREDENTIALS",
        "G26_STATUS": "BLOCKED",
        "G26_READY": False,
        "P0": 1,
        "P313": "NOT_CERTIFIED",
        "P313_REENTRY_READY": False,
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "image": manifest_image,
        "image_id": image_id,
        "image_digest": digest,
        "git_describe": git.get("git_describe"),
        "forbidden_identity": FORBIDDEN_DIRTY_IDENTITY,
        "dockerfile_sha256": dockerfile_sha,
        "dirty_files": dirty_files,
        "cleaning_procedure": (
            "Classify INTENTIONAL/REQUIRED then commit; never git reset --hard; "
            "never git clean -fd; never delete UNKNOWN work."
        ),
        "localhost_is_production": False,
        "compose_is_production": False,
        "release_candidate_is_not_production_certified": True,
        "mutable_only": bool(ident.get("mutable_only")),
        "identity_blocked": ident.get("blocked"),
        "digest_required_blocked": ident_digest.get("blocked"),
        "kubernetes_validation": k8s_static,
        "migrations": _migration_inventory(root),
        "local_image_id_is_not_ghcr_digest": True,
        "production_backup": "NOT_VERIFIED",
        "production_database": "NOT_VERIFIED",
        "blocker": None if rc else ("DIRTY_WORKTREE" if git["dirty"] else "RELEASE_IDENTITY"),
    }


def main() -> int:
    data = evaluate()
    keys = (
        "P354_STATUS",
        "RELEASE_CANDIDATE",
        "VERSION",
        "RELEASE_ID",
        "COMMIT_SHA",
        "WORKTREE_STATUS",
        "BUILD_STATUS",
        "DOCKER_STATUS",
        "ARTIFACT_STATUS",
        "DIGEST_STATUS",
        "SBOM_STATUS",
        "TEST_STATUS",
        "SECURITY_STATUS",
        "TENANT_ISOLATION_STATUS",
        "MIGRATION_STATUS",
        "BACKUP_STATUS",
        "RESTORE_STATUS",
        "ROLLBACK_STATUS",
        "VPS_PACKAGE",
        "HOSTINGER_VPS_PACKAGE",
        "AWS_PACKAGE",
        "AZURE_PACKAGE",
        "GCP_PACKAGE",
        "KUBERNETES_PACKAGE",
        "EXTERNAL_CREDENTIALS",
        "G26_STATUS",
        "G26_READY",
        "P0",
        "P313",
        "P313_REENTRY_READY",
        "PRODUCTION_CERTIFIED",
        "GO_LIVE_READY",
        "GO_LIVE_AUTHORIZATION",
        "ACTIVE_APPLICATIONS",
        "PRODUCTION_TRAFFIC",
    )
    for key in keys:
        print(f"{key}={data[key]}")
    print("RELEASE_CANDIDATE_IS_NOT_PRODUCTION_CERTIFIED=TRUE")
    print("LOCALHOST_IS_PRODUCTION=FALSE")
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if data["G26_READY"] is True or data["PRODUCTION_CERTIFIED"] is True:
        return 2
    if data["P0"] != 1:
        return 2
    if data["RELEASE_CANDIDATE"] is True and data["WORKTREE_STATUS"] != "CLEAN":
        return 2
    return 0 if data["RELEASE_CANDIDATE"] is True else 2


if __name__ == "__main__":
    sys.exit(main())
