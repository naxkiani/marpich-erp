#!/usr/bin/env python3
"""MEOS release readiness (P353). Does not manufacture registry digests or G26_READY."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd or repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )


def _git(args: list[str]) -> str:
    return (_run(["git", *args]).stdout or "").strip()


def _secret_scan() -> str:
    script = repo_root() / "scripts" / "meos-secret-scan.py"
    if not script.is_file():
        return "NOT_AVAILABLE"
    r = _run([sys.executable, str(script)])
    if r.returncode == 0:
        return "PASS"
    if r.returncode == 2:
        return "FAIL"
    return "BLOCKED"


def _docker_image_available(names: list[str]) -> tuple[str, str, str]:
    if shutil.which("docker") is None:
        return "NOT_AVAILABLE", "NOT_AVAILABLE", "MISSING_DOCKER_CLI"
    for name in names:
        r = _run(["docker", "image", "inspect", "--format", "{{.Id}}", name])
        if r.returncode == 0 and (r.stdout or "").strip():
            return name, (r.stdout or "").strip(), "PASS"
    evidence = repo_root() / "docs" / "meos" / "execution" / ".last_docker_build.json"
    if evidence.is_file():
        try:
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            return (
                str(payload.get("image", "NOT_AVAILABLE")),
                str(payload.get("image_id", "NOT_AVAILABLE")),
                str(payload.get("status", "NOT_AVAILABLE")),
            )
        except json.JSONDecodeError:
            return "NOT_AVAILABLE", "NOT_AVAILABLE", "FAIL"
    return "NOT_AVAILABLE", "NOT_AVAILABLE", "NOT_AVAILABLE"


def _registry_status() -> str:
    if os.environ.get("GITHUB_TOKEN") or os.environ.get("GHCR_TOKEN"):
        return "CREDENTIALS_PRESENT_UNVERIFIED"
    docker_config = Path.home() / ".docker" / "config.json"
    if docker_config.is_file():
        try:
            payload = json.loads(docker_config.read_text(encoding="utf-8"))
            auths = payload.get("auths") or {}
            creds = payload.get("credHelpers") or {}
            keys = " ".join(list(auths) + list(creds)).lower()
            if "ghcr.io" in keys:
                return "DOCKER_CONFIG_HAS_GHCR"
        except (OSError, json.JSONDecodeError):
            pass
    return "READY_FOR_CREDENTIALS"


def _tests_status() -> str:
    override = os.environ.get("MEOS_TESTS_STATUS")
    if override:
        return override
    gates = repo_root() / "docs" / "meos" / "execution" / ".last_p353_gates.json"
    if gates.is_file():
        try:
            payload = json.loads(gates.read_text(encoding="utf-8"))
            return str(payload.get("tests", "NOT_AVAILABLE"))
        except json.JSONDecodeError:
            return "FAIL"
    return "NOT_AVAILABLE"


def evaluate() -> dict[str, Any]:
    root = repo_root()
    short = _git(["status", "--short"])
    describe = _git(["describe", "--always", "--dirty"])
    sha = _git(["rev-parse", "HEAD"]) or "NOT_AVAILABLE"
    branch = _git(["branch", "--show-current"]) or "NOT_AVAILABLE"
    clean = short == ""
    dirty = (not clean) or ("dirty" in describe)
    secret = _secret_scan()
    image, image_id, docker_build = _docker_image_available(
        ["meos/backend:p353-local", "meos/backend:p352-local", "meos/backend:local-build"]
    )
    tests = _tests_status()
    registry = _registry_status()
    ci = root / ".github" / "workflows" / "identity-federation-enterprise.yml"
    ci_digest_wired = False
    if ci.is_file():
        ci_digest_wired = "steps.image.outputs.digest" in ci.read_text(encoding="utf-8")
    helm_helper = root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "_helpers.tpl"
    helm_digest = False
    if helm_helper.is_file():
        helm_digest = ".Values.image.digest" in helm_helper.read_text(encoding="utf-8")
    compose = (root / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml").read_text(
        encoding="utf-8"
    )
    commit_valid = bool(sha) and sha != "NOT_AVAILABLE" and not dirty
    worktree_clean = clean
    tests_pass = tests == "PASS"
    build_pass = docker_build == "PASS"
    secret_pass = secret == "PASS"
    image_available = image not in {"", "NOT_AVAILABLE"} and image_id not in {"", "NOT_AVAILABLE"}
    digest_available = False
    image_digest = "NOT_AVAILABLE"
    local_release = all(
        [worktree_clean, tests_pass, build_pass, secret_pass, commit_valid, image_available]
    )
    if registry == "READY_FOR_CREDENTIALS":
        registry_release = "READY_FOR_CREDENTIALS"
    elif digest_available:
        registry_release = True
    else:
        registry_release = "READY_FOR_CREDENTIALS"
    deployment_release = "READY_FOR_CREDENTIALS"
    production_release = False
    return {
        "WORKTREE_CLEAN": worktree_clean,
        "TESTS_PASS": tests_pass,
        "tests": tests,
        "BUILD_PASS": build_pass,
        "build": docker_build,
        "SECRET_SCAN_PASS": secret_pass,
        "secret_scan": secret,
        "COMMIT_VALID": commit_valid,
        "IMAGE_AVAILABLE": image_available,
        "REGISTRY_AVAILABLE": registry != "READY_FOR_CREDENTIALS",
        "IMMUTABLE_DIGEST_AVAILABLE": digest_available,
        "git_status_clean": clean,
        "commit_sha": sha,
        "branch": branch,
        "dirty_state": dirty,
        "git_describe": describe,
        "forbidden_for_certified_release": dirty or not digest_available,
        "image": image,
        "image_id": image_id,
        "image_digest": image_digest,
        "artifact_identity": "DIRTY_SHA" if dirty else sha,
        "artifact_status": "LOCAL_BUILD" if image_available else "NOT_AVAILABLE",
        "registry": "ghcr.io/marpich/marpich-backend",
        "registry_status": registry,
        "ci_digest_wired": ci_digest_wired,
        "helm_digest_helper": helm_digest,
        "vps_image_override": "MEOS_IMAGE" in compose,
        "docker_cli": shutil.which("docker") is not None,
        "compose_is_production": False,
        "g26_not_overridden": True,
        "LOCAL_RELEASE_READY": local_release,
        "REGISTRY_RELEASE_READY": registry_release,
        "DEPLOYMENT_RELEASE_READY": deployment_release,
        "PRODUCTION_RELEASE_READY": production_release,
        "RELEASE_READY": local_release,
        "note": (
            "LOCAL_RELEASE_READY is not PRODUCTION_CERTIFIED. "
            "Local image_id is not a GHCR digest. "
            "Registry digest stays NOT_AVAILABLE until a real CI/GHCR push."
        ),
    }


def main() -> int:
    data = evaluate()
    print(f"WORKTREE_CLEAN={data['WORKTREE_CLEAN']}")
    print(f"TESTS_PASS={data['TESTS_PASS']}")
    print(f"BUILD_PASS={data['BUILD_PASS']}")
    print(f"SECRET_SCAN_PASS={data['SECRET_SCAN_PASS']}")
    print(f"COMMIT_VALID={data['COMMIT_VALID']}")
    print(f"IMAGE_AVAILABLE={data['IMAGE_AVAILABLE']}")
    print(f"REGISTRY_AVAILABLE={data['REGISTRY_AVAILABLE']}")
    print(f"IMMUTABLE_DIGEST_AVAILABLE={data['IMMUTABLE_DIGEST_AVAILABLE']}")
    print(f"LOCAL_RELEASE_READY={data['LOCAL_RELEASE_READY']}")
    print(f"REGISTRY_RELEASE_READY={data['REGISTRY_RELEASE_READY']}")
    print(f"DEPLOYMENT_RELEASE_READY={data['DEPLOYMENT_RELEASE_READY']}")
    print(f"PRODUCTION_RELEASE_READY={data['PRODUCTION_RELEASE_READY']}")
    print(f"RELEASE_READY={data['RELEASE_READY']}")
    print(f"COMMIT_SHA={data['commit_sha']}")
    print(f"IMAGE={data['image']}")
    print(f"IMAGE_ID={data['image_id']}")
    print(f"IMAGE_DIGEST={data['image_digest']}")
    print(f"REGISTRY_STATUS={data['registry_status']}")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["LOCAL_RELEASE_READY"] else 2


if __name__ == "__main__":
    sys.exit(main())
