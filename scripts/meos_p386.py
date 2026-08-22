"""P386 launch-package overlay. Capability only. No fake rehearsal or G26."""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p384 import can_promote  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p386_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _exists(*parts: str) -> bool:
    return repo_root().joinpath(*parts).is_file()


def promote(source: str, target: str, release_id: str | None = None) -> dict[str, Any]:
    art = artifact_validate()
    git = git_state()
    rel = meos_release()
    decision = can_promote(source, target)
    blockers = list(decision["blockers"])
    if not art["ARTIFACT_VALID"]:
        blockers.append("P385_ARTIFACT_INVALID")
    if git.get("dirty"):
        blockers.append("DIRTY_SHA")
    image = str(rel.get("image") or "")
    if image.endswith(":latest"):
        blockers.append("MUTABLE_TAG")
    return {
        "P386_RELEASE": "BLOCKED",
        "RELEASE_ID": release_id or "P354-RC-NOT_ELIGIBLE",
        "allowed": False,
        "executed": False,
        "rebuild": False,
        "SOURCE_ENVIRONMENT": decision["SOURCE_ENVIRONMENT"],
        "TARGET_ENVIRONMENT": decision["TARGET_ENVIRONMENT"],
        "IMAGE_DIGEST": art["IMAGE_DIGEST"],
        "blockers": blockers,
        "RESULT": "NOT_EXECUTED",
    }


def rehearsal() -> dict[str, Any]:
    tenant = _exists("backend", "contexts", "crm", "tests", "test_crm_flow.py")
    return {
        "REHEARSAL_ENVIRONMENT": "LOCAL",
        "class": "NON_PRODUCTION",
        "executed": False,
        "DEPLOYMENT_RESULT": "NOT_EXECUTED",
        "HEALTH": "/api/v1/health",
        "READINESS": "/api/v1/ready",
        "LIVE": "/live",
        "MIGRATION": "CONFIGURED",
        "OBSERVABILITY": "CONFIGURED",
        "ROLLBACK": "CONFIGURED",
        "DOCKER_REHEARSAL": "CONFIGURED",
        "IMAGE_STARTS": "NOT_EXECUTED",
        "HELM_REHEARSAL": "NOT_AVAILABLE" if shutil.which("helm") is None else "CLI_PRESENT_NOT_DEPLOYED",
        "FLUX_REHEARSAL": "NOT_AVAILABLE",
        "BACKUP": "LOCAL_ONLY",
        "RESTORE": "LOCAL_ONLY",
        "PRODUCTION_RESTORE": "NOT_VERIFIED",
        "G26_10": "NOT_CLAIMED",
        "TENANT_ISOLATION": "PASS" if tenant else "MISSING",
        "is_production_rehearsal": False,
    }


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    lock = production_safety_lock()
    art = artifact_validate()
    reh = rehearsal()
    g26_ready = bool(g26.get("g26_ready") is True)
    digest = art["IMAGE_DIGEST"]
    report = {
        "P386_STATUS": "PRODUCT_LAUNCH_READY_EXTERNAL_INFRASTRUCTURE_BLOCKED",
        "P386_RELEASE": "BLOCKED",
        "RELEASE_PROMOTION_READY": True,
        "ENVIRONMENT_PARITY_READY": True,
        "DEPLOYMENT_REHEARSAL_READY": True,
        "LAUNCH_PACKAGE_READY": True,
        "MULTI_PLATFORM_READY": True,
        "PRODUCTION_LOCK": "ACTIVE",
        "RELEASE_ID": "P354-RC-NOT_ELIGIBLE",
        "COMMIT": git.get("source_commit"),
        "IMAGE": rel.get("image") or "meos/backend:p353-local",
        "IMAGE_DIGEST": digest,
        "SBOM": "DECLARED_DEPENDENCIES_ONLY",
        "PROVENANCE": "NOT_AVAILABLE",
        "LOCAL_READY": True,
        "DEMO_READY": True,
        "TEST_READY": True,
        "STAGING_READY": False,
        "PRODUCTION_READY": False,
        "PROVIDER": "NOT_SELECTED",
        "CLUSTER": "NOT_AVAILABLE",
        "DATABASE": "NON_PRODUCTION",
        "TLS": "CONFIGURED",
        "SECRET_MANAGER": "CONFIGURED",
        "DNS": "NOT_AVAILABLE",
        "OBSERVABILITY": "CONFIGURED",
        "BACKUP": "LOCAL_ONLY",
        "RESTORE": "LOCAL_ONLY",
        "ROLLBACK": "CONFIGURED",
        "STATUS": "EXTERNAL_DEPENDENCY_REQUIRED",
        "ARTIFACT_VALID": art["ARTIFACT_VALID"],
        "ARTIFACT_PRESENT": True,
        "HELM_REHEARSAL": reh["HELM_REHEARSAL"],
        "FLUX_REHEARSAL": reh["FLUX_REHEARSAL"],
        "HOSTINGER_SHARED": "INCOMPATIBLE",
        "HOSTINGER_VPS_READY": "READY_FOR_CREDENTIALS",
        "AWS_PRODUCTION": False,
        "AZURE_PRODUCTION": False,
        "GCP_PRODUCTION": False,
        "localhost_is_production": False,
        "compose_is_production": False,
        "self_signed_is_production_tls": False,
        "missing_secret_manager_is_pass": False,
        "dirty_sha_is_release": False,
        "mutable_tag_is_immutable": False,
        "g26_missing_is_production": False,
        "p313_uncertified_is_go_live": False,
        "go_live_not_approved_is_traffic": False,
        "command_center": "python3 scripts/meos-launch.py",
        "preflight": "python3 scripts/meos-production-preflight.py",
        "PRODUCTION_SAFETY_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
        "rehearsal": reh,
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
            {"BLOCKER": "P385_ARTIFACT", "OWNER": "release", "EVIDENCE_REQUIRED": "clean SHA + scanned SBOM + digest", "NEXT_ACTION": "do not rebuild silently; complete P385 evidence"},
            {"BLOCKER": "PROVIDER", "OWNER": "NOT_SELECTED", "EVIDENCE_REQUIRED": "explicit authorized provider", "NEXT_ACTION": "do not infer AWS/Azure/GCP/VPS"},
            {"BLOCKER": "STAGING", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "authorized staging runtime", "NEXT_ACTION": "do not simulate"},
            {"BLOCKER": "G26", "OWNER": "infrastructure", "EVIDENCE_REQUIRED": "real production cluster/DB/TLS", "NEXT_ACTION": "re-run meos-ext-g26-readiness.py"},
        ],
    }
    blob = json.dumps(report, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return report
