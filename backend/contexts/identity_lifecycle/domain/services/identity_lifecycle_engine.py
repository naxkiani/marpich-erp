"""Identity lifecycle engine — catalog, policy keys, dashboard helpers."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import LifecycleCapability

POLICY_KEYS = [
    "identity_lifecycle.registration.enabled",
    "identity_lifecycle.invitation.enabled",
    "identity_lifecycle.kyc.required",
    "identity_lifecycle.aml.required",
    "identity_lifecycle.consent.required",
    "identity_lifecycle.soft_delete.retention_days",
    "identity_lifecycle.ai_assistant.enabled",
]

CAPABILITY_LABELS = {
    LifecycleCapability.LIFECYCLE_WORKFLOW_ENGINE.value: "Lifecycle Workflow Engine",
    LifecycleCapability.REGISTRATION_INVITATION.value: "Registration & Invitation",
    LifecycleCapability.VERIFICATION_ORCHESTRATION.value: "Verification Orchestration",
    LifecycleCapability.KYC_AML_COMPLIANCE.value: "KYC & AML Compliance",
    LifecycleCapability.ACCOUNT_STATE_MANAGEMENT.value: "Account State Management",
    LifecycleCapability.IDENTITY_MERGE_SPLIT.value: "Identity Merge & Split",
    LifecycleCapability.ARCHIVE_RECOVERY.value: "Archive & Recovery",
    LifecycleCapability.DELETION_GOVERNANCE.value: "Deletion Governance",
    LifecycleCapability.CONSENT_MANAGEMENT.value: "Consent Management",
    LifecycleCapability.LIFECYCLE_AUDIT_TRAIL.value: "Lifecycle Audit Trail",
    LifecycleCapability.AI_LIFECYCLE_ASSISTANT.value: "AI Lifecycle Assistant",
    LifecycleCapability.POLICY_DRIVEN_LIFECYCLE.value: "Policy-Driven Lifecycle",
    LifecycleCapability.LIFECYCLE_DASHBOARD.value: "Lifecycle Dashboard",
    LifecycleCapability.LIFECYCLE_API.value: "Lifecycle API",
}

VERIFICATION_TYPES = [
    {"type": "email_verification", "label": "Email Verification"},
    {"type": "phone_verification", "label": "Phone Verification"},
    {"type": "government_id_verification", "label": "Government ID Verification"},
    {"type": "kyc", "label": "KYC"},
    {"type": "aml", "label": "AML"},
    {"type": "background_verification", "label": "Background Verification"},
    {"type": "identity_verification", "label": "Identity Verification"},
]


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in LifecycleCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_verification_types() -> list[dict]:
    return list(VERIFICATION_TYPES)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "identity_lifecycle", "type": "platform", "label": "Identity Lifecycle Platform"},
            {"id": "identity", "type": "platform", "label": "Identity Core"},
            {"id": "directory", "type": "platform", "label": "Directory Service"},
            {"id": "identity_risk", "type": "platform", "label": "Identity Risk"},
            {"id": "policy", "type": "platform", "label": "Policy Engine"},
        ],
        "edges": [
            {"from": "identity_lifecycle", "to": "identity", "type": "user_lifecycle"},
            {"from": "identity_lifecycle", "to": "directory", "type": "catalog_sync"},
            {"from": "identity_risk", "to": "identity_lifecycle", "type": "lifecycle_event_consume"},
        ],
    }


def build_dashboard(
    *,
    profile: dict,
    cases: list[dict],
    verifications: list[dict],
    audits: list[dict],
) -> dict:
    by_state: dict[str, int] = {}
    for case in cases:
        state = str(case.get("state", "unknown"))
        by_state[state] = by_state.get(state, 0) + 1
    pending_verifications = len([v for v in verifications if v.get("status") == "pending"])
    return {
        "summary": {
            "total_cases": len(cases),
            "by_state": by_state,
            "pending_verifications": pending_verifications,
            "audit_entries": len(audits),
            "active_cases": by_state.get("active", 0),
            "suspended_cases": by_state.get("suspended", 0),
        },
        "profile": profile,
    }
