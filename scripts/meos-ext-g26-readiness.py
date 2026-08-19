#!/usr/bin/env python3
"""MEOS EXT-G26 readiness validator.

Inspects actual evidence. Does not simulate cloud, print secrets, or treat
localhost/compose as production. G26_READY is true only when every required
gate is PASS.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE", "NOT_APPLICABLE"})
GATE_IDS = [f"G26-{i:02d}" for i in range(1, 11)]
LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "0.0.0.0"})
NON_PROD_PORTS = frozenset({"5433", "5444", "8000", "8080"})
SECRET_ENV_NAMES = frozenset(
    {
        "PGPASSWORD",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_ACCESS_KEY_ID",
        "RENDER_API_KEY",
        "JWT_SECRET",
        "DATABASE_URL",
    }
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    return (result.stdout or "").strip()


def _classify_environment(host: str, port: str) -> str:
    host_l = (host or "").strip().lower()
    port_s = str(port or "").strip()
    if host_l in LOCAL_HOSTS or port_s in NON_PROD_PORTS:
        return "LOCAL"
    if host_l in {"", "not_available"}:
        return "NOT_AVAILABLE"
    return "UNKNOWN"


def evaluate(root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    compose = root / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
    ci = root / ".github" / "workflows" / "identity-federation-enterprise.yml"
    helm = root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml"
    kubeconfig = os.environ.get("KUBECONFIG", "").strip()
    kube_home = Path(os.environ.get("MEOS_KUBE_HOME", str(Path.home())))
    home_kube = kube_home / ".kube" / "config"
    cluster_present = bool(kubeconfig and Path(kubeconfig).is_file()) or home_kube.is_file()

    short = _git(["status", "--short"], root)
    describe = _git(["describe", "--always", "--dirty"], root)
    dirty = bool(short) or "dirty" in describe
    commit = _git(["rev-parse", "HEAD"], root) or "NOT_AVAILABLE"

    pghost = os.environ.get("MEOS_PRODUCTION_PGHOST", os.environ.get("PGHOST", "127.0.0.1"))
    pgport = os.environ.get("MEOS_PRODUCTION_PGPORT", os.environ.get("PGPORT", "5433"))
    env_class = _classify_environment(pghost, pgport)
    postgres_is_workstation = env_class == "LOCAL"

    public_ca = os.environ.get("MEOS_PUBLIC_CA_TLS", "").strip() == "1"
    secret_mgr = os.environ.get("MEOS_SECRET_MANAGER_AVAILABLE", "").strip() == "1"
    image_digest = os.environ.get("MEOS_IMAGE_DIGEST", "").strip()
    production_dns = os.environ.get("MEOS_PRODUCTION_DNS", "").strip()
    deployed_commit = os.environ.get("MEOS_DEPLOYED_COMMIT", "").strip()
    deployed_digest = os.environ.get("MEOS_DEPLOYED_DIGEST", "").strip()
    rollback_exercised = os.environ.get("MEOS_ROLLBACK_EXERCISED", "").strip() == "1"
    health_url = os.environ.get("MEOS_HEALTH_URL", "http://127.0.0.1:8000/api/v1/health")

    health_is_local = any(h in health_url for h in ("127.0.0.1", "localhost", "[::1]"))
    production_identity = "LOCAL" if health_is_local or postgres_is_workstation else "UNKNOWN"
    if production_identity == "LOCAL":
        production = False
    else:
        production = False  # UNKNOWN is not PRODUCTION without cluster + digest

    dns_is_local = production_dns.lower() in LOCAL_HOSTS or production_dns == ""

    gates: dict[str, dict[str, str]] = {}
    gates["G26-01"] = {
        "status": "PASS" if cluster_present else "BLOCKED",
        "evidence": "kubeconfig present" if cluster_present else "KUBECONFIG missing; ~/.kube/config absent",
        "blocker": "" if cluster_present else "Authorized production cluster",
    }
    if postgres_is_workstation or env_class == "LOCAL":
        gates["G26-02"] = {
            "status": "BLOCKED",
            "evidence": f"class={env_class} port={pgport} (workstation :5433/:5444 and localhost are NON_PRODUCTION)",
            "blocker": "Managed PostgreSQL host that is not localhost/:5433/:5444",
        }
    else:
        gates["G26-02"] = {
            "status": "PASS",
            "evidence": f"non-local PG class={env_class} port={pgport}",
            "blocker": "",
        }

    if public_ca and not dns_is_local:
        gates["G26-03"] = {"status": "PASS", "evidence": "MEOS_PUBLIC_CA_TLS=1 and non-local DNS", "blocker": ""}
    else:
        gates["G26-03"] = {
            "status": "BLOCKED",
            "evidence": "Public CA not evidenced; compose self-signed is not production TLS",
            "blocker": "Public DNS + public-CA certificate",
        }

    gates["G26-04"] = {
        "status": "PASS" if secret_mgr else "BLOCKED",
        "evidence": "secret manager flagged available" if secret_mgr else "MEOS_SECRET_MANAGER_AVAILABLE unset",
        "blocker": "" if secret_mgr else "Production secret manager",
    }

    if dirty:
        gates["G26-05"] = {
            "status": "FAIL",
            "evidence": f"git status --short not empty; describe={describe}; {describe} FORBIDDEN if dirty",
            "blocker": "Clean working tree then CI digest",
        }
    elif not image_digest:
        gates["G26-05"] = {
            "status": "BLOCKED",
            "evidence": f"clean tree commit={commit}; image digest missing",
            "blocker": "CI image digest",
        }
    else:
        gates["G26-05"] = {
            "status": "PASS",
            "evidence": f"clean commit={commit} digest_present=true",
            "blocker": "",
        }

    ci_exists = ci.is_file()
    if ci_exists and image_digest and not dirty and cluster_present:
        gates["G26-06"] = {"status": "PASS", "evidence": "CI workflow present with digest", "blocker": ""}
    else:
        gates["G26-06"] = {
            "status": "BLOCKED",
            "evidence": "CI workflow DESIGNED" if ci_exists else "CI workflow missing",
            "blocker": "CI deploy credentials and immutable digest",
        }

    if production_dns and not dns_is_local:
        gates["G26-07"] = {"status": "PASS", "evidence": "non-local DNS flag set", "blocker": ""}
    else:
        gates["G26-07"] = {
            "status": "NOT_AVAILABLE",
            "evidence": "No production DNS hostname evidenced",
            "blocker": "Production DNS/ingress",
        }

    if deployed_commit and deployed_digest and cluster_present and not health_is_local:
        gates["G26-08"] = {
            "status": "PASS",
            "evidence": "deployed commit/digest set; health URL not localhost",
            "blocker": "",
        }
    else:
        gates["G26-08"] = {
            "status": "BLOCKED",
            "evidence": "PRODUCTION_RUNTIME not evidenced; local /health is not production",
            "blocker": "Production runtime identity",
        }

    identity_ok = (
        bool(deployed_commit)
        and bool(deployed_digest)
        and not dirty
        and deployed_commit == commit
        and deployed_digest == image_digest
        and bool(image_digest)
    )
    if identity_ok:
        gates["G26-09"] = {"status": "PASS", "evidence": "deployed commit/digest match clean SHA/digest", "blocker": ""}
    else:
        gates["G26-09"] = {
            "status": "NOT_AVAILABLE",
            "evidence": "No matching deployed commit/digest",
            "blocker": "Immutable deployment identity",
        }

    rollback_configured = helm.is_file() and ci.is_file()
    if rollback_exercised and identity_ok:
        gates["G26-10"] = {"status": "PASS", "evidence": "rollback exercised flag plus identity", "blocker": ""}
    else:
        gates["G26-10"] = {
            "status": "BLOCKED",
            "evidence": "Helm rollback CONFIGURED" if rollback_configured else "rollback path missing",
            "blocker": "Exercised production rollback",
        }

    for gid, row in gates.items():
        assert row["status"] in ALLOWED, f"{gid} {row['status']}"

    mandatory_pass = all(gates[gid]["status"] == "PASS" for gid in GATE_IDS)
    g26_ready = bool(mandatory_pass)
    if g26_ready:
        production_identity = "PRODUCTION"
    production = False  # validator never certifies GO-LIVE; identity PRODUCTION ≠ certified

    compose_is_production = False
    if compose.is_file():
        text = compose.read_text(encoding="utf-8").lower()
        if "not a cloud" in text:
            compose_is_production = False

    result = {
        "g26_ready": g26_ready,
        "g26_status": "PASS" if g26_ready else "BLOCKED",
        "p0_count": 1,
        "p313": "NOT_CERTIFIED",
        "p313_auto_start": False,
        "production": production,
        "production_identity": production_identity,
        "production_certified": False,
        "go_live_ready": False,
        "go_live_authorization": "NOT APPROVED",
        "registry_active_count": 0,
        "production_traffic": "NOT_ENABLED",
        "g23": "FAIL",
        "g23_configured": True,
        "g23_production_verified": False,
        "git_describe": describe,
        "git_status_short_empty": not bool(short),
        "forbidden_dirty": dirty,
        "compose_is_production": compose_is_production,
        "localhost_health_is_production": False,
        "gates": gates,
        "p313_reentry": "IF G26_READY THEN STOP P348. START P313 only by explicit re-entry.",
    }
    leaked = [name for name in SECRET_ENV_NAMES if name.lower() in json.dumps(result).lower()]
    if leaked:
        raise RuntimeError("validator output must not include secret env names")
    return result


def main() -> int:
    result = evaluate()
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    print(f"G26_READY={str(result['g26_ready']).upper()}", file=sys.stderr)
    print(f"G26_STATUS={result['g26_status']}", file=sys.stderr)
    print(f"P0={result['p0_count']}", file=sys.stderr)
    print("P313_AUTO_START=false", file=sys.stderr)
    return 0 if result["g26_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
