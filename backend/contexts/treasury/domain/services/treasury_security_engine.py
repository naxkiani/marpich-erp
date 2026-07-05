"""Treasury Security Engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.treasury.domain.aggregates.treasury_security_engine import (
    FreezeScope,
    OperationStatus,
    SecurityPolicyType,
)

SECURITY_CATALOG: dict[str, dict] = {
    SecurityPolicyType.MAKER_CHECKER.value: {
        "label": "Maker Checker",
        "enforcement": "maker_must_differ_from_checker",
    },
    SecurityPolicyType.FOUR_EYES.value: {
        "label": "Four Eyes Principle",
        "enforcement": "minimum_two_distinct_approvers",
    },
    SecurityPolicyType.SEGREGATION_OF_DUTIES.value: {
        "label": "Segregation of Duties",
        "enforcement": "conflicting_roles_blocked",
    },
    SecurityPolicyType.TRANSACTION_LIMITS.value: {
        "label": "Transaction Limits",
        "enforcement": "amount_threshold",
    },
    SecurityPolicyType.APPROVAL_MATRIX.value: {
        "label": "Approval Matrix",
        "enforcement": "role_amount_matrix",
    },
    SecurityPolicyType.DIGITAL_SIGNATURE.value: {
        "label": "Digital Signature",
        "enforcement": "sha256_hash_on_approval",
    },
    SecurityPolicyType.ROLE_BASED_ACCESS.value: {
        "label": "Role Based Access",
        "enforcement": "role_permission_check",
    },
    SecurityPolicyType.ATTRIBUTE_BASED_ACCESS.value: {
        "label": "Attribute Based Access",
        "enforcement": "attribute_policy_check",
    },
    SecurityPolicyType.DEVICE_VERIFICATION.value: {
        "label": "Device Verification",
        "enforcement": "trusted_device_required",
    },
    SecurityPolicyType.RISK_BASED_AUTH.value: {
        "label": "Risk-Based Authentication",
        "enforcement": "risk_score_threshold",
    },
    SecurityPolicyType.TRANSACTION_LOCKING.value: {
        "label": "Transaction Locking",
        "enforcement": "explicit_lock_required",
    },
    SecurityPolicyType.EMERGENCY_FREEZE.value: {
        "label": "Emergency Freeze",
        "enforcement": "tenant_wide_block",
    },
    "security_policies": {"label": "Treasury Security Policies", "supported": True},
    "audit_trail": {"label": "Audit Trail", "audit_all_sensitive": True},
}

SENSITIVE_OPERATIONS = [
    "transfer",
    "payment",
    "investment",
    "cash_movement",
    "bank_account_change",
    "limit_change",
    "policy_change",
    "emergency_freeze",
    "lock_release",
]

SOD_CONFLICTS: dict[str, list[str]] = {
    "treasury_maker": ["treasury_checker", "treasury_approver"],
    "treasury_initiator": ["treasury_approver", "treasury_executor"],
    "cash_handler": ["cash_verifier", "cash_approver"],
}

DEFAULT_RISK_THRESHOLD = 70.0


def list_security_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in SECURITY_CATALOG.items()]


def evaluate_rbac(
    *,
    roles: list[str],
    operation: str,
    rules: list[dict],
) -> dict:
    for rule in rules:
        if not rule.get("is_active", True) or rule.get("rule_type") != "rbac":
            continue
        rule_roles = set(rule.get("roles", []))
        if rule_roles.intersection(roles):
            denied = set(rule.get("denied_operations", []))
            if operation in denied:
                return {"allowed": False, "reason": "role_denied", "rule": rule.get("name")}
            allowed = set(rule.get("allowed_operations", []))
            if allowed and operation in allowed:
                return {"allowed": True, "rule": rule.get("name")}
    if roles:
        return {"allowed": True, "reason": "default_role_access"}
    return {"allowed": False, "reason": "no_matching_role"}


def evaluate_abac(
    *,
    attributes: dict,
    operation: str,
    rules: list[dict],
) -> dict:
    for rule in rules:
        if not rule.get("is_active", True) or rule.get("rule_type") != "abac":
            continue
        rule_attrs = rule.get("attributes", {})
        if all(attributes.get(k) == v for k, v in rule_attrs.items()):
            denied = set(rule.get("denied_operations", []))
            if operation in denied:
                return {"allowed": False, "reason": "attribute_denied", "rule": rule.get("name")}
            allowed = set(rule.get("allowed_operations", []))
            if allowed and operation in allowed:
                return {"allowed": True, "rule": rule.get("name")}
    return {"allowed": True, "reason": "no_abac_restriction"}


def evaluate_device_verification(*, device_verified: bool, policies: list[dict]) -> dict:
    device_policies = [
        p for p in policies
        if p.get("policy_type") == SecurityPolicyType.DEVICE_VERIFICATION.value
        and p.get("is_active", True)
    ]
    if not device_policies:
        return {"verified": True, "required": False}
    if device_verified:
        return {"verified": True, "required": True}
    return {"verified": False, "required": True, "reason": "device_not_verified"}


def evaluate_risk_auth(*, risk_score: float, policies: list[dict]) -> dict:
    threshold = DEFAULT_RISK_THRESHOLD
    for policy in policies:
        if (
            policy.get("policy_type") == SecurityPolicyType.RISK_BASED_AUTH.value
            and policy.get("is_active", True)
        ):
            threshold = policy.get("rules", {}).get("risk_threshold", threshold)

    if risk_score >= threshold:
        return {
            "allowed": False,
            "risk_score": risk_score,
            "threshold": threshold,
            "reason": "risk_score_exceeds_threshold",
            "step_up_required": True,
        }
    return {"allowed": True, "risk_score": risk_score, "threshold": threshold}


def check_maker_checker(*, maker_id: str, checker_id: str) -> dict:
    if maker_id == checker_id:
        return {"valid": False, "reason": "maker_cannot_be_checker"}
    return {"valid": True}


def check_four_eyes(*, approvers: list[str], required: int = 2) -> dict:
    distinct = list(dict.fromkeys(approvers))
    if len(distinct) < required:
        return {
            "valid": False,
            "reason": "insufficient_approvers",
            "required": required,
            "current": len(distinct),
        }
    return {"valid": True, "approver_count": len(distinct)}


def check_segregation_of_duties(*, roles: list[str]) -> dict:
    conflicts = []
    for role in roles:
        conflicting = SOD_CONFLICTS.get(role, [])
        for other in roles:
            if other != role and other in conflicting:
                conflicts.append({"role": role, "conflicts_with": other})
    if conflicts:
        return {"valid": False, "reason": "segregation_violation", "conflicts": conflicts}
    return {"valid": True}


def check_transaction_limit(
    *,
    amount: float,
    operation_type: str,
    limits: list[dict],
) -> dict:
    applicable = [
        lim for lim in limits
        if lim.get("operation_type") == operation_type and lim.get("is_active", True)
    ]
    if not applicable:
        return {"within_limit": True, "reason": "no_limit_configured"}

    for lim in sorted(applicable, key=lambda x: x["max_amount"]):
        if amount <= lim["max_amount"]:
            return {
                "within_limit": True,
                "limit_name": lim.get("name"),
                "max_amount": lim["max_amount"],
            }
    max_lim = applicable[-1]
    return {
        "within_limit": False,
        "reason": "amount_exceeds_limit",
        "max_amount": max_lim["max_amount"],
        "limit_name": max_lim.get("name"),
    }


def resolve_approval_matrix(
    *,
    amount: float,
    operation_type: str,
    matrix: list[dict],
) -> dict:
    applicable = [
        m for m in matrix
        if m.get("operation_type") == operation_type
        and m.get("is_active", True)
        and m.get("min_amount", 0) <= amount <= m.get("max_amount", float("inf"))
    ]
    if not applicable:
        return {"approval_level": 1, "role": "treasury_approver", "matched": False}

    best = max(applicable, key=lambda x: x.get("approval_level", 1))
    return {
        "approval_level": best.get("approval_level", 1),
        "role": best.get("role"),
        "matched": True,
        "matrix_entry": best.get("name", best.get("role")),
    }


def is_emergency_frozen(*, locks: list[dict], tenant_id: str) -> bool:
    return any(
        lock.get("lock_type") == "emergency_freeze"
        and lock.get("subject_ref") == tenant_id
        and lock.get("is_active", True)
        for lock in locks
    )


def is_subject_locked(*, locks: list[dict], subject_ref: str) -> bool:
    return any(
        lock.get("lock_type") == "transaction_lock"
        and lock.get("subject_ref") == subject_ref
        and lock.get("is_active", True)
        for lock in locks
    )


def build_security_dashboard(
    *,
    policies: list[dict],
    limits: list[dict],
    matrix: list[dict],
    operations: list[dict],
    locks: list[dict],
    audits: list[dict],
) -> dict:
    pending = sum(1 for o in operations if o.get("status") == OperationStatus.PENDING_CHECKER.value)
    active_locks = sum(1 for l in locks if l.get("is_active"))
    frozen = is_emergency_frozen(locks=locks, tenant_id=policies[0]["tenant_id"] if policies else "")

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "active_policies": len([p for p in policies if p.get("is_active")]),
            "transaction_limits": len([l for l in limits if l.get("is_active")]),
            "approval_matrix_entries": len([m for m in matrix if m.get("is_active")]),
            "pending_checker_operations": pending,
            "active_locks": active_locks,
            "emergency_frozen": frozen,
            "audit_entries_24h": len(audits),
        },
        "sensitive_operations": SENSITIVE_OPERATIONS,
        "recent_audits": audits[:15],
        "active_locks": [l for l in locks if l.get("is_active")][:10],
    }


def build_security_policies_view(*, policies: list[dict]) -> dict:
    by_type: dict[str, list[dict]] = {}
    for policy in policies:
        pt = policy.get("policy_type", "unknown")
        by_type.setdefault(pt, []).append(policy)

    return {
        "policy_count": len(policies),
        "policy_types": [pt.value for pt in SecurityPolicyType],
        "by_policy_type": by_type,
        "policies": policies,
        "freeze_scopes": [s.value for s in FreezeScope],
    }


def generate_digital_signature_hash(*, operation_id: str, approver_id: str) -> str:
    import hashlib

    payload = f"{operation_id}:{approver_id}:{datetime.now(UTC).isoformat()}"
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


def evaluate_operation_security(
    *,
    maker_id: str,
    checker_id: str | None,
    roles: list[str],
    attributes: dict,
    operation_type: str,
    amount: float,
    risk_score: float,
    device_verified: bool,
    policies: list[dict],
    limits: list[dict],
    matrix: list[dict],
    access_rules: list[dict],
    locks: list[dict],
    tenant_id: str,
) -> dict:
    checks: dict = {}

    if is_emergency_frozen(locks=locks, tenant_id=tenant_id):
        return {"allowed": False, "reason": "emergency_freeze_active", "checks": checks}

    checks["rbac"] = evaluate_rbac(
        roles=roles, operation=operation_type, rules=access_rules
    )
    if not checks["rbac"]["allowed"]:
        return {"allowed": False, "reason": "rbac_denied", "checks": checks}

    checks["abac"] = evaluate_abac(
        attributes=attributes, operation=operation_type, rules=access_rules
    )
    if not checks["abac"]["allowed"]:
        return {"allowed": False, "reason": "abac_denied", "checks": checks}

    checks["sod"] = check_segregation_of_duties(roles=roles)
    if not checks["sod"]["valid"]:
        return {"allowed": False, "reason": "sod_violation", "checks": checks}

    checks["transaction_limit"] = check_transaction_limit(
        amount=amount, operation_type=operation_type, limits=limits
    )
    if not checks["transaction_limit"]["within_limit"]:
        return {"allowed": False, "reason": "limit_exceeded", "checks": checks}

    checks["approval_matrix"] = resolve_approval_matrix(
        amount=amount, operation_type=operation_type, matrix=matrix
    )
    checks["device"] = evaluate_device_verification(
        device_verified=device_verified, policies=policies
    )
    if not checks["device"]["verified"]:
        return {"allowed": False, "reason": "device_not_verified", "checks": checks}

    checks["risk_auth"] = evaluate_risk_auth(risk_score=risk_score, policies=policies)
    if not checks["risk_auth"]["allowed"]:
        return {"allowed": False, "reason": "risk_auth_required", "checks": checks}

    if checker_id:
        checks["maker_checker"] = check_maker_checker(
            maker_id=maker_id, checker_id=checker_id
        )
        if not checks["maker_checker"]["valid"]:
            return {"allowed": False, "reason": "maker_checker_violation", "checks": checks}

    return {"allowed": True, "checks": checks}
