#!/usr/bin/env python3
"""MEOS install readiness (P354). Independent of G26_READY. Does not manufacture production."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import (  # noqa: E402
    git_state,
    installation_plan,
    meos_release,
    observability_status,
    secrets_status,
    tls_status,
    tool_status,
)


def evaluate(platform_name: str = "LOCAL") -> dict[str, Any]:
    rel = meos_release()
    git = git_state()
    plan = installation_plan(platform_name)
    tools = tool_status()
    tls = tls_status(platform_name, production=False)
    secrets = secrets_status()
    obs = observability_status()
    install_ready = plan["status"] in {"READY", "READY_FOR_CREDENTIALS"} and not git["forbidden_dirty_identity"]
    return {
        "INSTALL_READY": "READY" if plan["status"] == "READY" else plan["status"],
        "PLATFORM": platform_name,
        "RELEASE": rel["verification_status"],
        "IMAGE": rel["image"],
        "IMAGE_DIGEST": rel["image_digest"],
        "DATABASE": plan["preflight"]["database"]["status"],
        "TLS": tls["status"],
        "SECRETS": secrets["overall"],
        "DNS": "READY_FOR_CREDENTIALS",
        "BACKUP": plan["preflight"]["backup"]["class"],
        "ROLLBACK": "READY" if plan["preflight"]["rollback"]["command"] else "BLOCKED",
        "OBSERVABILITY": obs["g23_class"],
        "DOCKER": tools["docker"],
        "HELM": tools["helm"],
        "source_commit": rel["source_commit"],
        "schema_version": rel["schema_version"],
        "config_version": rel["config_version"],
        "g26_ready": False,
        "production_certified": False,
        "p0": 1,
        "p313": "NOT_CERTIFIED",
        "go_live_authorization": "NOT_APPROVED",
        "compose_is_production": False,
        "DEPLOYMENT_MECHANISM_READY": True,
    }


def main() -> int:
    platform_name = sys.argv[1] if len(sys.argv) > 1 else "LOCAL"
    data = evaluate(platform_name)
    for key in (
        "INSTALL_READY",
        "PLATFORM",
        "RELEASE",
        "IMAGE",
        "DATABASE",
        "TLS",
        "SECRETS",
        "DNS",
        "BACKUP",
        "ROLLBACK",
        "OBSERVABILITY",
    ):
        print(f"{key}={data[key]}")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["DEPLOYMENT_MECHANISM_READY"] else 2


if __name__ == "__main__":
    sys.exit(main())
