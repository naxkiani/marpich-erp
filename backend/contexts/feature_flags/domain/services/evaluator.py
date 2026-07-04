"""Feature flag evaluation engine."""
from __future__ import annotations

import hashlib

from contexts.feature_flags.domain.aggregates.feature_flag import FeatureFlag


def _bucket(key: str, stable_id: str) -> int:
    digest = hashlib.sha256(f"{key}:{stable_id}".encode()).hexdigest()
    return int(digest[:8], 16) % 100


def _pick_variant(flag: FeatureFlag, bucket: int) -> str | None:
    if not flag.ab_test_enabled or not flag.ab_variants:
        return None
    total = sum(v.get("weight", 0) for v in flag.ab_variants) or 100
    point = bucket % total
    cumulative = 0
    for variant in flag.ab_variants:
        cumulative += variant.get("weight", 0)
        if point < cumulative:
            return variant.get("id")
    return flag.ab_variants[0].get("id")


def evaluate_flag(flag: FeatureFlag, context: dict) -> dict:
    if flag.emergency_disabled:
        return {
            "enabled": False,
            "variant_id": None,
            "reason": "emergency_disabled",
            "flag_version": flag.version,
        }

    user_id = context.get("user_id")
    org_id = context.get("organization_id")
    tenant_id = context.get("tenant_id") or flag.tenant_id
    environment = context.get("environment")
    country = context.get("country")
    industry = context.get("industry_pack")

    if user_id and user_id in flag.user_rules:
        enabled = flag.user_rules[user_id]
        return _result(flag, enabled, "user", None)

    if org_id and org_id in flag.organization_rules:
        enabled = flag.organization_rules[org_id]
        return _result(flag, enabled, "organization", None)

    if tenant_id in flag.tenant_rules:
        enabled = flag.tenant_rules[tenant_id]
        return _result(flag, enabled, "tenant", None)

    if country and country in flag.country_rules:
        enabled = flag.country_rules[country]
        return _result(flag, enabled, "country", None)

    if industry and industry in flag.industry_rules:
        enabled = flag.industry_rules[industry]
        return _result(flag, enabled, "industry", None)

    if environment and environment in flag.environment_rules:
        enabled = flag.environment_rules[environment]
        return _result(flag, enabled, "environment", None)

    stable_id = user_id or tenant_id or "anonymous"
    bucket = _bucket(flag.key, stable_id)

    if flag.rollout_stage in ("canary", "off") or flag.rollout_percentage < 100:
        if bucket >= flag.rollout_percentage:
            return _result(flag, False, "rollout", None)

    variant_id = _pick_variant(flag, bucket)
    if variant_id:
        return _result(flag, True, "ab_test", variant_id)

    return _result(flag, flag.default_enabled, "default", None)


def _result(flag: FeatureFlag, enabled: bool, reason: str, variant_id: str | None) -> dict:
    return {
        "enabled": enabled,
        "variant_id": variant_id,
        "reason": reason,
        "flag_version": flag.version,
    }
