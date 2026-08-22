"""P385 supply-chain factory overlay. No fake SBOM, digest, signature, or G26."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
SBOM = "infrastructure/launch/MEOS_RELEASE_PACKAGE/SBOM.declared.json"
MANIFEST = "docs/meos/execution/MEOS_RELEASE_MANIFEST.v1.yaml"
EVIDENCE_INDEX = "infrastructure/launch/MEOS_RELEASE_PACKAGE/evidence/INDEX.yaml"


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p385_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _exists(*parts: str) -> bool:
    return repo_root().joinpath(*parts).is_file()


def _sha256(rel: str) -> dict[str, Any]:
    path = repo_root() / rel
    if not path.is_file():
        return {"file": rel, "sha256": "MISSING", "size": 0}
    data = path.read_bytes()
    return {"file": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def _sbom_status() -> dict[str, Any]:
    path = repo_root() / SBOM
    if not path.is_file():
        return {"SBOM": "NOT_AVAILABLE", "SBOM_FORMAT": "NOT_AVAILABLE", "generated": False}
    payload = json.loads(path.read_text(encoding="utf-8"))
    status = str(payload.get("SBOM_STATUS") or "DECLARED_DEPENDENCIES_ONLY")
    return {
        "SBOM": status,
        "SBOM_FORMAT": payload.get("bomFormat") or "NOT_AVAILABLE",
        "SBOM_PATH": SBOM,
        "SBOM_SHA256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "generated": status == "SCANNED",
        "tool_executed": False,
        "syft": shutil.which("syft") is not None,
        "cyclonedx": shutil.which("cyclonedx-py") is not None or shutil.which("cyclonedx") is not None,
    }


def artifact_validate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    sbom = _sbom_status()
    required = {
        "manifest": _exists("docs", "meos", "execution", "MEOS_RELEASE_MANIFEST.v1.yaml"),
        "commit": str(git.get("source_commit") or "") not in {"", "NOT_AVAILABLE"},
        "image_reference": bool(rel.get("image")),
        "digest": digest.startswith("sha256:"),
        "sbom": sbom["SBOM"] != "NOT_AVAILABLE",
        "sbom_scanned": sbom["generated"],
        "provenance": False,
        "security_scan_evidence": False,
        "secret_scan_script": _exists("scripts", "meos-secret-scan.py"),
        "checksums": _exists("infrastructure", "launch", "MEOS_RELEASE_PACKAGE", "checksums", "P383.SHA256"),
    }
    invented = digest not in {"NOT_AVAILABLE", "None", ""} and not digest.startswith("sha256:")
    valid = all((
        required["manifest"],
        required["commit"],
        required["digest"],
        required["sbom_scanned"],
        required["provenance"],
        not git.get("dirty"),
        not invented,
    ))
    return {
        "ARTIFACT_VALID": valid,
        "ARTIFACT_VALIDATION_READY": True,
        "required": required,
        "invented_digest": invented,
        "IMAGE_DIGEST": digest if digest.startswith("sha256:") else "NOT_AVAILABLE",
        "IMAGE_DIGEST_SOURCE": "NOT_AVAILABLE",
        "sbom": sbom,
        "G26_READY_IS_NOT_ARTIFACT_VALID": True,
    }


def quality_gate() -> dict[str, Any]:
    ignored = []
    for name in ("FORCE_RELEASE", "BYPASS_SECURITY", "FORCE_PRODUCTION"):
        if os.environ.get(name, "").strip() in {"1", "true", "TRUE", "yes"}:
            ignored.append(f"{name}_IGNORED")
    git = git_state()
    art = artifact_validate()
    gates = {
        "SOURCE": "FAIL" if git.get("dirty") else "PASS",
        "BUILD": "LOCAL_IMAGE",
        "TEST": "NOT_MEASURED",
        "SECURITY": "CONFIGURED",
        "SECRET_SCAN": "CONFIGURED",
        "SBOM": art["sbom"]["SBOM"],
        "PROVENANCE": "NOT_AVAILABLE",
        "ARTIFACT": "FAIL" if not art["ARTIFACT_VALID"] else "PASS",
        "MANIFEST": "PASS" if art["required"]["manifest"] else "FAIL",
    }
    quality = "PASS" if all(v == "PASS" for v in gates.values()) else "FAIL"
    return {
        "RELEASE_QUALITY": quality,
        "gates": gates,
        "ignored_overrides": ignored,
        "default_pass": False,
    }


def evidence_bundle() -> dict[str, Any]:
    files = [
        MANIFEST,
        SBOM,
        EVIDENCE_INDEX,
        "docs/meos/execution/MEOS_RELEASE_SUPPLY_CHAIN.v1.yaml",
        "docs/meos/execution/MEOS_RELEASE_EVIDENCE_SPEC.v1.yaml",
        "scripts/meos-secret-scan.py",
    ]
    items = [_sha256(rel) for rel in files]
    return {
        "root": "infrastructure/launch/MEOS_RELEASE_PACKAGE/evidence",
        "repo_root_evidence": "NOT_CREATED",
        "immutable_after_release": "REQUIRED_WHEN_RELEASE_EXISTS",
        "items": items,
        "CHECKSUMS_READY": all(row["sha256"] != "MISSING" for row in items),
        "manual_entry": False,
    }


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    lock = production_safety_lock()
    art = artifact_validate()
    quality = quality_gate()
    evidence = evidence_bundle()
    sbom = art["sbom"]
    g26_ready = bool(g26.get("g26_ready") is True)
    digest = art["IMAGE_DIGEST"]
    report = {
        "P385_STATUS": "SUPPLY_CHAIN_READY",
        "CLEAN_RELEASE": "BLOCKED" if git.get("dirty") else "READY",
        "BUILD": "LOCAL_IMAGE",
        "TEST": "NOT_MEASURED",
        "SECURITY_SCAN": "CONFIGURED",
        "SECRET_SCAN": "CONFIGURED",
        "SBOM": sbom["SBOM"],
        "PROVENANCE": "NOT_AVAILABLE",
        "IMAGE": rel.get("image") or "meos/backend:p353-local",
        "IMAGE_DIGEST": digest,
        "SIGNATURE": "READY_FOR_CREDENTIALS",
        "ARTIFACT_VALIDATION": "READY",
        "ARTIFACT_VALID": art["ARTIFACT_VALID"],
        "RELEASE_MANIFEST": "READY",
        "CHECKSUMS": "READY" if evidence["CHECKSUMS_READY"] else "BLOCKED",
        "RELEASE_EVIDENCE": "READY",
        "RELEASE_FACTORY_READY": True,
        "ARTIFACT_VALIDATION_READY": True,
        "SBOM_READY": True,
        "PROVENANCE_READY": True,
        "SECURITY_GATE_READY": True,
        "RELEASE_EVIDENCE_READY": True,
        "RELEASE_QUALITY": quality["RELEASE_QUALITY"],
        "GHCR_PUSH": "BLOCKED",
        "REGISTRY_PUSH": "BLOCKED",
        "SIGNING": "READY_FOR_CREDENTIALS",
        "STATUS": "EXTERNAL_DEPENDENCY_REQUIRED",
        "PRODUCTION_SAFETY_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
        "LOCAL_IS_NOT_PRODUCTION": True,
        "DEMO_IS_NOT_PRODUCTION": True,
        "COMPOSE_IS_NOT_PRODUCTION": True,
        "RELEASE_READY_IS_NOT_PRODUCTION_CERTIFIED": True,
        "command_center": "python3 scripts/meos-launch.py",
        "canonical_ci": ".github/workflows/identity-federation-enterprise.yml",
        "repo_root_release": "FORBIDDEN",
        "quality": quality,
        "artifact": art,
        "evidence": {"CHECKSUMS_READY": evidence["CHECKSUMS_READY"], "root": evidence["root"]},
        "G26_STATUS": g26.get("g26_status", "BLOCKED"),
        "G26_READY": g26_ready,
        "P0": int(g26.get("p0_count", 1)),
        "P313": "NOT_CERTIFIED",
        "P313_REENTRY_READY": bool(g26_ready),
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "blockers": [
            {"BLOCKER": "DIRTY_SHA", "OWNER": "workspace", "EVIDENCE_REQUIRED": "empty git status --short", "NEXT_ACTION": "do not git reset --hard; commit or isolate unrelated files"},
            {"BLOCKER": "image_digest", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI GHCR digest", "NEXT_ACTION": "clean tree then existing CI publish"},
            {"BLOCKER": "SBOM_SCANNED", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "syft/anchore execution", "NEXT_ACTION": "reuse CI sbom-action; do not invent SPDX"},
            {"BLOCKER": "PROVENANCE", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI provenance attestation", "NEXT_ACTION": "record when CI produces it"},
            {"BLOCKER": "SIGNATURE", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "approved signing credentials", "NEXT_ACTION": "SIGNING remains READY_FOR_CREDENTIALS"},
        ],
    }
    blob = json.dumps(report, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return report
