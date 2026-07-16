"""Authorization PDP engine — RBAC, ABAC, PBAC cascade."""
from __future__ import annotations

import fnmatch
import re

from contexts.authorization.domain.aggregates.authorization_platform import AuthorizationCapability
from shared.domain.permissions import PermissionEvaluator

POLICY_KEYS = [
    "authorization.rbac.enabled",
    "authorization.abac.enabled",
    "authorization.pbac.enabled",
    "authorization.default_decision",
    "authorization.pbac.policy_key_prefix",
]

CAPABILITY_LABELS = {
    AuthorizationCapability.RBAC_EVALUATION.value: "RBAC Evaluation",
    AuthorizationCapability.ABAC_EVALUATION.value: "ABAC Evaluation",
    AuthorizationCapability.PBAC_EVALUATION.value: "PBAC Evaluation",
    AuthorizationCapability.BATCH_CHECK.value: "Batch Check",
    AuthorizationCapability.DECISION_SIMULATION.value: "Decision Simulation",
    AuthorizationCapability.DECISION_AUDIT.value: "Decision Audit",
    AuthorizationCapability.POLICY_DRIVEN_PDP.value: "Policy-Driven PDP",
    AuthorizationCapability.AUTHORIZATION_DASHBOARD.value: "Authorization Dashboard",
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in AuthorizationCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "authorization", "type": "platform", "label": "Authorization PDP"},
            {"id": "identity", "type": "platform", "label": "Identity"},
            {"id": "policy", "type": "platform", "label": "Policy Engine"},
        ],
        "edges": [
            {"from": "authorization", "to": "identity", "type": "principal_delegate"},
            {"from": "authorization", "to": "policy", "type": "pbac_delegate"},
        ],
        "evaluation_order": ["deny_override", "rbac", "abac", "pbac", "default"],
    }


def resolve_permission_code(
    *,
    permission_code: str | None,
    resource: str,
    action: str,
) -> str:
    if permission_code:
        return permission_code.strip().lower()
    if resource.startswith("marpich://"):
        parts = resource.replace("marpich://", "").split("/")
        module = parts[0] if parts else "platform"
        resource_segment = parts[1] if len(parts) > 1 else "resource"
        return f"{module}.{resource_segment}.{action}".lower()
    if resource and action:
        return f"{resource}.{action}".lower()
    return action.lower()


def evaluate_rbac(*, permissions: list[str], required: str) -> tuple[bool, list[str]]:
    evaluator = PermissionEvaluator()
    if evaluator.has_permission(permissions, required):
        return True, [f"rbac.permission.{required}"]
    return False, [f"rbac.missing.{required}"]


def _match_pattern(pattern: str, permission_code: str) -> bool:
    return fnmatch.fnmatch(permission_code, pattern.lower())


def _evaluate_condition(condition: dict, facts: dict) -> bool:
    attribute = condition.get("attribute", "")
    operator = condition.get("operator", "eq")
    expected = condition.get("value")
    actual = facts.get(attribute)

    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator == "in":
        return actual in (expected or [])
    if operator == "not_in":
        return actual not in (expected or [])
    if operator == "gte":
        return actual is not None and expected is not None and actual >= expected
    if operator == "lte":
        return actual is not None and expected is not None and actual <= expected
    if operator == "gt":
        return actual is not None and expected is not None and actual > expected
    if operator == "lt":
        return actual is not None and expected is not None and actual < expected
    if operator == "matches":
        return bool(actual and re.match(str(expected), str(actual)))
    return False


def evaluate_abac(
    *,
    policies: list[dict],
    permission_code: str,
    facts: dict,
) -> tuple[str | None, list[str], list[str]]:
    """Returns effect (allow/deny/None), reason_codes, matched policy refs."""
    applicable = [
        p for p in policies
        if p.get("active", True) and _match_pattern(p.get("permission_pattern", "*"), permission_code)
    ]
    applicable.sort(key=lambda p: p.get("priority", 100))

    reasons: list[str] = []
    matched_refs: list[str] = []
    for policy in applicable:
        conditions = policy.get("conditions") or []
        if conditions and not all(_evaluate_condition(c, facts) for c in conditions):
            continue
        effect = policy.get("effect", "deny")
        ref = policy.get("policy_ref", "unknown")
        matched_refs.append(ref)
        reasons.append(f"abac.{effect}.{ref}")
        if effect == "deny":
            return "deny", reasons, matched_refs
        if effect == "allow":
            return "allow", reasons, matched_refs
    return None, reasons, matched_refs


def evaluate_pbac(
    *,
    policy_decision: dict | None,
    policy_key: str | None,
) -> tuple[str | None, list[str], list[str]]:
    if not policy_decision or not policy_key:
        return None, [], []
    reasons: list[str] = []
    keys: list[str] = [policy_key]
    if not policy_decision.get("matched"):
        return None, [f"pbac.no_match.{policy_key}"], keys
    outcome = (policy_decision.get("outcome") or "").lower()
    params = policy_decision.get("parameters") or {}
    if outcome in {"deny", "blocked", "reject"}:
        reasons.append(f"pbac.deny.{policy_key}")
        return "deny", reasons, keys
    if params.get("enabled") is False:
        reasons.append(f"pbac.disabled.{policy_key}")
        return "deny", reasons, keys
    if params.get("require_mfa") or params.get("step_up"):
        reasons.append(f"pbac.obligation.mfa.{policy_key}")
        return "allow", reasons + ["pbac.obligation.mfa"], keys
    reasons.append(f"pbac.allow.{policy_key}")
    return "allow", reasons, keys


