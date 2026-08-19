"""Server-side MEOS product entitlement (P355). Never trust client flags."""
from __future__ import annotations

from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ALLOWED_SUBSCRIPTION = {
    "none": {"", None, "NONE", "TRIAL", "ACTIVE"},
    "trial_or_active": {"TRIAL", "ACTIVE"},
    "active_or_contract": {"ACTIVE"},
    "enterprise_contract": {"ACTIVE"},
}

EDITION_RANKS = {
    "community": 10,
    "professional": 20,
    "business": 30,
    "enterprise": 40,
    "government": 50,
}


def _contracts_dir() -> Path:
    here = Path(__file__).resolve()
    backend = here.parents[3]
    bundled = backend / "shared" / "contracts" / "meos_product"
    if bundled.is_dir():
        return bundled
    repo = here.parents[4]
    return repo / "docs" / "meos" / "execution"


@lru_cache(maxsize=4)
def _load(name: str) -> dict[str, Any]:
    path = _contracts_dir() / name
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def edition_model() -> dict[str, Any]:
    return _load("MEOS_EDITION_MODEL.v1.yaml")


def license_model() -> dict[str, Any]:
    return _load("MEOS_LICENSE_MODEL.v1.yaml")


def version_compatibility() -> dict[str, Any]:
    return _load("MEOS_VERSION_COMPATIBILITY.v1.yaml")


def resolve_edition_features(edition: str) -> set[str]:
    editions = edition_model().get("editions") or {}
    if edition not in editions:
        return set()
    collected: set[str] = set()
    current = edition
    seen: set[str] = set()
    while current and current not in seen:
        seen.add(current)
        spec = editions.get(current) or {}
        collected.update(spec.get("features") or [])
        current = spec.get("includes") or ""
    return collected


def transition_allowed(current: str, target: str) -> bool:
    table = license_model().get("subscription_transitions") or {}
    return target in (table.get(current) or [])


def compatible_schema(application: str, schema: str) -> bool:
    matrix = (version_compatibility().get("compatibility") or {}).get("application_to_database") or {}
    allowed = (matrix.get(application) or {}).get("schema") or []
    return schema in allowed


def validate_license(
    *,
    tenant_id: str,
    feature_id: str,
    license: dict[str, Any] | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Deterministic server-side check. Missing/invalid → BLOCKED / NOT_ENTITLED. No silent downgrade."""
    now = now or datetime.now(UTC)
    editions = edition_model().get("editions") or {}
    if not license:
        community = resolve_edition_features("community")
        if feature_id in community:
            return {"status": "ENABLED", "edition": "community", "reason": "community_default"}
        return {"status": "NOT_ENTITLED", "edition": None, "reason": "license_missing", "invalid_state": "BLOCKED"}

    if license.get("demo") is True and license.get("class") != "DEMO":
        return {"status": "BLOCKED", "reason": "demo_must_be_marked_DEMO", "invalid_state": "BLOCKED"}

    lic_tenant = str(license.get("tenant_id") or "")
    if lic_tenant and lic_tenant != tenant_id:
        return {"status": "BLOCKED", "reason": "tenant_mismatch", "invalid_state": "BLOCKED"}

    edition = str(license.get("edition") or "community")
    if edition not in editions:
        return {"status": "BLOCKED", "reason": "edition_invalid", "invalid_state": "BLOCKED"}

    if license.get("status") in {"SUSPENDED", "CANCELLED", "EXPIRED"}:
        return {
            "status": str(license.get("status")),
            "edition": edition,
            "reason": "license_not_active",
            "invalid_state": "BLOCKED",
        }

    expires = license.get("expires_at")
    if expires:
        exp = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=UTC)
        if now >= exp:
            return {"status": "EXPIRED", "edition": edition, "reason": "expiration_invalid", "invalid_state": "BLOCKED"}

    app_ver = str(license.get("application_version") or "0.1.0")
    schema = str(license.get("schema_version") or "055")
    if not compatible_schema(app_ver, schema):
        return {"status": "BLOCKED", "reason": "version_not_allowed", "invalid_state": "BLOCKED"}

    sub = str(license.get("subscription_state") or "NONE")
    req = str((editions[edition] or {}).get("subscription_requirement") or "none")
    allowed = ALLOWED_SUBSCRIPTION.get(req, {"ACTIVE"})
    if req != "none" and sub not in allowed:
        if sub == "TRIAL" and req == "trial_or_active":
            pass
        elif sub not in allowed:
            return {"status": "NOT_ENTITLED", "edition": edition, "reason": "subscription_not_entitled", "invalid_state": "BLOCKED"}

    features = resolve_edition_features(edition)
    if feature_id not in features:
        return {"status": "NOT_ENTITLED", "edition": edition, "reason": "feature_not_in_edition", "invalid_state": "BLOCKED"}

    if sub == "TRIAL":
        return {"status": "TRIAL", "edition": edition, "reason": "trial"}
    return {"status": "ENABLED", "edition": edition, "reason": "ok"}
