"""MEOS unified launch control (P354 orchestration).

Calls existing Docker/Compose/VPS/Helm/CI/G26 mechanisms.
Does not create a second deployment architecture. Does not print secrets.
Does not set G26_READY. Forbidden override flags cannot bypass production gates.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import (
    FORBIDDEN_DIRTY_IDENTITY,
    git_state,
    identity_ok,
    installation_plan,
    meos_release,
    observability_status,
    production_db_rejected,
    repo_root,
    secrets_status,
    tls_status,
    tool_status,
)

ALLOWED_LAUNCH_STATUS = {
    "NOT_READY",
    "READY_FOR_CREDENTIALS",
    "READY",
    "PLAN_READY",
    "DEPLOYMENT_BLOCKED",
    "DEPLOYED",
    "VERIFICATION_FAILED",
    "VERIFIED",
    "CERTIFICATION_REQUIRED",
    "PRODUCTION_CERTIFIED",
}

FORBIDDEN_OVERRIDES = (
    "--force",
    "--skip-g26",
    "--production-anyway",
    "--ignore-certification",
)

ENV_ALIASES = {
    "local": "LOCAL",
    "demo": "DEMO",
    "vps": "VPS",
    "hostinger-vps": "HOSTINGER_VPS",
    "hostinger_vps": "HOSTINGER_VPS",
    "hostinger": "HOSTINGER_VPS",
    "aws": "AWS",
    "azure": "AZURE",
    "gcp": "GCP",
    "kubernetes": "KUBERNETES",
    "k8s": "KUBERNETES",
    "production": "PRODUCTION",
    "prod": "PRODUCTION",
}

ENV_IDS = (
    "LOCAL",
    "DEMO",
    "VPS",
    "HOSTINGER_VPS",
    "AWS",
    "AZURE",
    "GCP",
    "KUBERNETES",
    "PRODUCTION",
)

CHECK_STATES = {
    "AVAILABLE",
    "MISSING",
    "INVALID",
    "NOT_REQUIRED",
    "NOT_VERIFIED",
    "READY_FOR_CREDENTIALS",
}

CREDENTIAL_ENV = {
    "AWS": ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"),
    "AZURE": ("AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"),
    "GCP": ("GOOGLE_APPLICATION_CREDENTIALS", "GCLOUD_PROJECT"),
    "VPS": ("MEOS_VPS_HOST", "MEOS_VPS_SSH_USER"),
    "HOSTINGER_VPS": ("MEOS_VPS_HOST", "MEOS_HOSTINGER_VPS_HOST"),
}

NON_PROD = frozenset({"LOCAL", "DEMO"})
CLOUD = frozenset({"VPS", "HOSTINGER_VPS", "AWS", "AZURE", "GCP", "KUBERNETES"})

Runner = Callable[..., subprocess.CompletedProcess[str]]


def normalize_env(name: str) -> str:
    raw = (name or "").strip()
    if raw.upper() == "HOSTINGER_SHARED" or raw.lower() in {"hostinger-shared", "shared"}:
        return "HOSTINGER_SHARED"
    key = raw.lower().replace("_", "-")
    if key in ENV_ALIASES:
        return ENV_ALIASES[key]
    upper = raw.upper().replace("-", "_")
    if upper in ENV_IDS:
        return upper
    raise ValueError(f"UNKNOWN_ENVIRONMENT:{raw}")


def refuse_overrides(argv: list[str]) -> dict[str, Any] | None:
    hits = [a for a in argv if a in FORBIDDEN_OVERRIDES]
    if not hits:
        return None
    return {
        "status": "DEPLOYMENT_BLOCKED",
        "reason": "FORBIDDEN_OVERRIDE",
        "flags": hits,
        "g26_ready": False,
        "production_certified": False,
        "executed": False,
        "note": "No override may bypass G26, P313, or GO-LIVE.",
    }


def classify_path(rel: str) -> str:
    p = rel.lstrip(" MADRCU?!").strip()
    if p.endswith(".pyc") or "/__pycache__/" in f"/{p}/" or p.endswith("/__pycache__"):
        return "GENERATED"
    if p.startswith("docs/"):
        return "DOCUMENTATION"
    if "/tests/" in f"/{p}/" or p.startswith("backend/tests/"):
        return "TEST"
    if p.startswith(".meos-backups/") or p.endswith(".sql.gz"):
        return "BUILD_ARTIFACT"
    if p.startswith("deploy/") or p.startswith("scripts/") or p.startswith("infrastructure/"):
        return "SOURCE"
    if p.endswith(".md") or p.endswith(".yaml") or p.endswith(".yml"):
        return "DOCUMENTATION"
    return "SOURCE"


def dirty_report(git: dict[str, Any] | None = None) -> dict[str, Any]:
    git = git or git_state()
    short = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    lines = [ln for ln in (short.stdout or "").splitlines() if ln.strip()]
    files = []
    for line in lines:
        path = line[3:] if len(line) > 3 else line
        files.append({"path": path, "classification": classify_path(path), "raw": line})
    return {
        "worktree_clean": git["worktree_clean"],
        "git_describe": git["git_describe"],
        "forbidden_identity": bool(git["forbidden_dirty_identity"]),
        "dirty": bool(git["dirty"]),
        "files": files,
        "required_action": "Commit or classify; never git reset --hard"
        if files
        else "CLEAN",
        "release_identity": "FORBIDDEN_FOR_RELEASE" if git["dirty"] else "CLEAN_TREE",
    }


def _which_state(binary: str, *, required: bool) -> str:
    found = shutil.which(binary) is not None
    if found:
        return "AVAILABLE"
    return "MISSING" if required else "NOT_REQUIRED"


def _env_set(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return bool(value) and value not in {"CHANGE_ME", "NOT_AVAILABLE", "none"}


def credentials_for(env_id: str) -> dict[str, Any]:
    if env_id in NON_PROD:
        return {"status": "NOT_REQUIRED", "missing": [], "detected": False}
    if env_id == "KUBERNETES":
        kube = Path.home() / ".kube" / "config"
        detected = _env_set("KUBECONFIG") or kube.is_file()
        missing = [] if detected else ["kubeconfig"]
        return {
            "status": "AVAILABLE" if detected else "READY_FOR_CREDENTIALS",
            "missing": missing,
            "detected": detected,
        }
    if env_id == "PRODUCTION":
        return {
            "status": "MISSING",
            "missing": ["EXT-G26", "production cluster"],
            "detected": False,
        }
    names = CREDENTIAL_ENV.get(env_id, ())
    if env_id == "HOSTINGER_VPS":
        detected = _env_set("MEOS_VPS_HOST") or _env_set("MEOS_HOSTINGER_VPS_HOST")
        missing = [] if detected else ["MEOS_VPS_HOST or MEOS_HOSTINGER_VPS_HOST"]
        return {
            "status": "AVAILABLE" if detected else "READY_FOR_CREDENTIALS",
            "missing": missing,
            "detected": detected,
        }
    if env_id == "GCP":
        detected = _env_set("GOOGLE_APPLICATION_CREDENTIALS") or _env_set("GCLOUD_PROJECT")
        missing = [] if detected else ["GOOGLE_APPLICATION_CREDENTIALS", "project"]
        return {
            "status": "AVAILABLE" if detected else "READY_FOR_CREDENTIALS",
            "missing": missing,
            "detected": detected,
        }
    missing = [n for n in names if not _env_set(n)]
    detected = not missing and bool(names)
    return {
        "status": "AVAILABLE" if detected else "READY_FOR_CREDENTIALS",
        "missing": missing,
        "detected": detected,
    }


def g26_snapshot() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_ext_g26_readiness", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate(repo_root())
    return {
        "g26_ready": bool(data.get("g26_ready") is True),
        "g26_status": data.get("g26_status", "BLOCKED"),
        "p0": int(data.get("p0_count", 1)),
        "p313": data.get("p313", "NOT_CERTIFIED"),
        "production_certified": bool(data.get("production_certified") is True),
        "go_live_ready": bool(data.get("go_live_ready") is True),
        "go_live_authorization": str(data.get("go_live_authorization") or "NOT_APPROVED").replace(" ", "_"),
        "active_applications": int(data.get("registry_active_count", 0)),
        "production_traffic": data.get("production_traffic", "NOT_ENABLED"),
    }


def production_gates(g26: dict[str, Any] | None = None) -> dict[str, Any]:
    g26 = g26 or g26_snapshot()
    ok = (
        g26["g26_ready"] is True
        and g26["p313"] == "CERTIFIED"
        and g26["production_certified"] is True
        and g26["go_live_authorization"] in {"APPROVED", "APPROVED"}
        and str(g26["go_live_authorization"]).upper() == "APPROVED"
    )
    blockers = []
    if g26["g26_ready"] is not True:
        blockers.append("G26_READY=FALSE")
    if g26["p313"] != "CERTIFIED":
        blockers.append("P313_NOT_CERTIFIED")
    if g26["production_certified"] is not True:
        blockers.append("PRODUCTION_CERTIFIED=FALSE")
    if str(g26["go_live_authorization"]).upper() != "APPROVED":
        blockers.append("GO_LIVE_AUTHORIZATION_NOT_APPROVED")
    return {"ok": ok, "blockers": blockers, "g26": g26}


def check(name: str, state: str, **extra: Any) -> dict[str, Any]:
    if state not in CHECK_STATES:
        raise ValueError(f"invalid_check_state:{state}")
    row = {"name": name, "state": state}
    row.update(extra)
    return row


def preflight(env_id: str) -> dict[str, Any]:
    try:
        env_id = env_id if env_id == "HOSTINGER_SHARED" else normalize_env(env_id)
    except ValueError:
        env_id = normalize_env(env_id)
    if env_id == "HOSTINGER_SHARED":
        return {
            "environment": "HOSTINGER_SHARED",
            "status": "DEPLOYMENT_BLOCKED",
            "hostinger_shared": "INCOMPATIBLE",
            "blockers": ["HOSTINGER_SHARED_INCOMPATIBLE"],
            "g26_ready": False,
            "production_certified": False,
        }
    git = git_state()
    rel = meos_release()
    tools = tool_status()
    dirty = dirty_report(git)
    creds = credentials_for(env_id)
    g26 = g26_snapshot()
    ident = identity_ok(rel, require_digest=env_id not in NON_PROD)
    docker_state = "AVAILABLE" if tools["docker"] == "PASS" else "MISSING"
    compose_state = "AVAILABLE" if tools["compose"] == "PASS" else "MISSING"
    python_state = "AVAILABLE" if shutil.which("python3") else "MISSING"
    node_state = "NOT_REQUIRED"
    helm_state = "AVAILABLE" if tools["helm"] == "PASS" else (
        "NOT_REQUIRED" if env_id in NON_PROD | {"VPS", "HOSTINGER_VPS"} else "READY_FOR_CREDENTIALS"
    )
    kubectl_state = "AVAILABLE" if tools["kubectl"] == "PASS" else (
        "NOT_REQUIRED" if env_id != "KUBERNETES" and env_id != "PRODUCTION" else "READY_FOR_CREDENTIALS"
    )
    flux_state = "NOT_REQUIRED" if env_id != "KUBERNETES" else (
        "AVAILABLE" if tools["flux"] == "PASS" else "READY_FOR_CREDENTIALS"
    )
    provider_cli = {
        "AWS": "aws",
        "AZURE": "az",
        "GCP": "gcloud",
    }.get(env_id)
    provider_state = "NOT_REQUIRED"
    if provider_cli:
        provider_state = "AVAILABLE" if shutil.which(provider_cli) else "READY_FOR_CREDENTIALS"

    db_host = os.environ.get("PGHOST", "127.0.0.1")
    db_port = os.environ.get("PGPORT", "5433" if env_id == "LOCAL" else ("5444" if env_id == "DEMO" else ""))
    db_prod_illegal = production_db_rejected(db_host, db_port or "0")
    if env_id in NON_PROD:
        db_state = "AVAILABLE"
        db_class = "NON_PRODUCTION"
    elif env_id == "PRODUCTION" or db_prod_illegal:
        db_state = "INVALID" if db_prod_illegal else "MISSING"
        db_class = "LOCALHOST_OR_DEMO_REJECTED" if db_prod_illegal else "PRODUCTION_DB_REQUIRED"
    else:
        db_state = "READY_FOR_CREDENTIALS"
        db_class = "CHANGE_ME"

    tls = tls_status("LOCAL" if env_id in NON_PROD else env_id, production=env_id == "PRODUCTION")
    tls_state = {
        "PASS": "AVAILABLE",
        "BLOCKED": "INVALID",
        "READY_FOR_CREDENTIALS": "READY_FOR_CREDENTIALS",
        "MISSING": "MISSING",
    }.get(tls["status"], "NOT_VERIFIED")
    secrets = secrets_status()
    secret_state = {
        "AVAILABLE": "AVAILABLE",
        "NOT_VERIFIED": "NOT_VERIFIED",
        "MISSING": "MISSING",
    }.get(secrets["overall"], "NOT_VERIFIED")
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    registry_state = "AVAILABLE" if digest.startswith("sha256:") else (
        "NOT_REQUIRED" if env_id in NON_PROD else "READY_FOR_CREDENTIALS"
    )

    checks = [
        check("repository", "AVAILABLE"),
        check("git_cleanliness", "AVAILABLE" if git["worktree_clean"] else "INVALID"),
        check("docker", docker_state, required=env_id in NON_PROD),
        check("docker_compose", compose_state, required=env_id in NON_PROD | {"VPS", "HOSTINGER_VPS"}),
        check("python", python_state),
        check("node", node_state),
        check("database", db_state, classification=db_class, host_class="non_production" if env_id in NON_PROD else db_class),
        check("environment_variables", "AVAILABLE" if env_id in NON_PROD else "NOT_VERIFIED"),
        check("secret_provider", secret_state if env_id not in NON_PROD else "NOT_REQUIRED"),
        check("tls", tls_state),
        check("dns", "NOT_REQUIRED" if env_id in NON_PROD else "READY_FOR_CREDENTIALS"),
        check("registry", registry_state),
        check("credentials", creds["status"] if creds["status"] in CHECK_STATES else "READY_FOR_CREDENTIALS"),
        check("deployment_cli", "AVAILABLE"),
        check("helm", helm_state),
        check("kubectl", kubectl_state),
        check("flux", flux_state),
        check("provider_cli", provider_state),
        check("backup", "AVAILABLE" if (repo_root() / "scripts" / "meos-postgres-backup.sh").is_file() else "MISSING"),
        check("restore", "AVAILABLE" if (repo_root() / "scripts" / "meos-postgres-restore-drill.sh").is_file() else "MISSING"),
        check("rollback", "AVAILABLE"),
        check("observability", "NOT_VERIFIED"),
    ]

    blockers: list[str] = []
    if env_id == "PRODUCTION":
        blockers.extend(production_gates(g26)["blockers"])
        blockers.append("PRODUCTION_DEPLOYMENT_BLOCKED")
    if env_id == "PRODUCTION" and db_prod_illegal:
        blockers.append("LOCALHOST_OR_COMPOSE_DB_NOT_PRODUCTION")
    if FORBIDDEN_DIRTY_IDENTITY in str(git["git_describe"]):
        blockers.append("FORBIDDEN_DIRTY_IDENTITY")
    if env_id not in NON_PROD and git["dirty"]:
        blockers.append("DIRTY_TREE_BLOCKS_RELEASE_DEPLOY")
    if env_id in NON_PROD and docker_state == "MISSING":
        blockers.append("DOCKER_MISSING")
    if env_id in CLOUD and not creds["detected"]:
        pass  # READY_FOR_CREDENTIALS is not a hard local blocker for planning

    if env_id in NON_PROD:
        if docker_state == "MISSING":
            status = "NOT_READY"
        else:
            status = "READY"
    elif env_id == "PRODUCTION":
        status = "DEPLOYMENT_BLOCKED"
    else:
        status = "READY_FOR_CREDENTIALS"

    assert status != "READY" or env_id in NON_PROD
    if status == "READY_FOR_CREDENTIALS":
        assert env_id not in NON_PROD or False
    return {
        "environment": env_id,
        "status": status,
        "checks": checks,
        "blockers": blockers,
        "requirements": _requirements(env_id),
        "credentials": creds,
        "dirty": dirty,
        "release": {
            "source_commit": rel["source_commit"],
            "image": rel["image"],
            "image_digest": digest,
            "forbidden_for_release": bool(git["dirty"]),
        },
        "database_classification": db_class,
        "localhost_is_production": False,
        "compose_is_production": False,
        "hostinger_shared": "INCOMPATIBLE",
        "g26_ready": False,
        "p0": g26["p0"],
        "p313": "NOT_CERTIFIED",
        "production_certified": False,
        "go_live_authorization": "NOT_APPROVED",
        "next_action": _next_action(env_id, status, creds, blockers),
    }


def _requirements(env_id: str) -> list[str]:
    table = {
        "LOCAL": ["Docker", "Compose", "scripts/dev-up.sh"],
        "DEMO": ["Docker", "Compose", "deploy/scripts/meos-demo.sh"],
        "VPS": ["SSH", "Ubuntu", "Docker", "public hostname", "public CA"],
        "HOSTINGER_VPS": ["Hostinger VPS (not shared)", "SSH", "Docker"],
        "AWS": ["AWS credentials", "region", "EC2 or EKS", "RDS"],
        "AZURE": ["Azure identity", "subscription", "VM or AKS", "Key Vault"],
        "GCP": ["GCP identity", "project", "GCE or GKE", "Secret Manager"],
        "KUBERNETES": ["kubeconfig", "Helm", "image.digest", "Ingress"],
        "PRODUCTION": ["G26_READY", "P313 CERTIFIED", "GO_LIVE APPROVED", "immutable digest"],
    }
    return table[env_id]


def _next_action(env_id: str, status: str, creds: dict[str, Any], blockers: list[str]) -> str:
    if env_id == "PRODUCTION":
        return "Supply EXT-G26 evidence. Do not start P313. Do not GO-LIVE."
    if status == "READY":
        return f"python3 scripts/meos-launch.py plan --env {env_id.lower().replace('_', '-')} then deploy --confirm yes"
    if creds.get("missing"):
        return f"Supply credentials: {', '.join(creds['missing'])}"
    if blockers:
        return "Resolve blockers; re-run preflight"
    return "python3 scripts/meos-launch.py plan --env " + env_id.lower().replace("_", "-")


def plan(env_id: str) -> dict[str, Any]:
    env_id = normalize_env(env_id)
    pf = preflight(env_id)
    install = installation_plan(env_id if env_id != "PRODUCTION" else "LOCAL")
    rel = meos_release()
    commands = {
        "LOCAL": ["./deploy/scripts/meos-local.sh start", "./scripts/dev-up.sh"],
        "DEMO": ["./deploy/scripts/meos-demo.sh start"],
        "VPS": ["scripts/meos-vps-bootstrap.sh"],
        "HOSTINGER_VPS": ["reuse deploy/vps after SSH"],
        "AWS": ["EC2 + Docker Compose (P353); EKS uses Helm"],
        "AZURE": ["Azure VM + Docker Compose (P353); AKS uses Helm"],
        "GCP": ["GCE + Docker Compose (P353); GKE uses Helm"],
        "KUBERNETES": ["helm upgrade --install marpich-iam infrastructure/kubernetes/helm/marpich-iam --set-string image.digest=<ci-digest>"],
        "PRODUCTION": ["BLOCKED until G26 + P313 + GO-LIVE"],
    }
    status = "PLAN_READY" if env_id in NON_PROD and pf["status"] == "READY" else (
        "DEPLOYMENT_BLOCKED" if env_id == "PRODUCTION" else "READY_FOR_CREDENTIALS"
    )
    return {
        "TARGET": env_id,
        "REQUIREMENTS": pf["requirements"],
        "DEPENDENCIES": [c["name"] + "=" + c["state"] for c in pf["checks"]],
        "COMMANDS": commands[env_id],
        "ARTIFACT": {
            "COMMIT_SHA": rel["source_commit"],
            "IMAGE": rel["image"],
            "IMAGE_DIGEST": rel["image_digest"],
            "BUILD_ID": rel.get("build_id", "NOT_AVAILABLE"),
        },
        "DATABASE": pf["database_classification"],
        "TLS": tls_status("LOCAL" if env_id in NON_PROD else env_id, production=env_id == "PRODUCTION"),
        "SECRETS": secrets_status()["overall"],
        "NETWORK": "localhost" if env_id in NON_PROD else "CHANGE_ME_PUBLIC_HOSTNAME",
        "BACKUP": "scripts/meos-postgres-backup.sh" if env_id in NON_PROD else "READY_FOR_CREDENTIALS",
        "ROLLBACK": "deploy/scripts/meos-demo.sh stop" if env_id == "DEMO" else (
            "deploy/scripts/meos-local.sh stop" if env_id == "LOCAL" else "MEOS_PREVIOUS_IMAGE or helm rollback marpich-iam 0"
        ),
        "VERIFICATION": [
            "GET /api/v1/health PROCESS",
            "GET /api/v1/ready APPLICATION",
            "python3 scripts/meos-ext-g26-readiness.py PRODUCTION_READINESS",
        ],
        "status": status,
        "executed": False,
        "deployment_occurs": False,
        "preflight_status": pf["status"],
        "blockers": pf["blockers"],
        "install_plan_mode": install["mode"],
        "g26_ready": False,
        "production_certified": False,
        "ready_for_credentials_is_ready": False,
        "confirmation_required": True,
        "next_action": "python3 scripts/meos-launch.py deploy --env "
        + env_id.lower().replace("_", "-")
        + " --confirm yes"
        if env_id in NON_PROD
        else pf["next_action"],
    }


def _http_ok(url: str, timeout: float = 5.0) -> bool:
    try:
        with urlopen(url, timeout=timeout) as resp:
            return 200 <= int(resp.status) < 300
    except (URLError, OSError, ValueError, TimeoutError):
        return False


def verify(env_id: str) -> dict[str, Any]:
    env_id = normalize_env(env_id)
    rel = meos_release()
    git = git_state()
    g26 = g26_snapshot()
    health_url = {
        "LOCAL": "http://127.0.0.1:8000/api/v1/health",
        "DEMO": "http://127.0.0.1:8080/api/v1/health",
    }.get(env_id)
    ready_url = {
        "LOCAL": "http://127.0.0.1:8000/api/v1/ready",
        "DEMO": "http://127.0.0.1:8080/api/v1/ready",
    }.get(env_id)
    health = _http_ok(health_url) if health_url else False
    ready = _http_ok(ready_url) if ready_url else False
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    digest_ok = digest.startswith("sha256:")
    if env_id == "PRODUCTION":
        verified = False
        status = "DEPLOYMENT_BLOCKED"
        reason = "PRODUCTION_REQUIRES_G26_P313_GO_LIVE"
    elif env_id in NON_PROD:
        verified = bool(health and ready)
        status = "VERIFIED" if verified else "VERIFICATION_FAILED"
        reason = "PROCESS_AND_APPLICATION_PROBES" if verified else "HEALTH_OR_READY_FAILED"
        if git["dirty"]:
            # Health may pass; this is not a release verification.
            if verified:
                status = "VERIFIED"
                reason = "NON_PRODUCTION_PROBES_ONLY"
    else:
        verified = False
        status = "READY_FOR_CREDENTIALS"
        reason = "NO_REMOTE_EVIDENCE"
    if env_id not in NON_PROD and not digest_ok:
        status = "READY_FOR_CREDENTIALS" if env_id != "PRODUCTION" else "DEPLOYMENT_BLOCKED"
    return {
        "environment": env_id,
        "COMMIT_SHA": rel["source_commit"],
        "IMAGE": rel["image"],
        "IMAGE_DIGEST": digest,
        "health": health if health_url else "NOT_REQUIRED",
        "readiness": ready if ready_url else "NOT_REQUIRED",
        "tls": "NOT_VERIFIED",
        "dns": "NOT_REQUIRED" if env_id in NON_PROD else "NOT_VERIFIED",
        "database": "NON_PRODUCTION" if env_id in NON_PROD else "NOT_VERIFIED",
        "migration": "NOT_INFERRED_FROM_EXIT_CODE",
        "logs": "CONFIGURED",
        "metrics": "CONFIGURED",
        "alerts": "CONFIGURED_NOT_PRODUCTION_VERIFIED",
        "tenant_isolation": "unit_test_crm_exists",
        "DEPLOYMENT_VERIFIED": verified if env_id in NON_PROD else False,
        "status": status,
        "reason": reason,
        "g26_ready": False,
        "production_certified": False,
        "localhost_is_production": False,
        "compose_is_production": False,
        "g26": g26["g26_status"],
        "p0": g26["p0"],
        "p313": "NOT_CERTIFIED",
    }


def deploy(env_id: str, *, confirm: str = "", runner: Runner | None = None) -> dict[str, Any]:
    env_id = normalize_env(env_id)
    pf = preflight(env_id)
    planned = plan(env_id)
    g26 = production_gates()
    deployment_id = "dep-" + uuid.uuid4().hex[:12]
    base = {
        "DEPLOY_TARGET": env_id,
        "DEPLOYMENT_ID": deployment_id,
        "IMAGE": planned["ARTIFACT"]["IMAGE"],
        "IMAGE_DIGEST": planned["ARTIFACT"]["IMAGE_DIGEST"],
        "COMMIT_SHA": planned["ARTIFACT"]["COMMIT_SHA"],
        "ENVIRONMENT": env_id,
        "BUILD_ID": planned["ARTIFACT"]["BUILD_ID"],
        "preflight": pf["status"],
        "plan_status": planned["status"],
        "g26_ready": False,
        "production_certified": False,
        "go_live_authorization": "NOT_APPROVED",
        "p0": 1,
        "p313": "NOT_CERTIFIED",
    }
    if env_id == "PRODUCTION" or not g26["ok"]:
        if env_id == "PRODUCTION":
            return {
                **base,
                "status": "DEPLOYMENT_BLOCKED",
                "executed": False,
                "CONFIRM": False,
                "blockers": g26["blockers"],
                "note": "Production requires G26_READY + P313 CERTIFIED + GO_LIVE APPROVED. No override.",
            }
    if env_id == "PRODUCTION":
        return {**base, "status": "DEPLOYMENT_BLOCKED", "executed": False}
    if (confirm or "").strip().lower() != "yes":
        return {
            **base,
            "status": "NOT_EXECUTED",
            "executed": False,
            "CONFIRM": False,
            "prompt": (
                f"DEPLOY_TARGET = {env_id}\n"
                f"IMAGE_DIGEST = {planned['ARTIFACT']['IMAGE_DIGEST']}\n"
                f"DATABASE = {planned['DATABASE']}\n"
                f"TLS = {planned['TLS'].get('class')}\n"
                f"BACKUP = {planned['BACKUP']}\n"
                "CONFIRM DEPLOYMENT? [yes/no]"
            ),
            "next_action": "Re-run with --confirm yes after reviewing the plan",
        }
    if env_id in CLOUD:
        return {
            **base,
            "status": "READY_FOR_CREDENTIALS",
            "executed": False,
            "CONFIRM": True,
            "blockers": pf["blockers"] or pf["credentials"]["missing"],
            "note": "Confirmation recorded. External deploy not executed without credentials. Not simulated.",
        }
    if pf["status"] not in {"READY", "PLAN_READY"}:
        return {
            **base,
            "status": "DEPLOYMENT_BLOCKED",
            "executed": False,
            "CONFIRM": True,
            "blockers": pf["blockers"],
        }
    run = runner or subprocess.run
    if env_id == "DEMO":
        script = repo_root() / "deploy" / "scripts" / "meos-demo.sh"
        result = run(["bash", str(script), "start"], cwd=repo_root(), capture_output=True, text=True)
    else:
        script = repo_root() / "deploy" / "scripts" / "meos-local.sh"
        result = run(["bash", str(script), "start"], cwd=repo_root(), capture_output=True, text=True)
    executed = result.returncode == 0
    verification = verify(env_id)
    status = "DEPLOYED" if executed else "DEPLOYMENT_BLOCKED"
    if executed and verification["DEPLOYMENT_VERIFIED"] is not True:
        status = "DEPLOYED"
    return {
        **base,
        "status": status,
        "executed": executed,
        "CONFIRM": True,
        "exit_code": result.returncode,
        "verification": {
            "health": verification["health"],
            "readiness": verification["readiness"],
            "DEPLOYMENT_VERIFIED": verification["DEPLOYMENT_VERIFIED"],
            "note": "Success is not inferred from exit code alone",
        },
        "class": "NON_PRODUCTION",
        "stdout_tail": (result.stdout or "")[-500:],
        "stderr_tail": (result.stderr or "")[-500:],
    }


def rollback(env_id: str, *, confirm: str = "", runner: Runner | None = None) -> dict[str, Any]:
    env_id = normalize_env(env_id)
    if (confirm or "").strip().lower() != "yes":
        return {
            "environment": env_id,
            "status": "NOT_EXECUTED",
            "ROLLBACK_ACTION": "confirmation required",
            "executed": False,
        }
    if env_id == "PRODUCTION":
        return {
            "environment": env_id,
            "status": "DEPLOYMENT_BLOCKED",
            "CURRENT_RELEASE": "NOT_AVAILABLE",
            "PREVIOUS_RELEASE": "NOT_AVAILABLE",
            "ROLLBACK_ACTION": "helm rollback marpich-iam 0 — NOT production-exercised",
            "POST_ROLLBACK_HEALTH": "NOT_AVAILABLE",
            "configured_equals_exercised": False,
            "executed": False,
            "g26_ready": False,
        }
    if env_id in CLOUD:
        return {
            "environment": env_id,
            "status": "READY_FOR_CREDENTIALS",
            "ROLLBACK_ACTION": "MEOS_PREVIOUS_IMAGE or helm rollback marpich-iam 0",
            "POST_ROLLBACK_HEALTH": "NOT_AVAILABLE",
            "configured_equals_exercised": False,
            "executed": False,
        }
    run = runner or subprocess.run
    script = "meos-demo.sh" if env_id == "DEMO" else "meos-local.sh"
    result = run(
        ["bash", str(repo_root() / "deploy" / "scripts" / script), "stop"],
        cwd=repo_root(),
        capture_output=True,
        text=True,
    )
    return {
        "environment": env_id,
        "status": "READY" if result.returncode == 0 else "VERIFICATION_FAILED",
        "ROLLBACK_ACTION": f"./deploy/scripts/{script} stop",
        "POST_ROLLBACK_HEALTH": verify(env_id)["health"],
        "configured_equals_exercised": False,
        "executed": result.returncode == 0,
        "class": "NON_PRODUCTION",
    }


def status(env_id: str | None = None) -> dict[str, Any]:
    rel = meos_release()
    g26 = g26_snapshot()
    git = git_state()
    obs = observability_status()
    env = normalize_env(env_id) if env_id else "ALL"
    rows = {}
    for name in ENV_IDS:
        pf = preflight(name)
        rows[name] = pf["status"]
    return {
        "PRODUCT": "MEOS",
        "VERSION": rel.get("release_version", "0.1.0"),
        "GIT": git["git_describe"],
        "IMAGE": rel["image"],
        "ENVIRONMENT": env,
        "DATABASE": "NON_PRODUCTION_LOCAL_OR_UNVERIFIED",
        "TLS": "NOT_VERIFIED",
        "SECRETS": secrets_status()["overall"],
        "BACKUP": "CONFIGURED",
        "RESTORE": "PASS_LOCAL",
        "ROLLBACK": "CONFIGURED",
        "OBSERVABILITY": obs["g23_class"],
        "DEPLOYMENT": rows.get(env, "READY_FOR_CREDENTIALS") if env != "ALL" else rows,
        "VERIFICATION": "NOT_INFERRED",
        "CERTIFICATION": "NOT_CERTIFIED",
        "status": "CERTIFICATION_REQUIRED",
        "G26": g26["g26_status"],
        "G26_READY": False,
        "P0": 1,
        "P313": "NOT_CERTIFIED",
        "GO_LIVE": "NOT_APPROVED",
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "environments": rows,
        "localhost_is_production": False,
        "compose_is_production": False,
        "ready_for_credentials_is_ready": False,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def list_environments() -> dict[str, Any]:
    items = []
    for env_id in ENV_IDS:
        pf = preflight(env_id)
        items.append(
            {
                "id": env_id,
                "status": pf["status"],
                "credentials": pf["credentials"]["status"],
                "next_action": pf["next_action"],
            }
        )
    return {
        "environments": items,
        "hostinger_shared": "INCOMPATIBLE",
        "g26_ready": False,
        "orchestration_only": True,
        "new_deployment_platform": "FORBIDDEN",
    }
