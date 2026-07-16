"""Zero Trust Federation — continuous verification of every federation request."""
from __future__ import annotations


ZERO_TRUST_CHECKS = (
    "identity",
    "device",
    "application",
    "location",
    "behavior",
    "session",
    "network",
    "organization",
    "risk_score",
    "trust_score",
    "policy",
)


def evaluate_federation_zero_trust(
    *,
    identity_verified: bool = False,
    device_trusted: bool = False,
    application_trusted: bool = True,
    location_allowed: bool = True,
    behavior_anomaly: bool = False,
    session_valid: bool = True,
    network_trusted: bool = True,
    organization_trusted: bool = True,
    risk_score: int = 0,
    trust_score: int = 50,
    policy_allowed: bool = True,
    step_up_threshold: int = 70,
    deny_threshold: int = 90,
) -> dict:
    """No implicit trust — evaluate every dimension before federation proceeds."""
    checks = {
        "identity": identity_verified,
        "device": device_trusted,
        "application": application_trusted,
        "location": location_allowed,
        "behavior": not behavior_anomaly,
        "session": session_valid,
        "network": network_trusted,
        "organization": organization_trusted,
        "risk_score": risk_score < deny_threshold,
        "trust_score": trust_score >= 40,
        "policy": policy_allowed,
    }
    failed = [k for k, ok in checks.items() if not ok]
    effective_risk = risk_score
    if not identity_verified:
        effective_risk += 25
    if not device_trusted:
        effective_risk += 20
    if behavior_anomaly:
        effective_risk += 15
    if not organization_trusted:
        effective_risk += 10
    effective_risk = min(100, effective_risk)

    if not policy_allowed or effective_risk >= deny_threshold or "identity" in failed:
        action = "deny"
    elif effective_risk >= step_up_threshold or failed:
        action = "step_up"
    else:
        action = "allow"

    return {
        "allowed": action == "allow",
        "action": action,
        "checks": [{"dimension": k, "passed": v} for k, v in checks.items()],
        "failed_dimensions": failed,
        "risk_score": effective_risk,
        "trust_score": trust_score,
        "principles": [
            "never_trust",
            "always_verify",
            "least_privilege",
            "continuous_verification",
            "assume_breach",
        ],
        "policy_decision_flow": [
            "collect_context",
            "evaluate_dimensions",
            "compute_risk_trust",
            "apply_policy",
            "decide_allow_step_up_deny",
            "audit",
        ],
        "trust_evaluation_flow": [
            "load_identity_trust",
            "load_device_trust",
            "load_organization_trust",
            "compose_hierarchy",
            "propagate_graph",
            "emit_decision",
        ],
    }


def secure_defaults() -> dict:
    return {
        "mtls_required": True,
        "pkce_required": True,
        "nonce_required": True,
        "state_required": True,
        "audience_validation": True,
        "replay_protection": True,
        "token_encryption": "JWE_optional",
        "signature_algorithms": ["RS256", "ES256"],
        "certificate_pinning": True,
        "origin_validation": True,
    }
