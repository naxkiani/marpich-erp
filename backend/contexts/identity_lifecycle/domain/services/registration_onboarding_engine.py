"""Registration validation, duplicate detection, ZT gates (P201-A)."""
from __future__ import annotations

import re
from typing import Any

from contexts.identity_lifecycle.domain.aggregates.registration_onboarding import (
    SUPPORTED_IDENTITY_TYPES,
    ApprovalMode,
    IdentityRegistration,
    RegistrationChannel,
    RegistrationStatus,
)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def catalog() -> dict:
    return {
        "prompt": "P201-A",
        "adr": 227,
        "identity_types": sorted(SUPPORTED_IDENTITY_TYPES),
        "channels": [c.value for c in RegistrationChannel],
        "statuses": [s.value for s in RegistrationStatus],
        "approval_modes": [a.value for a in ApprovalMode],
        "workflow_steps": [
            "registration_requested",
            "validation",
            "duplicate_detection",
            "risk_evaluation",
            "policy_evaluation",
            "approval",
            "identity_creation",
            "profile_initialization",
            "provisioning_request",
            "welcome_workflow",
            "activation_request",
        ],
        "not": [
            "authorization_pdp",
            "identity_governance_iga",
            "federation_idp_sdk",
            "contexts_eilmp",
        ],
    }


def validate_registration_input(reg: IdentityRegistration) -> list[str]:
    errors: list[str] = []
    if reg.identity_type not in SUPPORTED_IDENTITY_TYPES:
        errors.append("registration.invalid_identity_type")
    if reg.channel not in {c.value for c in RegistrationChannel}:
        errors.append("registration.invalid_channel")
    if not reg.email or not _EMAIL_RE.match(reg.email):
        errors.append("registration.invalid_email")
    if not reg.display_name or len(reg.display_name) < 2:
        errors.append("registration.invalid_display_name")
    if not reg.tenant_id:
        errors.append("registration.tenant_required")
    return errors


def evaluate_zero_trust(zt_context: dict[str, Any] | None) -> dict:
    ctx = dict(zt_context or {})
    risk = float(ctx.get("risk_score", 25))
    device_trusted = bool(ctx.get("device_trusted", True))
    network_trusted = bool(ctx.get("network_trusted", True))
    location_ok = bool(ctx.get("location_allowed", True))
    identity_evidence = bool(ctx.get("identity_evidence", True))
    passed = (
        risk < 80
        and device_trusted
        and network_trusted
        and location_ok
        and identity_evidence
    )
    trust = "high" if risk < 30 and passed else "medium" if passed else "low"
    return {
        "passed": passed,
        "risk_score": risk,
        "trust_level": trust,
        "checks": {
            "device_trusted": device_trusted,
            "network_trusted": network_trusted,
            "location_allowed": location_ok,
            "identity_evidence": identity_evidence,
            "risk_below_threshold": risk < 80,
        },
        "authz_permit_deny": None,
    }


def detect_duplicates(
    *,
    candidate: IdentityRegistration,
    existing: list[IdentityRegistration],
    cases: list[dict] | None = None,
    threshold: float = 0.85,
) -> list[dict]:
    matches: list[dict] = []
    email = candidate.email.lower()
    for other in existing:
        if other.registration_ref == candidate.registration_ref:
            continue
        if other.tenant_id != candidate.tenant_id:
            continue
        score = 0.0
        reasons: list[str] = []
        if other.email == email:
            score = max(score, 1.0)
            reasons.append("email")
        if candidate.phone and other.phone and candidate.phone == other.phone:
            score = max(score, 0.95)
            reasons.append("phone")
        if (
            candidate.national_id
            and other.national_id
            and candidate.national_id == other.national_id
        ):
            score = max(score, 0.98)
            reasons.append("national_id")
        if (
            candidate.employee_number
            and other.employee_number
            and candidate.employee_number == other.employee_number
        ):
            score = max(score, 0.97)
            reasons.append("employee_number")
        if score >= threshold:
            matches.append(
                {
                    "registration_ref": other.registration_ref,
                    "score": score,
                    "reasons": reasons,
                    "status": other.status,
                }
            )
    for case in cases or []:
        if case.get("tenant_id") != candidate.tenant_id:
            continue
        score = 0.0
        reasons: list[str] = []
        if (case.get("email") or "").lower() == email:
            score = 1.0
            reasons.append("case_email")
        if score >= threshold:
            matches.append(
                {
                    "case_ref": case.get("case_ref"),
                    "score": score,
                    "reasons": reasons,
                    "status": case.get("state"),
                }
            )
    return matches


def ai_registration_hints(reg: IdentityRegistration, duplicates: list[dict]) -> dict:
    hints = ["classify_identity_type"]
    if duplicates:
        hints.append("review_duplicate_matches")
    if reg.risk_score >= 50:
        hints.append("require_manual_or_security_approval")
    else:
        hints.append("eligible_for_automatic_approval")
    return {
        "hints": hints,
        "recommended_approval_mode": (
            ApprovalMode.SECURITY.value
            if reg.risk_score >= 50
            else ApprovalMode.AUTOMATIC.value
        ),
        "inference_via": "ai_platform_acl",
    }


def build_initial_profile(reg: IdentityRegistration) -> dict:
    return {
        "personal": {
            "display_name": reg.display_name,
            "email": reg.email,
            "phone": reg.phone,
        },
        "organization": {
            "organization_ref": reg.organization_ref,
            "employee_number": reg.employee_number,
        },
        "security": {
            "identity_type": reg.identity_type,
            "trust_level": reg.trust_level,
            "risk_score": reg.risk_score,
        },
        "compliance": {"national_id_present": bool(reg.national_id)},
        "tenant": {"tenant_id": reg.tenant_id},
        "localization": {
            "locale": reg.metadata.get("locale", "en-US"),
            "timezone": reg.metadata.get("timezone", "UTC"),
            "language": reg.metadata.get("language", "en"),
        },
        "preferences": {"notifications": reg.metadata.get("notifications", True)},
    }


def build_onboarding_checklist(reg: IdentityRegistration) -> dict:
    return {
        "workflow_id": f"onb-{reg.registration_ref}",
        "identity_type": reg.identity_type,
        "checklist": [
            {"step": "welcome_package", "status": "pending"},
            {"step": "initial_assignments", "status": "pending"},
            {"step": "provisioning_request", "status": "pending"},
            {"step": "activation_request", "status": "pending"},
        ],
        "welcome_package": {
            "generated": True,
            "channels": ["in_app", "email"],
        },
    }
