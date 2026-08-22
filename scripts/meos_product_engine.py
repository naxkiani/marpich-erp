#!/usr/bin/env python3
"""MEOS productization engine (P355). No fake customers, payments, or production tenants."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from meos_release_engine import git_state, meos_release  # noqa: E402


ONBOARDING_STEPS = (
    "TENANT_CREATED",
    "IDENTITY_CONFIGURED",
    "EDITION_ASSIGNED",
    "LICENSE_ASSIGNED",
    "CONFIGURATION_INITIALIZED",
    "ADMIN_CREATED",
    "SECURITY_CONFIGURED",
    "READY",
)

CHANNELS = ("DEV", "ALPHA", "BETA", "RC", "STABLE", "LTS")


def product_identity() -> dict[str, Any]:
    rel = meos_release()
    git = git_state()
    channel = "DEV" if git["dirty"] else "RC"
    if git["forbidden_dirty_identity"] or git["dirty"]:
        release_status = "FORBIDDEN_DIRTY"
    else:
        release_status = "CANDIDATE"
    return {
        "product_id": "meos",
        "product_name": "Marpich Enterprise Operating System",
        "product_version": rel["release_version"],
        "release_channel": channel,
        "edition": "community",
        "release_status": release_status,
        "supported_platforms": rel["supported_platforms"],
        "minimum_requirements": {
            "python": "3.12",
            "postgres": "16",
            "docker": "compose-v2",
        },
        "license_model": "docs/meos/execution/MEOS_LICENSE_MODEL.v1.yaml",
        "subscription_model": "LICENSE_DESIGN_ONLY",
        "feature_profile": "docs/meos/execution/MEOS_EDITION_MODEL.v1.yaml",
        "build_id": rel["build_id"],
        "source_commit": rel["source_commit"],
        "image_digest": rel["image_digest"],
        "schema_version": rel["schema_version"],
        "configuration_version": rel["config_version"],
        "commercial_release": False,
        "g26_ready": False,
    }


def onboarding_plan(*, authorize_create_tenant: bool, production: bool) -> dict[str, Any]:
    blocked: list[str] = []
    if production:
        blocked.append("PRODUCTION_TENANT_REQUIRES_EXPLICIT_AUTHORIZATION_AND_G26")
    if not authorize_create_tenant:
        blocked.append("PLAN_ONLY_NO_TENANT_CREATED")
    return {
        "flow": list(ONBOARDING_STEPS),
        "reuses": [
            "contexts.identity",
            "contexts.organization",
            "contexts.settings",
            "contexts.feature_flags",
            "contexts.audit",
            "contexts.notifications",
        ],
        "mode": "PLAN_ONLY" if not authorize_create_tenant else "BLOCKED_IF_PRODUCTION",
        "production_tenant_created": False,
        "blocked": blocked,
        "g26_ready": False,
    }


def upgrade_plan(current: str, target: str | None) -> dict[str, Any]:
    return {
        "CURRENT_VERSION": current,
        "TARGET_VERSION": target or "NOT_AVAILABLE",
        "MIGRATION_PLAN": "scripts/meos-migration-check.sh then scripts/run-migrations.sh",
        "BACKUP_REQUIRED": True,
        "ROLLBACK_SUPPORTED": True,
        "UPGRADE_STATUS": "DESIGNED",
        "ROLLBACK_TESTED": False,
    }


def channel_promotion_allowed(source: str, dest: str) -> bool:
    order = list(CHANNELS)
    if source not in order or dest not in order:
        return False
    return order.index(dest) == order.index(source) + 1


if __name__ == "__main__":
    print(json.dumps(product_identity(), indent=2, sort_keys=True))
