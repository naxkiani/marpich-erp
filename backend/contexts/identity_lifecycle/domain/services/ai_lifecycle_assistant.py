"""AI Lifecycle Assistant — explainable recommendations for lifecycle operations."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import LifecycleState
from contexts.identity_lifecycle.domain.services import lifecycle_workflow_engine as workflow


def recommend_next_actions(
    *,
    current_state: str,
    verifications: list[dict],
    consents: list[dict],
    kyc_required: bool,
    aml_required: bool,
    consent_required: bool,
) -> dict:
    recommendations: list[dict] = []
    passed_types = {v["verification_type"] for v in verifications if v.get("status") == "passed"}
    has_consent = any(c.get("granted") for c in consents)

    if current_state == LifecycleState.REGISTERED.value:
        if "email_verification" not in passed_types:
            recommendations.append({
                "action": "email_verification",
                "priority": "high",
                "reason": "Email verification is required before account activation.",
            })
        if consent_required and not has_consent:
            recommendations.append({
                "action": "consent_management",
                "priority": "high",
                "reason": "User consent must be recorded per policy.",
            })

    if current_state in {LifecycleState.PENDING_VERIFICATION.value, LifecycleState.REGISTERED.value}:
        if kyc_required and "kyc" not in passed_types:
            recommendations.append({
                "action": "kyc",
                "priority": "high",
                "reason": "KYC verification is required by tenant policy.",
            })
        if aml_required and "aml" not in passed_types:
            recommendations.append({
                "action": "aml",
                "priority": "high",
                "reason": "AML screening is required by tenant policy.",
            })
        if "phone_verification" not in passed_types:
            recommendations.append({
                "action": "phone_verification",
                "priority": "medium",
                "reason": "Phone verification strengthens identity assurance.",
            })

    if current_state == LifecycleState.VERIFIED.value:
        recommendations.append({
            "action": "account_activation",
            "priority": "high",
            "reason": "All required verifications passed — ready for activation.",
        })

    if current_state == LifecycleState.SUSPENDED.value:
        recommendations.append({
            "action": "reactivation",
            "priority": "medium",
            "reason": "Review suspension reason before reactivating.",
            "requires_review": True,
        })

    if current_state == LifecycleState.ARCHIVED.value:
        recommendations.append({
            "action": "identity_recovery",
            "priority": "low",
            "reason": "Archived identity can be recovered if business need exists.",
        })

    if current_state == LifecycleState.SOFT_DELETED.value:
        recommendations.append({
            "action": "identity_recovery",
            "priority": "medium",
            "reason": "Soft-deleted identity is within retention window — recovery possible.",
        })
        recommendations.append({
            "action": "hard_delete",
            "priority": "low",
            "reason": "Hard delete permanently removes identity after retention period.",
            "requires_review": True,
        })

    pending_actions = [
        a["action"]
        for a in workflow.list_workflow_actions()
        if workflow.can_transition(current_state, a["action"])
    ]

    return {
        "current_state": current_state,
        "recommendations": recommendations,
        "available_actions": pending_actions,
        "assistant_version": "1.0",
        "explainable": True,
    }
