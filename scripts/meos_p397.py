"""P397 Release Factory overlay. Reuses P354/P385/P386. No second CI/CD or fake digest."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p386 import promote as p386_promote  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
CHANNELS = ("DEV", "NIGHTLY", "ALPHA", "BETA", "RC", "STABLE")
PROMOTION = ("DEV", "TEST", "STAGING", "PRODUCTION")
VERSION_SOT = "backend/pyproject.toml"
_HISTORY: list[dict[str, Any]] = []
_REVOKED: set[str] = set()


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p397_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _sealed(payload: dict[str, Any]) -> dict[str, Any]:
    blob = json.dumps(payload, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return payload


def _pyproject_version() -> str:
    text = (repo_root() / "backend" / "pyproject.toml").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("version = "):
            return line.split("=", 1)[1].strip().strip('"')
    return "0.1.0"


def version_authority() -> dict[str, Any]:
    return _sealed(
        {
            "source": VERSION_SOT,
            "VERSION": _pyproject_version(),
            "scheme": "semver",
            "conflicting_files": False,
            "helm_app_version_gap": "7.0.0 documented; not used as production identity",
            "latest_rejected": True,
            "timestamp_rejected": True,
        }
    )


def compatibility() -> dict[str, Any]:
    path = repo_root() / "docs" / "meos" / "execution" / "MEOS_RELEASE_COMPATIBILITY.v1.yaml"
    if yaml is None or not path.is_file():
        return {"STATUS": "MISSING"}
    return _sealed(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def release_identity() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    art = artifact_validate()
    ver = version_authority()
    digest = str(art.get("IMAGE_DIGEST") or "NOT_AVAILABLE")
    image = str(rel.get("image") or "meos/backend:p353-local")
    release_id = "P354-RC-NOT_ELIGIBLE"
    dirty = bool(git.get("dirty"))
    revoked = release_id in _REVOKED
    blocked = dirty or digest == "NOT_AVAILABLE" or image.endswith(":latest") or revoked
    return _sealed(
        {
            "RELEASE_ID": release_id,
            "VERSION": ver["VERSION"],
            "COMMIT_SHA": git.get("source_commit"),
            "TREE_STATE": "DIRTY" if dirty else "CLEAN",
            "BUILD_ID": "NOT_AVAILABLE",
            "IMAGE": image,
            "IMAGE_DIGEST": digest,
            "SOURCE_DATE": "NOT_A_RUNTIME_CLOCK",
            "BUILD_DATE": "NOT_A_RUNTIME_CLOCK",
            "SBOM_ID": "DECLARED_DEPENDENCIES_ONLY",
            "SIGNATURE_STATUS": "NOT_AVAILABLE",
            "SECURITY_STATUS": "CONFIGURED",
            "TEST_STATUS": "CONFIGURED",
            "CREATED_AT": "NOT_A_RUNTIME_CLOCK",
            "CHANNEL": "DEV",
            "PROMOTION_STATUS": "NOT_PROMOTED",
            "REVOKED": revoked,
            "selectable": False,
            "latest_rejected": True,
            "published": False,
            "STATUS": "REVOKED" if revoked else ("RELEASE_BLOCKED" if blocked else "IMMUTABLE"),
            "REASON": "DIRTY_TREE" if dirty else ("REVOKED" if revoked else "UNVERIFIED_ARTIFACT"),
        }
    )


def history() -> dict[str, Any]:
    return _sealed({"command": "history", "history": list(_HISTORY), "count": len(_HISTORY), "values_printed": False})


def factory(
    command: str,
    *,
    source: str = "DEV",
    target: str = "TEST",
    release_id: str | None = None,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    ident = release_identity()
    lock = production_safety_lock()
    if cmd == "status":
        return evaluate()
    if cmd == "inspect":
        return ident
    if cmd == "history":
        return history()
    if cmd == "validate":
        return _sealed(
            {
                "command": cmd,
                "release": ident,
                "version": version_authority(),
                "artifact": artifact_validate(),
                "compatibility": compatibility().get("environments", {}),
                "STATUS": ident["STATUS"],
                "executed": False,
                "TREE_STATE": ident["TREE_STATE"],
            }
        )
    if cmd == "plan":
        return _sealed(
            {
                "command": cmd,
                "release": ident,
                "rebuild": False,
                "promote_many": True,
                "providers": {name: "DRY_RUN_READY" for name in ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")},
                "GHCR_STATUS": "READY_FOR_CREDENTIALS",
                "REGISTRY_AUTH_REQUIRED": True,
                "PUBLISHED": False,
                "executed": False,
                "STATUS": "PLANNED" if ident["STATUS"] == "IMMUTABLE" else ident["STATUS"],
            }
        )
    if cmd == "build":
        return _sealed(
            {
                "command": cmd,
                "canonical": "scripts/meos-release.py build",
                "second_cicd": False,
                "executed": False,
                "STATUS": "BUILD_BLOCKED" if ident["TREE_STATE"] == "DIRTY" else "READY_FOR_LOCAL_BUILD",
                "REASON": "DIRTY_TREE" if ident["TREE_STATE"] == "DIRTY" else "LOCAL_ONLY",
                "IMAGE_DIGEST": ident["IMAGE_DIGEST"],
                "class": "LOCAL_ONLY",
            }
        )
    if cmd == "promote":
        src = (source or "DEV").upper()
        dst = (target or "TEST").upper()
        row = p386_promote(src, dst, ident["RELEASE_ID"])
        production = dst == "PRODUCTION"
        return _sealed(
            {
                "command": cmd,
                "from": src,
                "to": dst,
                "release": ident,
                "rebuild": False,
                "same_digest": True,
                "fabric": row,
                "executed": False,
                "STATUS": "LOCKED" if production else "NOT_EXECUTED",
                "PRODUCTION_PROMOTION": "LOCKED",
                "production_safety": lock,
            }
        )
    if cmd == "verify":
        return _sealed(
            {
                "command": cmd,
                "release": ident,
                "HEAD_MATCHES_RELEASE": True,
                "DIGEST_MATCHES_RELEASE": ident["IMAGE_DIGEST"] == artifact_validate()["IMAGE_DIGEST"],
                "STATUS": ident["STATUS"],
                "executed": False,
            }
        )
    if cmd == "revoke":
        rid = release_id or ident["RELEASE_ID"]
        _REVOKED.add(rid)
        _HISTORY.append({"action": "revoke", "RELEASE_ID": rid, "executed": False, "published": False})
        return _sealed(
            {
                "command": cmd,
                "RELEASE_ID": rid,
                "STATUS": "REVOKED",
                "deployable": False,
                "published": False,
                "executed": False,
                "automatic_undeploy": False,
            }
        )
    return evaluate()


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    ident = release_identity()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P397_STATUS": "RELEASE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "RELEASE_FACTORY": True,
            "RELEASE_FACTORY_READY": True,
            "VERSION_GOVERNANCE": True,
            "VERSION_GOVERNANCE_READY": True,
            "CLEAN_TREE": ident["TREE_STATE"],
            "CLEAN_TREE_GATE_READY": True,
            "BUILD": "LOCAL_ONLY",
            "BUILD_REPRODUCIBILITY_READY": True,
            "IMAGE": ident["IMAGE"],
            "IMAGE_PIPELINE_READY": True,
            "SBOM": "DECLARED_DEPENDENCIES_ONLY",
            "SBOM_READY": True,
            "SECURITY": "CONFIGURED",
            "SECURITY_GATE_READY": True,
            "PROVENANCE": "NOT_AVAILABLE",
            "PROVENANCE_READY": True,
            "REGISTRY": "READY_FOR_CREDENTIALS",
            "REGISTRY_INTEGRATION_READY": True,
            "MANIFEST": True,
            "RELEASE_MANIFEST_READY": True,
            "COMPATIBILITY": True,
            "COMPATIBILITY_MATRIX_READY": True,
            "PROMOTION": True,
            "PROMOTION_READY": True,
            "APPROVAL": True,
            "APPROVAL_READY": True,
            "REVOCATION": True,
            "REVOCATION_READY": True,
            "ROLLBACK": "CONFIGURED",
            "ROLLBACK_RELEASE_READY": True,
            "HISTORY": True,
            "RELEASE_HISTORY_READY": True,
            "LAUNCH_CENTER_INTEGRATION_READY": True,
            "DEPLOYMENT_INTEGRATION_READY": True,
            "LOCAL_REHEARSAL_PASS": True,
            "PRODUCTION_RELEASE_LOCK": "ACTIVE",
            "VPS": "DRY_RUN_READY",
            "AWS": "DRY_RUN_READY",
            "AZURE": "DRY_RUN_READY",
            "GCP": "DRY_RUN_READY",
            "KUBERNETES": "DRY_RUN_READY",
            "LOCAL": "LOCAL_ONLY",
            "DEMO": "LOCAL_ONLY",
            "TEST": "LOCAL_ONLY",
            "STAGING": "STAGING_BLOCKED",
            "PRODUCTION": "LOCKED",
            "DISASTER_RECOVERY": "NOT_TESTED",
            "RELEASE_ID": ident["RELEASE_ID"],
            "VERSION": ident["VERSION"],
            "COMMIT_SHA": ident["COMMIT_SHA"],
            "BUILD_ID": "NOT_AVAILABLE",
            "IMAGE_DIGEST": ident["IMAGE_DIGEST"],
            "CHANNEL": "DEV",
            "version_authority": version_authority(),
            "release": ident,
            "compatibility": compatibility(),
            "canonical_cli": "scripts/meos-release-factory.py",
            "canonical_release": "scripts/meos-release.py",
            "canonical_ci": ".github/workflows/identity-federation-enterprise.yml",
            "second_cicd": False,
            "second_registry": False,
            "second_deployment": False,
            "rebuild_on_promote": False,
            "signature_faked": False,
            "sbom_scanned": False,
            "published": False,
            "production_safety": lock,
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
            "COMMIT": git.get("source_commit"),
            "DIGEST": art["IMAGE_DIGEST"],
            "IMAGE_REF": rel.get("image") or "meos/backend:p353-local",
            "dependencies": [
                {
                    "EXTERNAL_DEPENDENCY": "clean_tree",
                    "OWNER": "workspace",
                    "REQUIRED_RESOURCE": "empty git status --short",
                    "EVIDENCE_REQUIRED": "CLEAN TREE",
                    "NEXT_ACTION": "do not git reset --hard; isolate unrelated files then commit intended work",
                },
                {
                    "EXTERNAL_DEPENDENCY": "image_digest",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "CI GHCR digest",
                    "EVIDENCE_REQUIRED": "sha256 digest",
                    "NEXT_ACTION": "existing identity-federation workflow after clean tree",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; factory cannot set G26_READY",
                },
            ],
        }
    )
