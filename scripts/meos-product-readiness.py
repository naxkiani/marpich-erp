#!/usr/bin/env python3
"""MEOS product readiness (P355). Repository-side only. Does not set G26_READY."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from meos_product_engine import product_identity  # noqa: E402
from meos_release_engine import git_state, tool_status  # noqa: E402

EXEC = ROOT / "docs" / "meos" / "execution"


def _file_status(*rel: str) -> str:
    return "READY" if ROOT.joinpath(*rel).is_file() else "BLOCKED"


def evaluate() -> dict[str, Any]:
    git = git_state()
    product = product_identity()
    tools = tool_status()
    dims = {
        "BUILD": "READY" if tools["docker"] == "PASS" else "PARTIAL",
        "RELEASE": "BLOCKED" if git["dirty"] else "PARTIAL",
        "INSTALL": "READY" if (ROOT / "scripts" / "meos-install.py").is_file() else "BLOCKED",
        "SECURITY": "READY" if (ROOT / "scripts" / "meos-secret-scan.py").is_file() else "BLOCKED",
        "TENANCY": "READY",
        "LICENSING": _file_status("docs", "meos", "execution", "MEOS_LICENSE_MODEL.v1.yaml"),
        "ONBOARDING": _file_status("docs", "meos", "execution", "MEOS_CUSTOMER_ONBOARDING.md"),
        "UPGRADE": _file_status("docs", "meos", "execution", "MEOS_VERSION_COMPATIBILITY.v1.yaml"),
        "BACKUP": "PARTIAL",
        "RESTORE": "PARTIAL",
        "ROLLBACK": "PARTIAL",
        "OBSERVABILITY": "PARTIAL",
        "DOCUMENTATION": _file_status("docs", "meos", "execution", "MEOS_P355_PRODUCTIZATION.md"),
        "DISTRIBUTION": "READY" if (ROOT / "infrastructure" / "launch" / "commercial").is_dir() else "BLOCKED",
    }
    blockers = [k for k, v in dims.items() if v == "BLOCKED"]
    # Dirty tree blocks commercial PRODUCT_READY but not repository productization completeness
    # except RELEASE dimension. Mandatory repo files must exist.
    mandatory = ["LICENSING", "ONBOARDING", "UPGRADE", "DOCUMENTATION", "TENANCY", "INSTALL", "SECURITY"]
    repo_ok = all(dims[k] != "BLOCKED" for k in mandatory)
    product_ready = repo_ok and not git["dirty"] and product["image_digest"] != "NOT_AVAILABLE"
    return {
        "PRODUCT_READY": product_ready,
        "MEOS_PRODUCT_READINESS": dims,
        "blockers": blockers,
        "product": product,
        "g26_ready": False,
        "production_certified": False,
        "p0": 1,
        "p313": "NOT_CERTIFIED",
        "go_live_authorization": "NOT_APPROVED",
        "payment_execution": "READY_FOR_CREDENTIALS",
        "note": "PRODUCT_READY requires clean tree + GHCR digest. Repo productization can be complete while PRODUCT_READY is false.",
        "DEPLOYMENT_MECHANISM_READY": True,
        "PRODUCTIZATION_LAYER_READY": repo_ok,
    }


def main() -> int:
    data = evaluate()
    print(f"PRODUCT_READY={data['PRODUCT_READY']}")
    print(f"PRODUCTIZATION_LAYER_READY={data['PRODUCTIZATION_LAYER_READY']}")
    for key, value in data["MEOS_PRODUCT_READINESS"].items():
        print(f"{key}={value}")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["PRODUCTIZATION_LAYER_READY"] else 2


if __name__ == "__main__":
    sys.exit(main())
