"""Banking Security Platform domain logic."""
from __future__ import annotations

from contexts.financial_kernel.domain.services.financial_security_engine import (
    checksum_payload,
    compute_tamper_hash,
    encrypt_payload,
    evaluate_abac_policy,
    evaluate_rbac_policy,
    sign_operation,
    verify_tamper,
)

SECURITY_CATALOG: dict[str, dict] = {
    "role_based_access": {"label": "Role Based Access", "supported": True},
    "attribute_based_access": {"label": "Attribute Based Access", "supported": True},
    "maker_checker": {"label": "Maker Checker", "supported": True},
    "four_eyes_principle": {"label": "Four Eyes Principle", "supported": True},
    "transaction_limits": {"label": "Transaction Limits", "supported": True},
    "daily_limits": {"label": "Daily Limits", "supported": True},
    "velocity_checks": {"label": "Velocity Checks", "supported": True},
    "device_verification": {"label": "Device Verification", "supported": True},
    "session_monitoring": {"label": "Session Monitoring", "supported": True},
    "transaction_monitoring": {"label": "Transaction Monitoring", "supported": True},
    "digital_signature": {"label": "Digital Signature", "supported": True},
    "encryption": {"label": "Encryption", "supported": True},
    "risk_based_authentication": {"label": "Risk Based Authentication", "supported": True},
    "emergency_freeze": {"label": "Emergency Freeze", "supported": True},
    "immutable_audit_trail": {"label": "Immutable Audit Trail", "supported": True},
    "policy_driven_approval": {"label": "Policy Driven Approval", "supported": True},
}

SECURITY_POLICY_KEYS: list[dict] = [
    {"key": "security.critical.approval_required", "description": "Critical banking action approval rules"},
    {"key": "security.transaction.limit", "description": "Single transaction limit"},
    {"key": "security.daily.limit", "description": "Daily transaction limit"},
    {"key": "security.velocity.limit", "description": "Velocity check threshold"},
    {"key": "security.device.trust", "description": "Device verification requirements"},
    {"key": "security.risk.threshold", "description": "Risk-based authentication threshold"},
    {"key": "security.emergency.freeze", "description": "Emergency freeze authorization"},
    {"key": "security.maker_checker.rules", "description": "Maker-checker enforcement rules"},
    {"key": "security.four_eyes.levels", "description": "Four-eyes approval levels"},
    {"key": "security.session.timeout", "description": "Session monitoring timeout"},
    {"key": "security.monitoring.threshold", "description": "Transaction monitoring alert threshold"},
]

CRITICAL_ACTIONS = [
    "transfer",
    "withdrawal",
    "loan_disbursement",
    "limit_change",
    "vault_movement",
    "emergency_freeze",
    "policy_change",
]


def list_security_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in SECURITY_CATALOG.items()]


def list_security_policy_keys() -> list[dict]:
    return list(SECURITY_POLICY_KEYS)


def evaluate_access(
    *,
    roles: list[str],
    permission: str,
    attributes: dict,
    rbac_rules: dict,
    abac_rules: dict,
) -> dict:
    rbac_ok = False
    for role in roles:
        if evaluate_rbac_policy(rules=rbac_rules, permission=permission, role=role):
            rbac_ok = True
            break
    if not rbac_ok and roles and not rbac_rules.get("allowed_roles") and not rbac_rules.get("allowed_permissions"):
        rbac_ok = True
    abac_ok = evaluate_abac_policy(rules=abac_rules, attributes=attributes) if abac_rules else True
    allowed = rbac_ok and abac_ok
    return {"allowed": allowed, "rbac": rbac_ok, "abac": abac_ok}


def check_transaction_limit(*, amount: float, single_limit: float) -> tuple[bool, str | None]:
    if single_limit > 0 and amount > single_limit:
        return False, "transaction_limit_exceeded"
    return True, None


def check_daily_limit(*, daily_total: float, amount: float, daily_limit: float) -> tuple[bool, str | None]:
    if daily_limit > 0 and daily_total + amount > daily_limit:
        return False, "daily_limit_exceeded"
    return True, None


def check_velocity(*, velocity_count: int, velocity_limit: int) -> tuple[bool, str | None]:
    if velocity_limit > 0 and velocity_count >= velocity_limit:
        return False, "velocity_limit_exceeded"
    return True, None


def assess_risk(
    *,
    amount: float,
    device_trusted: bool,
    session_risk: float,
    velocity_count: int,
    thresholds: dict,
) -> dict:
    score = 100.0
    factors: list[dict] = []
    large_threshold = float(thresholds.get("large_amount", 25000))
    velocity_limit = int(thresholds.get("velocity_limit", 20))

    if amount >= large_threshold:
        score -= 20
        factors.append({"factor": "large_amount", "impact": -20})
    if not device_trusted:
        score -= 25
        factors.append({"factor": "untrusted_device", "impact": -25})
    if session_risk < 70:
        score -= 15
        factors.append({"factor": "session_risk", "impact": -15})
    if velocity_count >= velocity_limit:
        score -= 30
        factors.append({"factor": "velocity", "impact": -30})

    score = max(0, round(score, 2))
    block_threshold = float(thresholds.get("block_threshold", 30))
    step_up_threshold = float(thresholds.get("step_up_threshold", 60))
    if score < block_threshold:
        level = "block"
    elif score < step_up_threshold:
        level = "step_up"
    else:
        level = "allow"
    return {"risk_score": score, "level": level, "factors": factors}


def resolve_required_approvals(*, action_type: str, amount: float, policy_params: dict) -> int:
    if policy_params.get("always_require_approval"):
        return int(policy_params.get("required_approvals", 1))
    if action_type in CRITICAL_ACTIONS:
        if amount >= float(policy_params.get("four_eyes_amount", 100000)):
            return int(policy_params.get("four_eyes_levels", 2))
        if amount >= float(policy_params.get("approval_amount", 10000)):
            return int(policy_params.get("required_approvals", 1))
    return 0


def build_security_dashboard(
    *,
    approvals: list[dict],
    alerts: list[dict],
    sessions: list[dict],
    freezes: list[dict],
    audits: list[dict],
) -> dict:
    pending = sum(1 for a in approvals if a.get("status") == "pending")
    open_alerts = sum(1 for a in alerts if a.get("status") == "open")
    active_sessions = sum(1 for s in sessions if s.get("status") == "active")
    active_freezes = sum(1 for f in freezes if f.get("status") == "active")
    return {
        "pending_approvals": pending,
        "open_alerts": open_alerts,
        "active_sessions": active_sessions,
        "active_freezes": active_freezes,
        "audit_entries": len(audits),
    }


__all__ = [
    "checksum_payload",
    "compute_tamper_hash",
    "encrypt_payload",
    "sign_operation",
    "verify_tamper",
]