def evaluate_access(
    *,
    profile: dict | None,
    permissions: list[str],
    abac_policies: list[dict],
    permission_code: str,
    resource: str,
    action: str,
    facts: dict,
    policy_decision: dict | None = None,
    policy_key: str | None = None,
    simulate: bool = False,
) -> dict:
    rbac_enabled = profile.get("rbac_enabled", True) if profile else True
    abac_enabled = profile.get("abac_enabled", True) if profile else True
    pbac_enabled = profile.get("pbac_enabled", True) if profile else True
    default_decision = profile.get("default_decision", "deny") if profile else "deny"

    reason_codes: list[str] = []
    policy_keys: list[str] = []
    obligations: list[str] = []
    models: list[str] = []

    rbac_allowed = True
    if rbac_enabled:
        rbac_allowed, rbac_reasons = evaluate_rbac(permissions=permissions, required=permission_code)
        reason_codes.extend(rbac_reasons)
        models.append("rbac")
        if not rbac_allowed:
            return _decision_payload(
                decision="deny",
                model="rbac",
                reason_codes=reason_codes,
                policy_keys=policy_keys,
                obligations=obligations,
                permission_code=permission_code,
                resource=resource,
                action=action,
                simulate=simulate,
            )

    if abac_enabled:
        abac_effect, abac_reasons, matched = evaluate_abac(
            policies=abac_policies,
            permission_code=permission_code,
            facts=facts,
        )
        reason_codes.extend(abac_reasons)
        if abac_effect:
            models.append("abac")
        if abac_effect == "deny":
            return _decision_payload(
                decision="deny",
                model="abac",
                reason_codes=reason_codes,
                policy_keys=matched,
                obligations=obligations,
                permission_code=permission_code,
                resource=resource,
                action=action,
                simulate=simulate,
            )
        if abac_effect == "allow":
            reason_codes.append("abac.allow")

    if pbac_enabled and policy_key:
        pbac_effect, pbac_reasons, pbac_keys = evaluate_pbac(
            policy_decision=policy_decision,
            policy_key=policy_key,
        )
        policy_keys.extend(pbac_keys)
        reason_codes.extend(pbac_reasons)
        if pbac_effect:
            models.append("pbac")
        if pbac_effect == "deny":
            return _decision_payload(
                decision="deny",
                model="pbac",
                reason_codes=reason_codes,
                policy_keys=policy_keys,
                obligations=obligations,
                permission_code=permission_code,
                resource=resource,
                action=action,
                simulate=simulate,
            )
        if "pbac.obligation.mfa" in pbac_reasons:
            obligations.append("mfa.step_up")

    if rbac_allowed:
        return _decision_payload(
            decision="allow",
            model="+".join(models) if models else "rbac",
            reason_codes=reason_codes or ["rbac.allow"],
            policy_keys=policy_keys,
            obligations=obligations,
            permission_code=permission_code,
            resource=resource,
            action=action,
            simulate=simulate,
        )

    return _decision_payload(
        decision=default_decision,
        model="default",
        reason_codes=reason_codes or [f"default.{default_decision}"],
        policy_keys=policy_keys,
        obligations=obligations,
        permission_code=permission_code,
        resource=resource,
        action=action,
        simulate=simulate,
    )


def _decision_payload(
    *,
    decision: str,
    model: str,
    reason_codes: list[str],
    policy_keys: list[str],
    obligations: list[str],
    permission_code: str,
    resource: str,
    action: str,
    simulate: bool,
) -> dict:
    return {
        "decision": decision,
        "model": model,
        "reason_codes": reason_codes,
        "policy_keys": policy_keys,
        "obligations": obligations,
        "permission_code": permission_code,
        "resource": resource,
        "action": action,
        "simulated": simulate,
    }


def build_dashboard(
    *,
    profile: dict | None,
    policies: list[dict],
    decisions: list[dict],
) -> dict:
    allowed = len([d for d in decisions if d.get("decision") == "allow"])
    denied = len([d for d in decisions if d.get("decision") == "deny"])
    return {
        "summary": {
            "capabilities": len(AuthorizationCapability),
            "abac_policies": len(policies),
            "decisions_total": len(decisions),
            "decisions_allowed": allowed,
            "decisions_denied": denied,
        },
        "profile": profile,
        "recent_decisions": sorted(decisions, key=lambda d: d.get("created_at", ""), reverse=True)[:10],
        "capabilities": list_capability_catalog(),
    }


def generate_seed_data() -> dict:
    return {
        "abac_policies": [
            {
                "name": "Business hours only",
                "effect": "deny",
                "permission_pattern": "banking.*",
                "conditions": [
                    {"attribute": "hour_utc", "operator": "lt", "value": 8},
                ],
                "priority": 10,
            },
            {
                "name": "High device trust for transfers",
                "effect": "allow",
                "permission_pattern": "banking.accounts.*",
                "conditions": [
                    {"attribute": "device_trust", "operator": "eq", "value": "high"},
                ],
                "priority": 20,
            },
        ],
    }
