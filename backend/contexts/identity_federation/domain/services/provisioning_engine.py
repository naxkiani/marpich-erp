"""Provisioning engine — JIT provisioning, role assignment, de-provisioning."""
from __future__ import annotations

from typing import Any


def evaluate_jit_provisioning(
    *,
    jit_enabled: bool,
    claims: dict[str, Any],
    rules: list[dict],
    default_roles: list[str] | None = None,
) -> dict:
    """Just-in-time user provisioning decision."""
    if not jit_enabled:
        return {"provision": False, "reason": "jit_disabled"}

    email = claims.get("email")
    if not email:
        return {"provision": False, "reason": "missing_email"}

    roles = list(default_roles or [])
    for rule in rules:
        if not rule.get("enabled", True):
            continue
        claim_key = rule.get("claim", "")
        expected = rule.get("value")
        if claim_key and claims.get(claim_key) == expected:
            roles.extend(rule.get("roles", []))

    return {
        "provision": True,
        "provisioning_mode": "jit",
        "email": email,
        "display_name": claims.get("name") or claims.get("display_name") or email.split("@")[0],
        "roles": list(dict.fromkeys(roles)),
        "attributes": {k: v for k, v in claims.items() if k.startswith("attr_")},
    }


def evaluate_deprovisioning(
    *,
    external_status: str | None,
    last_sync_at: str | None,
    inactive_days: int = 0,
    deprovision_threshold_days: int = 90,
) -> dict:
    """De-provisioning decision based on external account state."""
    if external_status in ("disabled", "suspended", "deleted"):
        return {"deprovision": True, "reason": f"external_status_{external_status}"}
    if inactive_days >= deprovision_threshold_days:
        return {"deprovision": True, "reason": "inactive_threshold_exceeded"}
    return {"deprovision": False, "reason": "active"}


def sync_provisioning_action(
    *,
    direction: str,
    records: list[dict],
) -> dict:
    """Batch sync provisioning summary."""
    created = updated = failed = 0
    for record in records:
        action = record.get("action", "skip")
        if action == "create":
            created += 1
        elif action == "update":
            updated += 1
        elif action == "fail":
            failed += 1
    return {
        "direction": direction,
        "records_processed": len(records),
        "created": created,
        "updated": updated,
        "failed": failed,
    }
